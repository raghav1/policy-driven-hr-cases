// One-time fix after splitting AI proposals into action + state: moves the old
// ai_proposed_action values (close, approved, rejected) into ai_proposal_state.
// Run once with:
//   npx now-sdk exec --auth pdi -f scripts/migrate-proposal-state.js \
//     --scope 77e3b6970d2d4d759440ba33ca5637df --reason "Split AI proposal state"
var moved = { pending: 0, approved: 0, rejected: 0 };
var states = { close: 'pending', approved: 'approved', rejected: 'rejected' };
var gr = new GlideRecord('x_2312287_hrorch_hr_case');
gr.addQuery('ai_proposed_action', 'IN', 'close,approved,rejected');
gr.addNullQuery('ai_proposal_state');
gr.query();
while (gr.next()) {
    var state = states[gr.getValue('ai_proposed_action')];
    // A closed case can no longer have a pending proposal.
    if (state == 'pending' && gr.getValue('active') == '0') state = 'superseded';
    gr.setValue('ai_proposed_action', 'close');
    gr.setValue('ai_proposal_state', state);
    gr.setWorkflow(false); // data fix only: no business rules, no journal entries
    gr.update();
    moved[state] = (moved[state] || 0) + 1;
}
gs.info('AI proposal state migrated: ' + JSON.stringify(moved));
