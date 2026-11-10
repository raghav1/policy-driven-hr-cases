// Server logic: settings, script includes, events, business rules, script actions and UI actions.
import {
    BusinessRule,
    Property,
    Record,
    ScriptAction,
    ScriptInclude,
    UiAction,
} from '@servicenow/sdk/core'
import { hrAgent } from './roles.now'

// ---- configuration ------------------------------------------------------------
// The service URL and API key are instance-specific secrets, so they are not part of the app.
// scripts/configure-agent.sh creates hr_orchestration.agent.base_url and .agent.api_key in
// global scope.

Property({
    $id: Now.ID['prop_timeout'],
    name: 'x_2312287_hrorch.agent.timeout_ms',
    type: 'integer',
    value: '90000',
    description: 'Timeout for calls to the AI agent service, in milliseconds',
    roles: { read: ['admin'], write: ['admin'] },
})

Property({
    $id: Now.ID['prop_threshold'],
    name: 'x_2312287_hrorch.suggestion.threshold',
    type: 'string',
    value: '0.75',
    description: 'Minimum AI confidence (0 to 1) before an AI suggestion is posted to the employee',
    roles: { read: ['admin'], write: ['admin'] },
})

Property({
    $id: Now.ID['prop_enabled'],
    name: 'x_2312287_hrorch.ai.enabled',
    type: 'boolean',
    value: 'true',
    description: 'Turn AI assistance on or off. When off, every new case goes to manual triage.',
    roles: { read: ['admin'], write: ['admin'] },
})

// ---- script includes ----------------------------------------------------------

ScriptInclude({
    $id: Now.ID['si_agent_client'],
    name: 'AgentClient',
    accessibleFrom: 'package_private',
    script: Now.include('../server/script-includes/AgentClient.server.js'),
})

ScriptInclude({
    $id: Now.ID['si_routing_engine'],
    name: 'RoutingEngine',
    accessibleFrom: 'package_private',
    script: Now.include('../server/script-includes/RoutingEngine.server.js'),
})

ScriptInclude({
    $id: Now.ID['si_case_orchestrator'],
    name: 'CaseOrchestrator',
    accessibleFrom: 'package_private',
    script: Now.include('../server/script-includes/CaseOrchestrator.server.js'),
})

// ---- events -------------------------------------------------------------------
// AI work runs in script actions, off the user's transaction: new cases and re-runs share one path.

Record({
    $id: Now.ID['event_triage'],
    table: 'sysevent_register',
    data: {
        event_name: 'x_2312287_hrorch.triage',
        table: 'x_2312287_hrorch_hr_case',
        description: 'An HR case needs AI triage (new case or a re-run). parm1 = reason.',
        fired_by: 'Business rule: HR case AI triage; UI action: Re-run AI triage',
    },
})

Record({
    $id: Now.ID['event_ai_mention'],
    table: 'sysevent_register',
    data: {
        event_name: 'x_2312287_hrorch.ai_mention',
        table: 'x_2312287_hrorch_hr_case',
        description: 'An HR agent tagged @ai in a work note. parm1 = message, parm2 = author.',
        fired_by: 'Business rule: HR case @ai mention',
    },
})

Record({
    $id: Now.ID['event_kb_changed'],
    table: 'sysevent_register',
    data: {
        event_name: 'x_2312287_hrorch.kb_changed',
        table: 'kb_knowledge',
        description: 'An HR policy article was published, updated or retired. parm1 = event.',
        fired_by: 'Business rule: HR policy article changed',
    },
})

// ---- business rules -------------------------------------------------------------

BusinessRule({
    $id: Now.ID['br_triage'],
    name: 'HR case: AI triage',
    table: 'x_2312287_hrorch_hr_case',
    when: 'after',
    action: ['insert'],
    order: 100,
    active: true,
    script: `(function executeRule(current, previous) {
    gs.eventQueue('x_2312287_hrorch.triage', current, 'new case', '');
})(current, previous);`,
})

