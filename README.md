# Policy-driven HR case orchestration

HR cases in ServiceNow are classified by an AI agent, routed by rules that HR owns, and answered with suggestions in which every statement quotes the company policy word for word. ServiceNow keeps control: it applies the routing rules, writes every change, keeps the audit trail, and a person approves critical actions such as closing a case. The AI service only recommends; it never writes to ServiceNow.

- Design overview: [docs/HR_Case_Orchestration_Design.pdf](docs/HR_Case_Orchestration_Design.pdf)
- Demo walkthrough: [docs/DEMO.md](docs/DEMO.md)
- Deferred work: [docs/BACKLOG.md](docs/BACKLOG.md)

## Product demo

Screenshots from a recorded run on a ServiceNow developer instance (synthetic data).

| | |
|---|---|
| **HR-owned routing rules**, checked by order ![](docs/screenshots/01-routing-rules.jpg) | **A new case is classified and routed** by the matching rule ![](docs/screenshots/02-case-classified-and-routed.jpg) |
| **Cited AI suggestion** posted to the employee, plus the routing note ![](docs/screenshots/03-ai-suggestion-with-citations.jpg) | **AI Citations**: every quote pinned to an article version ![](docs/screenshots/04-ai-citations-list.jpg) |
| **Same question, US employee**: US policy is quoted ![](docs/screenshots/05-us-employee-gets-us-policy.jpg) | **HR edits a routing rule** in the UI (no code) ![](docs/screenshots/06-hr-edits-routing-rule.png) |
| **The next case follows the new rule** ![](docs/screenshots/07-case-follows-new-rule.jpg) | **Policy article** in the HR knowledge base ![](docs/screenshots/08-policy-article.jpg) |
| **After a policy edit**, answers quote the new text within seconds ![](docs/screenshots/09-answer-quotes-edited-policy.jpg) | **@ai proposes closing**, flagging a concern for the reviewer ![](docs/screenshots/10-ai-proposes-close.png) |
| **A person decides**: Approve or Reject AI close ![](docs/screenshots/11-approve-ai-close-buttons.jpg) | **Closed after approval**, with the approver recorded ![](docs/screenshots/12-closed-after-approval.jpg) |
| **AI service down**: the case goes to Manual Triage with a reason ![](docs/screenshots/13-fallback-when-ai-is-down.jpg) | **Re-run AI triage** after recovery ![](docs/screenshots/14-recovered-after-rerun.jpg) |

## How it works

```
Employee submits a case (Service Portal)
  -> ServiceNow business rule (async) calls the AI service: POST /triage
       classify  ─┐
                  ├─> verify citations -> recommendation (JSON)
       draft  ────┘   (search policies via MCP tools, cite exact sentences)
  -> ServiceNow applies it: routing rules pick the team, AI fields and citations are saved,
     the suggestion is posted to the employee only if it is fully cited and confident enough
HR tags "@ai" in a work note -> POST /chat -> cited reply as a work note, optional close proposal
HR clicks "Approve AI close" -> ServiceNow closes the case and records who approved
A policy article is published or edited -> POST /ingest -> re-indexed within seconds
```

## Repository layout

| Path | Contents |
|---|---|
| `ai-service/app/main.py` | FastAPI endpoints, API-key auth, rate limiting, startup |
| `ai-service/app/agent/` | LangGraph workflows (`graph.py`), Claude adapter (`llm.py`), offline stand-in (`offline.py`), MCP tool server and client, prompts, citation checks |
| `ai-service/app/ingest/` | HTML parsing into citable sentences, heading-aware chunking, index sync |
| `ai-service/app/search/` | Hybrid retrieval: pgvector + Postgres full text, reciprocal rank fusion, cross-encoder rerank |
| `ai-service/app/sources.py` | Read-only access to ServiceNow (Table API) or the local corpus |
| `ai-service/tests/` | Unit and integration tests |
| `servicenow-app/src/fluent/` | Scoped app as code (ServiceNow SDK): tables, roles, security, logic, UI, reference data |
| `servicenow-app/src/server/` | Script includes: `AgentClient`, `RoutingEngine`, `CaseOrchestrator` |
| `servicenow-app/scripts/` | Instance setup: seed HR data, configure the AI service connection, connectivity check |
| `scripts/` | Synthetic policy generator, ServiceNow seed builder, end-to-end scenario checks |
| `corpus/` | 51 synthetic HR policy articles for a fictional company (generated) |
| `docs/` | Design and planning documents; `docs/source/` regenerates the PDFs |

## Run the AI service

Requires Docker.

```bash
cp .env.example .env     # set SERVICE_API_KEY (openssl rand -hex 32) and ANTHROPIC_API_KEY
python3 scripts/generate_corpus.py
docker compose up -d --build
curl localhost:8000/health
```

Expose it to ServiceNow over HTTPS through the gateway (forward TCP 443 to this host first; `PUBLIC_HOST` is a DNS name that resolves to your public IP, for example `<ip-with-dashes>.sslip.io`):

```bash
docker compose --profile public up -d
```

Configuration lives in `.env`; every setting is documented in `ai-service/app/config.py`. Key ones:

| Setting | Meaning |
|---|---|
| `LLM_PROVIDER` | `anthropic`, or `offline` for a deterministic stand-in that needs no key |
| `LLM_MODEL` | Claude model, `claude-sonnet-5-5` by default |
| `KB_SOURCE` | `servicenow` reads the HR knowledge base; `local` reads `corpus/` |
| `SN_*` | Read-only integration user and table names for the ServiceNow Table API |

## Set up the ServiceNow app

```bash
cd servicenow-app
npx now-sdk auth --add https://<instance>.service-now.com --type basic --alias pdi
npm install && npm run build && npx now-sdk install --auth pdi
npx now-sdk exec --auth pdi -f scripts/seed-hr-data.js --scope 77e3b6970d2d4d759440ba33ca5637df --reason "Seed HR data"
sh scripts/configure-agent.sh            # AI service URL and API key, read from ../.env
```

Then set a password for the `hr_ai_integration` user on the instance and put it in `.env` as `SN_PASSWORD`.

HR policies and routing rules are not part of the app package: HR owns them in the ServiceNow UI, and a redeploy must not overwrite their edits. `seed-hr-data.js` creates the starting knowledge base, 51 articles and 5 routing rules once and never changes existing records (regenerate it with `python3 scripts/build_seed_script.py`). The service URL and key are stored as admin-only global properties, so app installs never reset them.

## Tests

```bash
docker compose run --rm agent pytest -m "not integration"   # parsing, chunking, citation checks
docker compose run --rm agent pytest -s -m integration      # retrieval recall@5 on 30 questions, graph runs via MCP
python3 scripts/run_scenarios.py                            # end-to-end checks against the running API
```

## Design choices worth knowing

- **Exact citations.** Retrieved sentences go to Claude as search results with citations enabled. Each citation is checked word for word against the stored text; a sentence without a citation gets one repair attempt and is otherwise removed, and a draft that needed removals is never posted to the employee.
- **Country-aware answers.** The employee's country comes from their HR Profile or their location. Search only returns that country's policies plus global ones; if the country is unknown, the suggestion goes to HR for review.
- **Human in the loop.** The agent can only propose closing a case. If staff ask it to close, a proposal is always recorded (with any doubts in the resolution) and an HR agent approves or rejects it.
- **Fail safe.** Any AI failure, timeout or invalid response routes the case to HR Manual Triage with a work note explaining why.
- **Least privilege.** The integration user can read cases and HR articles and write nothing.

All data is synthetic. Before using real employee data, add the sensitivity check and redaction described in the backlog.
