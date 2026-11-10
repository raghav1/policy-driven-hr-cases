"""HTTP API called by the ServiceNow app.

Endpoints
  POST /triage           classify a new case and draft a cited suggestion
  POST /chat             answer an @ai request from HR staff, optionally proposing to close
  POST /ingest           re-index one knowledge article after it changes
  POST /admin/reconcile  re-sync the whole knowledge base (not exposed by the gateway)
  GET  /health           liveness and index size

The service only recommends. It never writes to ServiceNow; the ServiceNow app applies results.
Every endpoint except /health needs the shared API key. Failures come back as
{"error": <code>, "detail": <message>} with the status from app.errors.HTTP_STATUS.
"""

import asyncio
import logging
import secrets
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from app.agent.graph import Agent
from app.agent.llm import get_provider
from app.agent.mcp_client import ToolClient
from app.config import Settings, get_settings
from app.db import close_db, connection, init_db
from app.errors import HTTP_STATUS, AgentError
from app.ingest.pipeline import ingest, reconcile
from app.schemas import (
    Answer,
    ChatRequest,
    ChatResponse,
    Classification,
    IngestRequest,
    Proposal,
    TriageRequest,
    TriageResponse,
)
from app.sources import Source, make_source

log = logging.getLogger("hr-agent")


@dataclass
class Runtime:
    """Long-lived objects, created at startup and kept on app.state."""

    settings: Settings
    source: Source
    tools: ToolClient
    agent: Agent
    model: str
    runs: asyncio.Semaphore  # caps concurrent agent runs, and so model spend
    reconcile_task: asyncio.Task


async def _reconcile_forever(source: Source, interval_hours: float) -> None:
    """Full knowledge-base sync at startup and then on a schedule."""
    while True:
        try:
            log.info("reconcile: %s", await asyncio.to_thread(reconcile, source))
        except Exception:
            log.exception("reconcile failed")
        await asyncio.sleep(interval_hours * 3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    if not settings.service_api_key:
        log.warning("SERVICE_API_KEY is empty: every authenticated request will be refused")
    init_db()
    source = make_source(settings)
    tools = ToolClient()
    await tools.start()
    provider = get_provider()
    rt = Runtime(
        settings=settings,
        source=source,
        tools=tools,
        agent=Agent(provider, tools, settings.max_tool_calls),
        model=provider.model,
        runs=asyncio.Semaphore(settings.max_concurrent_runs),
        reconcile_task=asyncio.create_task(
            _reconcile_forever(source, settings.reconcile_interval_hours)
        ),
    )
    app.state.runtime = rt
    log.info("ready: model=%s, policy source=%s", rt.model, settings.kb_source)
    yield
    rt.reconcile_task.cancel()
    await tools.stop()
    source.close()
    close_db()


app = FastAPI(title="HR policy agent service", lifespan=lifespan)


@app.exception_handler(AgentError)
async def agent_error(request: Request, exc: AgentError) -> JSONResponse:
    log.warning("%s %s failed: %s (%s)", request.method, request.url.path, exc.code, exc.message)
    return JSONResponse(
        {"error": exc.code, "detail": exc.message}, status_code=HTTP_STATUS[exc.code]
    )


# ---- request guards ------------------------------------------------------------------------


def runtime(request: Request) -> Runtime:
    rt = getattr(request.app.state, "runtime", None)
    if rt is None:
        raise HTTPException(status_code=503, detail="service is starting")
    return rt


def require_api_key(request: Request, x_api_key: str = Header(default="")) -> None:
    expected = runtime(request).settings.service_api_key
    if not expected or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="invalid API key")


@asynccontextmanager
async def _run_slot(rt: Runtime):
    """Waits for a free agent slot, or fails with "busy" (ServiceNow then routes to manual)."""
    try:
        await asyncio.wait_for(rt.runs.acquire(), rt.settings.queue_timeout_seconds)
    except TimeoutError as exc:
        raise AgentError("busy", "too many requests in progress, try again shortly") from exc
    try:
        yield
    finally:
        rt.runs.release()


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
            chunks = conn.execute("SELECT count(*) AS n FROM policy_chunk WHERE active").fetchone()[
                "n"
            ]
    except Exception as exc:
        log.warning("health check failed: %s", exc)
        raise HTTPException(status_code=503, detail="search index unavailable") from exc
    return {"status": "ok", "active_chunks": chunks}


@app.post("/triage", response_model=TriageResponse, dependencies=[Depends(require_api_key)])
async def triage(req: TriageRequest, rt: Runtime = Depends(runtime)) -> TriageResponse:
    trace_id = uuid.uuid4().hex[:12]
    started = time.monotonic()
    async with _run_slot(rt):
        result = await rt.agent.triage(req)

    answer: Answer = result["answer"]
    blocked = _blocked_reason(req, answer)
    log.info(
        "triage %s %s category=%s cited=%s refs=%d %.1fs",
        trace_id,
        req.number,
        result["classification"]["category"],
        answer.all_claims_cited,
        len(answer.references),
        time.monotonic() - started,
    )
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
async def chat(req: ChatRequest, rt: Runtime = Depends(runtime)) -> ChatResponse:
    trace_id = uuid.uuid4().hex[:12]
    async with _run_slot(rt):
        result = await rt.agent.chat(req)

    proposal = result["proposal"]
    log.info("chat %s %s proposal=%s", trace_id, req.number, bool(proposal))
    return ChatResponse(
        trace_id=trace_id,
        reply=result["answer"],
        proposed_action=Proposal(**proposal) if proposal else None,
        tools_used=result["tools_used"],
        model=rt.model,
    )


@app.post("/ingest", dependencies=[Depends(require_api_key)])
async def ingest_article(req: IngestRequest, rt: Runtime = Depends(runtime)) -> dict:
    """Indexes before answering, so ServiceNow learns whether it worked.

    ServiceNow calls this from a background job, so the wait does not block anyone.
    """
    try:
        outcome = await asyncio.to_thread(ingest, rt.source, req.sys_id)
    except Exception as exc:
        log.exception("ingest %s failed", req.sys_id)
        raise AgentError("index_unavailable", "the article could not be indexed") from exc
    return {"sys_id": req.sys_id, "result": outcome}


@app.post("/admin/reconcile", dependencies=[Depends(require_api_key)])
async def run_reconcile(rt: Runtime = Depends(runtime)) -> dict:
    return await asyncio.to_thread(reconcile, rt.source)
