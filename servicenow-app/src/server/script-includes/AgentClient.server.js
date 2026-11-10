/**
 * Calls the AI agent service. Every method returns { ok, status, body, error } and never throws,
 * so callers can always fall back to manual handling.
 */
var AgentClient = Class.create();
AgentClient.prototype = {
    initialize: function () {
        this.baseUrl = gs.getProperty('hr_orchestration.agent.base_url', '');
        this.apiKey = gs.getProperty('hr_orchestration.agent.api_key', '');
        this.timeoutMs = parseInt(gs.getProperty('x_2312287_hrorch.agent.timeout_ms', '90000'), 10);
    },

    triage: function (caseGr) {
        return this._post('/triage', {
            case_id: caseGr.getUniqueValue(),
            number: caseGr.getValue('number'),
            title: caseGr.getValue('short_description') || '',
            description: caseGr.getValue('description') || '',
            employee: this._employee(caseGr.getValue('opened_by')),
        });
    },

    chat: function (caseGr, message, author) {
        return this._post('/chat', {
            case_id: caseGr.getUniqueValue(),
            number: caseGr.getValue('number'),
            message: String(message),
            author: String(author),
        });
    },

    ingest: function (kbGr, event) {
        return this._post('/ingest', {
            sys_id: kbGr.getUniqueValue(),
            number: kbGr.getValue('number'),
            version: parseInt(kbGr.getValue('sys_mod_count'), 10) || 0,
            event: String(event),
        });
    },

    // Country names used on cmn_location, mapped to the ISO codes the policy index uses.
    COUNTRY_CODES: {
        'usa': 'US', 'united states': 'US', 'united states of america': 'US',
        'germany': 'DE', 'deutschland': 'DE',
        'india': 'IN',
        'united kingdom': 'GB', 'uk': 'GB', 'great britain': 'GB', 'england': 'GB',
        'italy': 'IT', 'france': 'FR', 'canada': 'CA', 'australia': 'AU', 'japan': 'JP', 'china': 'CN',
        'ireland': 'IE', 'spain': 'ES', 'netherlands': 'NL', 'mexico': 'MX', 'brazil': 'BR', 'brasil': 'BR',
    },

    /**
     * Country and employee type for the person who opened the case: the HR Profile first, then the
     * country of the user's location. Unknown countries pass through as written, so the search only
     * matches global policies for them.
     */
    _employee: function (userId) {
        var result = { country: null, employee_type: null };
        if (!userId) return result;
        var profile = new GlideRecord('x_2312287_hrorch_hr_profile');
        if (profile.get('user', userId)) {
            result.country = profile.getValue('country') || null;
            result.employee_type = profile.getValue('employee_type') || null;
        }
        if (!result.country) {
            var user = new GlideRecord('sys_user');
            if (user.get(userId) && user.getValue('location')) {
                var name = String(user.location.country || '').trim();
                if (name) result.country = this.COUNTRY_CODES[name.toLowerCase()] || name;
            }
        }
        return result;
    },

    _post: function (path, payload) {
        if (!this.baseUrl) {
            return { ok: false, status: 0, error: 'hr_orchestration.agent.base_url is not set' };
        }
        try {
            var request = new sn_ws.RESTMessageV2();
            request.setEndpoint(this.baseUrl.replace(/\/+$/, '') + path);
            request.setHttpMethod('post');
            request.setRequestHeader('Content-Type', 'application/json');
            request.setRequestHeader('Accept', 'application/json');
            request.setRequestHeader('X-API-Key', this.apiKey);
            request.setHttpTimeout(this.timeoutMs);
            request.setRequestBody(JSON.stringify(payload));
            var response = request.execute();
            var status = response.getStatusCode();
            var text = response.getBody();
            if (status < 200 || status >= 300) {
                var detail = text || response.getErrorMessage() || '';
                return { ok: false, status: status, error: 'HTTP ' + status + ': ' + String(detail).substring(0, 300) };
            }
            return { ok: true, status: status, body: text ? JSON.parse(text) : null };
        } catch (e) {
            return { ok: false, status: 0, error: String(e) };
        }
    },

    type: 'AgentClient',
};