BusinessRule({
    $id: Now.ID['br_mention'],
    name: 'HR case: @ai mention',
    table: 'x_2312287_hrorch_hr_case',
    when: 'before',
    action: ['update'],
    order: 200,
    active: true,
    // Only HR staff can ask the assistant, and only in work notes: employee comments are case data.
    condition: 'current.work_notes.changes()',
    script: `(function executeRule(current, previous) {
    if (!gs.hasRole('x_2312287_hrorch.hr_agent')) return;
    var text = current.work_notes.toString();
    if (!text || text.indexOf('[AI assistant]') === 0) return;
    if (!/(^|\\s)@ai\\b/i.test(text)) return;
    var message = text.substring(0, 3900);
    gs.eventQueue('x_2312287_hrorch.ai_mention', current, message, gs.getUserName());
})(current, previous);`,
})

BusinessRule({
    $id: Now.ID['br_kb_changed'],
    name: 'HR policy article changed',
    table: 'kb_knowledge',
    when: 'after',
    action: ['insert', 'update'],
    order: 200,
    active: true,
    condition:
        `current.kb_knowledge_base.title == 'HR Policies' &&
        (current.workflow_state.changes() || current.text.changes() ||
        current.short_description.changes())`,
    script: `(function executeRule(current, previous) {
    var event = current.getValue('workflow_state') == 'published' ? 'updated' : 'retired';
    gs.eventQueue('x_2312287_hrorch.kb_changed', current, event, '');
})(current, previous);`,
})

// ---- script actions (run off the user's transaction) ------------------------------

ScriptAction({
    $id: Now.ID['sa_triage'],
    name: 'HR case: run AI triage',
    eventName: 'x_2312287_hrorch.triage',
    active: true,
    order: 100,
    script: `(function () {
    new CaseOrchestrator().runTriage(current.getUniqueValue());
})();`,
})

ScriptAction({
    $id: Now.ID['sa_ai_mention'],
    name: 'HR case: answer @ai mention',
    eventName: 'x_2312287_hrorch.ai_mention',
    active: true,
    order: 100,
    script: `(function () {
    var caseId = current.getUniqueValue();
    new CaseOrchestrator().handleMention(caseId, String(event.parm1), String(event.parm2));
})();`,
})

ScriptAction({
    $id: Now.ID['sa_kb_changed'],
    name: 'HR policy article: notify AI service',
    eventName: 'x_2312287_hrorch.kb_changed',
    active: true,
    order: 100,
    script: `(function () {
    var result = new AgentClient().ingest(current);
    if (!result.ok) {
        var number = current.getValue('number');
        gs.warn('HR policy re-ingest failed for ' + number + ': ' + result.error);
    }
})();`,
})

// ---- UI actions -----------------------------------------------------------------

UiAction({
    $id: Now.ID['ua_approve_close'],
    table: 'x_2312287_hrorch_hr_case',
    name: 'Approve AI close',
    actionName: 'x_2312287_hrorch_approve_ai_close',
    hint: 'Close this case with the resolution the AI proposed',
    condition:
        `current.ai_proposed_action == 'close' && current.ai_proposal_state == 'pending' &&
        current.active == true`,
    showInsert: false,
    showUpdate: true,
    form: { showButton: true, style: 'primary' },
    roles: [hrAgent],
    order: 100,
    script: `new CaseOrchestrator().approveClose(current);
action.setRedirectURL(current);`,
})

UiAction({
    $id: Now.ID['ua_reject_close'],
    table: 'x_2312287_hrorch_hr_case',
    name: 'Reject AI close',
    actionName: 'x_2312287_hrorch_reject_ai_close',
    hint: 'Keep the case open and dismiss the AI proposal',
    condition:
        `current.ai_proposed_action == 'close' && current.ai_proposal_state == 'pending' &&
        current.active == true`,
    showInsert: false,
    showUpdate: true,
    form: { showButton: true },
    roles: [hrAgent],
    order: 110,
    script: `new CaseOrchestrator().rejectProposal(current);
action.setRedirectURL(current);`,
})

UiAction({
    $id: Now.ID['ua_rerun_triage'],
    table: 'x_2312287_hrorch_hr_case',
    name: 'Re-run AI triage',
    actionName: 'x_2312287_hrorch_rerun_triage',
    hint: 'Ask the AI to classify, route and draft a suggestion again',
    condition: 'current.active == true',
    showInsert: false,
    showUpdate: true,
    form: { showContextMenu: true },
    roles: [hrAgent],
    order: 200,
    script: `gs.eventQueue('x_2312287_hrorch.triage', current, 're-run', gs.getUserName());
gs.addInfoMessage('AI triage was queued. Refresh in a few seconds to see the result.');
action.setRedirectURL(current);`,
})
