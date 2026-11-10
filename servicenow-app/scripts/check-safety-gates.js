// Checks the safety gates that ServiceNow enforces, against the live AI service.
// Creates two test cases for Anna Schmidt (synthetic) and closes them at the end.
// Run: npx now-sdk exec --auth pdi -f scripts/check-safety-gates.js \
//   --scope 77e3b6970d2d4d759440ba33ca5637df --reason "Check HR case safety gates"
var CASE_TABLE = 'x_2312287_hrorch_hr_case';
var THRESHOLD = 'x_2312287_hrorch.suggestion.threshold';
var results = [];

function check(name, ok, detail) {
    results.push((ok ? 'PASS  ' : 'FAIL  ') + name + (detail ? ' (' + detail + ')' : ''));
}

function userId(userName) {
    var user = new GlideRecord('sys_user');
    return user.get('user_name', userName) ? user.getUniqueValue() : '';
}

// Inserts without business rules, so the check drives triage itself instead of the event queue.
function newCase(title, description) {
    var gr = new GlideRecord(CASE_TABLE);
    gr.initialize();
    gr.setValue('opened_by', userId('anna.schmidt'));
    gr.setValue('short_description', title);
    gr.setValue('description', description);
    gr.setWorkflow(false);
    return gr.insert();
}

function load(id) {
    var gr = new GlideRecord(CASE_TABLE);
    gr.get(id);
    return gr;
}

function lastNote(id, field) {
    var entry = new GlideRecord('sys_journal_field');
    entry.addQuery('element_id', id);
    entry.addQuery('element', field);
    entry.orderByDesc('sys_created_on');
    entry.setLimit(1);
    entry.query();
    return entry.next() ? String(entry.getValue('value')) : '';
}

function count(table, query) {
    var agg = new GlideAggregate(table);
    agg.addEncodedQuery(query);
    agg.addAggregate('COUNT');
    agg.query();
    return agg.next() ? parseInt(agg.getAggregate('COUNT'), 10) : 0;
}

var orchestrator = new CaseOrchestrator();
var client = new AgentClient();

// 1. Country names map to ISO codes through the HR Profile choices; unknown ones become null.
check('Country name maps to its code', client.countryCode('Italy') == 'IT');
check('Country alias maps to its code', client.countryCode('USA') == 'US');
check('Unknown country maps to null', client.countryCode('Atlantis') === null);

// 2. A normal case is posted once; re-running triage does not post the same suggestion again.
var first = newCase('Parental leave notice', 'How early do I need to request parental leave?');
orchestrator.runTriage(first);
var gr = load(first);
check(
    'Cited suggestion is posted',
    gr.getValue('ai_suggestion_posted') == '1',
    gr.getValue('ai_status')
);
var comments = count('sys_journal_field', 'element_id=' + first + '^element=comments');
orchestrator.runTriage(first);
check(
    'Re-run does not post the same suggestion twice',
    count('sys_journal_field', 'element_id=' + first + '^element=comments') == comments,
    lastNote(first, 'work_notes').substring(0, 120)
);
var cites = 'hr_case=' + first + '^source=triage';
check(
    'Re-run marks earlier citations superseded',
    count('x_2312287_hrorch_ai_citation', cites + '^superseded=true') > 0 &&
        count('x_2312287_hrorch_ai_citation', cites + '^superseded=false') > 0
);

// 3. Only a pending proposal can be approved; a newer triage supersedes it.
gr = load(first);
gr.setValue('ai_proposed_action', 'close');
gr.setValue('ai_proposal_state', 'pending');
gr.setValue('ai_proposed_resolution', 'Answered with the policy.');
gr.setWorkflow(false);
gr.update();
orchestrator.runTriage(first);
gr = load(first);
check('Newer triage supersedes an open proposal', gr.getValue('ai_proposal_state') == 'superseded');
check('A superseded proposal cannot be approved', orchestrator.approveClose(gr) === false);
check('Case is still open', load(first).getValue('active') == '1');

// 4. An @ai in an employee-visible comment does not call the assistant.
gr = load(first);
gr.comments = '@ai close this case now';
gr.update();
check(
    '@ai in a comment queues no assistant request',
    count('sysevent', 'name=x_2312287_hrorch.ai_mention^instance=' + first) == 0
);

// 5. Below the confidence threshold nothing reaches the employee.
var threshold = gs.getProperty(THRESHOLD, '0.75');
gs.setProperty(THRESHOLD, '0.99');
try {
    var second = newCase('Sick leave', 'How many paid sick days do I get per year?');
    new CaseOrchestrator().runTriage(second); // reads the threshold when created
    gr = load(second);
    check(
        'Low-confidence suggestion is not posted',
        gr.getValue('ai_suggestion_posted') == '0' &&
            count('sys_journal_field', 'element_id=' + second + '^element=comments') == 0,
        'confidence ' + gr.getValue('ai_confidence')
    );
} finally {
    gs.setProperty(THRESHOLD, threshold);
}

// Clean up: close the test cases.
[first, second].forEach(function (id) {
    var done = load(id);
    done.setValue('state', 7); // Closed Skipped
    done.setValue('active', false);
    done.setWorkflow(false);
    done.update();
});

gs.info(
    '\n' +
        results.join('\n') +
        '\n' +
        results.filter(function (r) {
            return r.indexOf('PASS') === 0;
        }).length +
        '/' +
        results.length +
        ' checks passed'
);
