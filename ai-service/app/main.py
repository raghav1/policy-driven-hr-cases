"""HTTP API called by the ServiceNow app.

Endpoints
  POST /triage           classify a new case and draft a cited suggestion
  POST /chat             answer an @ai request from HR staff, optionally proposing to close
  POST /ingest           re-index one knowledge article after it changes (runs in the background)
  POST /admin/reconcile  re-sync the whole knowledge base (not exposed by the gateway)
  GET  /health           liveness and index size

The service only recommends. It never writes to ServiceNow; the ServiceNow app applies results.
"""
import asyncio
import logging
import secrets
import time
import uuid
from collections import deque
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.agent.graph import Agent
from app.agent.llm import LLMError, get_provider
from app.agent.mcp_client import ToolClient
from app.config import get_settings
from app.db import close_db, connection, init_db
from app.ingest.pipeline import ingest, reconcile
from app.schemas import (Answer, ChatRequest, ChatResponse, Classification, IngestRequest, Proposal,
                         TriageRequest, TriageResponse)

settings = get_settings()
logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("hr-agent")


@dataclass
class Runtime:
    """Long-lived objects created at startup."""

    agent: Agent
    tools: ToolClient
    model: str
    reconcile_task: asyncio.Task


runtime: Runtime | None = None


async def _reconcile_forever(interval_hours: float) -> None:
    """Full knowledge-base sync at startup and then on a schedule."""
    while True:
        try:
            log.info("reconcile: %s", await asyncio.to_thread(reconcile))
        except Exception:
            log.exception("reconcile failed")
        await asyncio.sleep(interval_hours * 3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global runtime
    if not settings.service_api_key:
        log.warning("SERVICE_API_KEY is empty: every authenticated request will be refused")
    init_db()
    tools = ToolClient()
    await tools.start()
    provider = get_provider()
    runtime = Runtime(
        agent=Agent(provider, tools),
        tools=tools,
        model=provider.model,
        reconcile_task=asyncio.create_task(_reconcile_forever(settings.reconcile_interval_hours)),
    )
    log.info("ready: model=%s, policy source=%s", provider.model, settings.kb_source)
    yield
    runtime.reconcile_task.cancel()
    await tools.stop()
    close_db()


app = FastAPI(title="HR policy agent service", lifespan=lifespan)


# ---- request guards ------------------------------------------------------------------------

_requests_by_client: dict[str, deque[float]] = {}


def _client_id(request: Request) -> str:
    # Behind the gateway every request comes from the proxy, so use the original client address.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    """Sliding one-minute window per client."""
    now = time.monotonic()
    window = _requests_by_client.setdefault(_client_id(request), deque())
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= settings.rate_limit_per_minute:
        return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)
    window.append(now)
    # Forget idle clients so the table does not grow without bound.
    if len(_requests_by_client) > 10_000:
        for key in [k for k, w in _requests_by_client.items() if not w or now - w[-1] > 60]:
            del _requests_by_client[key]
    return await call_next(request)


def require_api_key(x_api_key: str = Header(default="")) -> None:
    expected = settings.service_api_key
    if not expected or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="invalid API key")


def _runtime() -> Runtime:
    if runtime is None:
        raise HTTPException(status_code=503, detail="service is starting")
    return runtime


def _answer(raw: dict) -> Answer:
    return Answer(
        text=raw["text"],
        formatted=raw["formatted"],
        claims=raw["claims"],
        all_claims_cited=raw["all_claims_cited"],
        found_policy=bool(raw["references"]),
        removed_uncited=raw["removed_uncited"],
    )


def _blocked_reason(req: TriageRequest, answer: Answer) -> str | None:
    """Why a triage suggestion must go to HR for review instead of the employee, or None."""
    if not req.employee.country:
        return "the employee's country is unknown, so the right country's policy cannot be chosen"
    if not answer.found_policy:
        return "no matching policy was found"
    if not answer.all_claims_cited:
        return "not every statement could be cited"
    if answer.removed_uncited:
        return "uncited statements were removed, so the draft may be incomplete"
    return None


# ---- endpoints -----------------------------------------------------------------------------

@app.get("/health")
def health() -> dict:
    try:
        with connection() as conn:
            chunks = conn.execute("SELECT count(*) AS n FROM policy_chunk WHERE active").fetchone()["n"]
    except Exception as exc:
        log.warning("health check failed: %s", exc)
        raise HTTPException(status_code=503, detail="search index unavailable") from exc
    return {"status": "ok", "active_chunks": chunks}


@app.post("/triage", response_model=TriageResponse, dependencies=[Depends(require_api_key)])
async def triage(req: TriageRequest) -> TriageResponse:
    rt = _runtime()
    trace_id = uuid.uuid4().hex[:12]
    started = time.monotonic()
    try:
        result = await rt.agent.triage(req)
    except LLMError as exc:
        log.warning("triage %s %s failed: %s", trace_id, req.number, exc)
        raise HTTPException(status_code=502, detail=f"agent failed: {exc}") from exc

    answer = _answer(result["answer"])
    blocked = _blocked_reason(req, answer)
    log.info("triage %s %s category=%s cited=%s refs=%d %.1fs", trace_id, req.number,
             result["classification"]["category"], answer.all_claims_cited,
             len(result["answer"]["references"]), time.monotonic() - started)
    return TriageResponse(
        trace_id=trace_id,
        classification=Classification(**result["classification"]),
        suggestion=answer,
        suggestion_allowed=blocked is None,
        suggestion_blocked_reason=blocked,
        tools_used=result["tools_used"],
        model=rt.model,
    )


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(require_api_key)])
async def chat(req: ChatRequest) -> ChatResponse:
    rt = _runtime()
    trace_id = uuid.uuid4().hex[:12]
    try:
        result = await rt.agent.chat(req)
    except LLMError as exc:
        log.warning("chat %s %s failed: %s", trace_id, req.number, exc)
        raise HTTPException(status_code=502, detail=f"agent failed: {exc}") from exc

    proposal = result["proposal"]
    log.info("chat %s %s proposal=%s", trace_id, req.number, bool(proposal))
    return ChatResponse(
        trace_id=trace_id,
        reply=_answer(result["answer"]),
        proposed_action=Proposal(**proposal) if proposal else None,
        tools_used=result["tools_used"],
        model=rt.model,
    )


@app.post("/ingest", status_code=202, dependencies=[Depends(require_api_key)])
async def ingest_article(req: IngestRequest, background: BackgroundTasks) -> dict:
    background.add_task(ingest, req.sys_id)
    return {"accepted": req.sys_id}


@app.post("/admin/reconcile", dependencies=[Depends(require_api_key)])
async def run_reconcile() -> dict:
    return await asyncio.to_thread(reconcile)
