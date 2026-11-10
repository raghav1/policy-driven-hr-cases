# Backlog: after the MVP

Not part of the MVP ([MVP_SCOPE.md](MVP_SCOPE.md)). Mention the important ones in the design doc as "next steps" so reviewers see they were considered.

## Sensitivity check (highest priority after MVP)

Gate before any AI call. Sensitive cases (harassment, discrimination, retaliation, medical, legal, whistleblowing, investigations, self-harm, immigration) go to a restricted queue and their text never leaves ServiceNow.

ServiceNow has the building blocks for restricting access (ACLs, roles, HRSD Center of Excellence security policies) and masking (Data Privacy for Now Assist, Sensitive Data Handler). It has no ready-made "is this HR case sensitive" check usable on a developer instance, so build the check on top of ACLs.

Layers, each able to raise sensitivity but never lower it:

1. Intake category: "Raise a concern" style categories are sensitive by definition.
2. Configurable keyword rules: `Sensitivity Rule` table (term or regex, category, active, owner) plus a `SensitivityChecker` Script Include. HR adds terms without code.
3. AI second check after redaction: agent returns `sensitivity`; if flagged, restrict and hide the draft.
4. Manual "Mark sensitive" UI action; only the restricted-case reviewer role can clear it.

When flagged: set `u_sensitivity` and `u_sensitivity_reason`, ACLs on the case, journal entries (`sys_journal_field`) and attachments, assign to the restricted group, strip the description from notifications, block `@ai` and agent calls, log the decision. Re-run on insert and when description or comments change.

Known gap: keyword rules miss indirect wording, and the AI check only sees text after it has left the instance (redacted). Lean toward over-restricting. Production fix: in-platform classification (Predictive Intelligence, or Now Assist with Data Privacy).

Tests: harassment keyword blocks the agent call; indirect wording caught by AI only; new rule row takes effect without code; `@ai` refused on a restricted case.

## Other deferred items

| Item | Why it waits |
|---|---|
| PII redaction (`CaseRedactor`) | MVP uses synthetic data only; required before any real data |
| Stable hostname (DNS, Cloudflare Tunnel) or cloud hosting | Public IP is enough for the demo |
| PDF attachments on KB articles | Open decision; article bodies first |
| Contextual chunk summaries (LLM-written context per chunk) | Measure retrieval first; add if the test set shows misses |
| ServiceNow AI Search instead of pgvector | Keeps the index in the platform; not available on a developer instance |
| `find_similar_cases` tool | Not needed for the six steps |
| Side-chat panel (UI Builder) | Inline `@ai` covers step 5 |
| Autonomy levels per category | One threshold plus the citation rule is enough |
| More critical actions (restrict, escalate, reassign) | Closing shows the approval pattern |
| Policy table with versions, owners, effective dates, conflicts | One routing rules table proves configurability |
| Subflows per HR area | Assignment is enough to show routing |
| Workspace UI | Core UI form and Service Portal are enough |
| Tracing dashboards, token and latency metrics | Logs are enough for the demo |
| ATF suite and CI/CD | Recorded tests first; add ATF if time allows |
| Now Assist / AI Agent Studio swap | Not available on a developer instance; describe as the upgrade path |
