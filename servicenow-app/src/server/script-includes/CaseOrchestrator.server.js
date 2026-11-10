/**
 * Applies the AI agent's recommendations to HR cases. The agent only recommends;
 * every write to a case happens here, under ServiceNow's rules.
 */
var CaseOrchestrator = Class.create();
CaseOrchestrator.prototype = {
    CASE_TABLE: 'x_2312287_hrorch_hr_case',
    AI_TAG: '[AI assistant]',
    MANUAL_GROUP: 'HR Manual Triage',

    initialize: function () {
        this.client = new AgentClient();
        this.threshold = parseFloat(
            gs.getProperty('x_2312287_hrorch.suggestion.threshold', '0.75')
        );
    },

    // ---- triage --------------------------------------------------------------

    runTriage: function (caseId) {
        var gr = new GlideRecord(this.CASE_TABLE);
        if (!gr.get(caseId)) return;

        // A journal field keeps only the last value set before update(), so notes are collected
        // and written once.
        var notes = [];
        if (gs.getProperty('x_2312287_hrorch.ai.enabled', 'true') != 'true') {
            gr.setValue('ai_status', 'off');
            notes.push('AI assistance is turned off. ' + this._routeToManual(gr));
            this._writeNotes(gr, notes);
            return;
        }

        // A new triage replaces any open proposal from earlier work on the case.
        if (this._supersedeProposal(gr))
            notes.push('Earlier close proposal superseded because AI triage ran again.');
        var result = this.client.triage(gr);
        if (!result.ok) {
            gr.setValue('ai_status', 'failed');
            notes.push('AI triage failed (' + result.error + '). ' + this._routeToManual(gr));
            this._writeNotes(gr, notes);
            return;
        }

        var r = result.body;
        var c = r.classification;
        gr.setValue('category', c.category);
        gr.setValue('topics', (c.topics || []).join(', '));
        gr.setValue('severity', c.severity);
        gr.setValue('priority', String(c.priority));
        gr.setValue('ai_confidence', c.confidence);
        gr.setValue('ai_reasoning', c.reasoning);
        gr.setValue('ai_trace_id', r.trace_id);
        gr.setValue('ai_model', r.model);
        gr.setValue('ai_status', 'completed');

        var rule = new RoutingEngine().evaluate(c.category, c.severity);
        if (rule) {
            gr.setValue('assignment_group', rule.assignment_group);
            if (rule.assigned_to) gr.setValue('assigned_to', rule.assigned_to);
            gr.setValue('routing_rule', rule.sys_id);
            notes.push(
                'Routed to ' +
                    rule.group_name +
                    ' by rule "' +
                    rule.name +
                    '" (order ' +
                    rule.order +
                    ').'
            );
        } else {
            notes.push('No routing rule matched. ' + this._routeToManual(gr));
        }
        notes.push(
            'Category ' +
                c.category +
                ', severity ' +
                c.severity +
                ', confidence ' +
                c.confidence +
                '. ' +
                c.reasoning
        );

        var s = r.suggestion;
        // The employee must not get the same suggestion twice. The model words it differently on
        // each run, so "the same" means quoting the same policy sentences as the posted one.
        var alreadyPosted =
            gr.getValue('ai_suggestion_posted') == '1' &&
            this._postedQuotes(gr) == this._quoteKey(s.references);
        gr.setValue('ai_suggestion', s.formatted);
        if (s.removed_uncited > 0) {
            notes.push(
                s.removed_uncited + ' uncited sentence(s) removed from the AI draft before review.'
            );
        }
        var reason = this._blockReason(r, c.confidence);
        if (!reason && alreadyPosted) {
            notes.push('AI suggestion quotes the same policy as the posted one; not posted again.');
        } else if (!reason) {
            gr.comments =
                'AI suggestion (drafted by the HR assistant from company policy; ' +
                'the HR team will review your case)\n\n' +
                s.formatted;
            gr.setValue('ai_suggestion_posted', true);
            notes.push('AI suggestion posted to the employee.');
        } else {
            // A re-run must not keep an earlier run's flag.
            gr.setValue('ai_suggestion_posted', false);
            notes.push(
                'AI suggestion not posted: ' +
                    reason +
                    '.' +
                    (s.formatted ? ' Draft for reference:\n\n' + s.formatted : '')
            );
        }
        this._writeNotes(gr, notes);
        this._supersedeCitations(gr, 'triage');
        this._saveCitations(gr, s, 'triage', r.trace_id);
    },

    // Why the suggestion goes to HR instead of the employee, or '' when it can be posted.
    _blockReason: function (r, confidence) {
        if (!r.suggestion_allowed)
            return r.suggestion_blocked_reason || 'the AI service did not allow it';
        if (confidence < this.threshold)
            return 'confidence ' + confidence + ' is below the threshold of ' + this.threshold;
        return '';
    },

    // Assigns the case to manual triage and returns the sentence for the work note.
    _routeToManual: function (gr) {
        var group = new GlideRecord('sys_user_group');
        if (group.get('name', this.MANUAL_GROUP))
            gr.setValue('assignment_group', group.getUniqueValue());
        return 'Routed to ' + this.MANUAL_GROUP + '.';
    },

    _writeNotes: function (gr, notes) {
        gr.work_notes = this.AI_TAG + ' ' + notes.join('\n');
        gr.update();
    },

    // ---- @ai chat ------------------------------------------------------------

    handleMention: function (caseId, message, author) {
        var gr = new GlideRecord(this.CASE_TABLE);
        if (!gr.get(caseId)) return;
        var result = this.client.chat(gr, message, author);
        if (!result.ok) {
            gr.work_notes =
                this.AI_TAG +
                ' The AI assistant is unavailable right now (' +
                result.error +
                '). Please try again.';
            gr.update();
            return;
        }
        var r = result.body;
        var lines = [
            this.AI_TAG + ' Reply to ' + author + ':',
            '',
            this._noMention(r.reply.formatted),
        ];
        // Approval must always refer to the latest exchange, so an earlier open proposal ends here.
        if (this._supersedeProposal(gr))
            lines.push('', 'The earlier close proposal is superseded by this request.');
        if (r.proposed_action && r.proposed_action.action == 'close') {
            gr.setValue('ai_proposed_action', 'close');
            gr.setValue('ai_proposal_state', 'pending');
            gr.setValue('ai_proposed_resolution', r.proposed_action.resolution);
            lines.push(
                '',
                'Proposed closing this case: "' +
                    r.proposed_action.resolution +
                    '". An HR agent can approve it with "Approve AI close".'
            );
        }
        gr.work_notes = lines.join('\n');
        gr.update();
        this._saveCitations(gr, r.reply, 'chat', r.trace_id);
    },

    _noMention: function (text) {
        // Replies must never re-trigger the @ai rule.
        return String(text || '').replace(/@ai\b/gi, 'AI');
    },

    // ---- human approval --------------------------------------------------------

    // Only a pending proposal can be acted on; a superseded or already decided one cannot.
    _isPending: function (gr) {
        return (
            gr.getValue('ai_proposed_action') == 'close' &&
            gr.getValue('ai_proposal_state') == 'pending'
        );
    },

    // Retires an open proposal. Returns true if there was one, so the caller can note it.
    _supersedeProposal: function (gr) {
        if (!this._isPending(gr)) return false;
        gr.setValue('ai_proposal_state', 'superseded');
        return true;
    },

    approveClose: function (gr) {
        if (!this._isPending(gr)) return false;
        var resolution = gr.getValue('ai_proposed_resolution');
        gr.setValue('state', 3); // Closed Complete
        gr.setValue('active', false);
        gr.setValue('close_notes', resolution);
        gr.setValue('ai_proposal_state', 'approved');
        gr.work_notes =
            this.AI_TAG + ' AI-proposed closure approved by ' + gs.getUserDisplayName() + '.';
        gr.update();
        return true;
    },

    rejectProposal: function (gr) {
        if (!this._isPending(gr)) return false;
        gr.setValue('ai_proposal_state', 'rejected');
        gr.work_notes =
            this.AI_TAG + ' AI-proposed closure rejected by ' + gs.getUserDisplayName() + '.';
        gr.update();
        return true;
    },

    // ---- audit -----------------------------------------------------------------

    // Identifies a suggestion by the policy sentences it quotes, in a stable order.
    _quoteKey: function (references) {
        var quotes = [];
        for (var i = 0; i < (references || []).length; i++) quotes.push(references[i].quote);
        return quotes.sort().join('\n');
    },

    // The quotes of the current (not superseded) triage suggestion.
    _postedQuotes: function (gr) {
        var cite = new GlideRecord('x_2312287_hrorch_ai_citation');
        cite.addQuery('hr_case', gr.getUniqueValue());
        cite.addQuery('source', 'triage');
        cite.addQuery('superseded', false);
        cite.query();
        var references = [];
        while (cite.next()) references.push({ quote: cite.getValue('quote') });
        return this._quoteKey(references);
    },

    // Marks earlier citations of this kind as replaced, so the list shows which quotes are current.
    _supersedeCitations: function (gr, source) {
        var old = new GlideRecord('x_2312287_hrorch_ai_citation');
        old.addQuery('hr_case', gr.getUniqueValue());
        old.addQuery('source', source);
        old.addQuery('superseded', false);
        old.setValue('superseded', true);
        old.updateMultiple();
    },

    _saveCitations: function (gr, answer, source, traceId) {
        var seen = {};
        var claims = answer.claims || [];
        for (var i = 0; i < claims.length; i++) {
            var cites = claims[i].citations || [];
            for (var j = 0; j < cites.length; j++) {
                var c = cites[j];
                if (seen[c.ref]) continue;
                seen[c.ref] = true;
                var cite = new GlideRecord('x_2312287_hrorch_ai_citation');
                cite.initialize();
                cite.setValue('hr_case', gr.getUniqueValue());
                cite.setValue('source', source);
                cite.setValue('ref_number', c.ref);
                cite.setValue('article', c.article);
                cite.setValue('article_version', c.version);
                cite.setValue('section', c.section);
                cite.setValue('quote', c.quote);
                cite.setValue('chunk_id', c.chunk_id);
                cite.setValue('start_char', c.start_char);
                cite.setValue('end_char', c.end_char);
                cite.setValue('trace_id', traceId);
                var kb = new GlideRecord('kb_knowledge');
                if (kb.get('number', c.article)) cite.setValue('kb_article', kb.getUniqueValue());
                cite.insert();
            }
        }
    },

    type: 'CaseOrchestrator',
};
