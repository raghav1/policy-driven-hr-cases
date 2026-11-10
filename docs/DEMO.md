# Demo walkthrough

About 12 minutes. Instance: https://dev479982.service-now.com

## Before you start (5 minutes ahead)

1. Docker is running and the stack is up: `docker compose --profile public up -d` from the project folder.
2. The instance can reach the service. From `servicenow-app/`:
   `npx now-sdk exec --auth pdi -f scripts/check-agent.js --scope 77e3b6970d2d4d759440ba33ca5637df --reason "pre-demo check"`
   Expect `200 {"status":"ok","active_chunks":738}`.
3. Log in to the instance as admin so the developer instance is awake.
4. Open these tabs:
   - Open HR Cases: https://dev479982.service-now.com/now/nav/ui/classic/params/target/x_2312287_hrorch_hr_case_list.do
   - Routing Rules: https://dev479982.service-now.com/now/nav/ui/classic/params/target/x_2312287_hrorch_routing_rule_list.do
   - Portal form: https://dev479982.service-now.com/sp?id=sc_cat_item&sys_id=4993ecfc0fa44c2eb7e404f56391fe5d
   - The design PDF
5. Your Mac must not sleep during the demo.

## 1. The problem and the approach (1 minute, design PDF)

Say: HR gets repetitive policy questions. Routing should be owned by HR as configuration, AI should help with classification and answers, and every answer must be traceable to policy. Show the architecture diagram: ServiceNow decides and writes, the AI service only recommends, the LLM sits behind an adapter.

## 2. An employee submits a case (2 minutes)

1. Impersonate **Anna Schmidt** (Germany): user menu, Impersonate user.
2. Open the portal form tab. Title: "Parental leave". Details: "My partner is due in March. How much parental leave can I take, and how early do I need to ask?" Submit.
3. Say: the record producer created an HR case. An async business rule calls the AI service so the employee never waits.
4. End impersonation.

## 3. What happened on the case (3 minutes)

Open the new case from Open HR Cases (wait about 10 seconds and refresh if AI status is still Pending).

Point out:
- **Category, severity, priority, topics**: set from the AI classification.
- **Assignment group and assignee** (HR Leave, Hana Weber) and **Routing rule**: chosen by the rule table, not by the AI.
- **Activity**: the employee-visible comment "AI suggestion" with numbered references, each quoting the policy word for word with article number and version.
- **Work note**: why it was routed, the AI's confidence and reasoning, and whether the suggestion was posted.
- **AI assistant section**: confidence, model, trace ID, and the **AI Citations** related list, each pinned to the knowledge article version.

Say: the suggestion is posted only if confidence is above the threshold and every statement is cited. Show case HRC0001004 (Aarav, vague request): unknown category, low confidence, nothing posted, routed to HR Manual Triage.

## 4. Change routing without code (2 minutes)

1. Routing Rules tab. Show the five rules and the order column. Say: first active match wins; the last row is the catch-all.
2. Edit "Benefits" and change the group to HR Payroll (or add a new rule above it). Save.
3. Submit a benefits question as **John Miller** (US): "Can I add my wife to my health insurance?"
4. Open the case: it routes by the new rule. Change the rule back afterwards.

## 5. HR asks the AI for help (2 minutes)

On Anna's case, as admin:
1. Work note: `@ai check KB0090002 for the notice period`. Save.
2. Refresh after about 10 seconds. The AI replies in a work note with the notice period quoted from that article.
3. Work note: `@ai the employee is answered, please close this`. Save and refresh.
4. The AI proposes closing. The case is still open. Click **Approve AI close**: the case closes with the proposed resolution and the approval is recorded.

Say: the AI service's integration user is read-only, so it cannot close anything itself; closing always needs a person.

## 6. Failure handling (1 minute)

Optional, if you want to show it live: stop the service (`docker compose stop agent`), submit a case, and show it routed to HR Manual Triage with a work note explaining the failure. Start it again with `docker compose start agent`.

Otherwise show case HRC0001001, which ran before the service was connected.

## 7. Wrap up (1 minute)

- Built with the ServiceNow SDK: scoped app in Git, tables, roles, ACLs, business rules, script includes, events, UI actions, record producer, all as code.
- AI service: FastAPI, LangGraph, MCP tools, hybrid search over chunked policies, citation checks.
- Tests: unit and integration tests, retrieval recall@5 of 1.00 on 30 questions, scenario script against the live API.
- Next steps: sensitivity check and redaction before real data, Now Assist on a licensed instance, ATF suite.

## If something goes wrong

| Symptom | Fix |
|---|---|
| AI status stays Pending | Wait 20 seconds; async rules can queue. Then check `docker compose logs agent`. |
| Work note says the service is unavailable | Run the pre-demo check above. If the public IP changed, update `PUBLIC_HOST` in `.env`, restart the gateway, run `sh servicenow-app/scripts/configure-agent.sh`. |
| Suggestion reads like quoted sentences | The service is in offline mode. Set `LLM_PROVIDER=anthropic` and `ANTHROPIC_API_KEY` in `.env`, then `docker compose up -d agent`. |
| Instance asleep | Log in at the instance URL and wake it from the developer portal. |
