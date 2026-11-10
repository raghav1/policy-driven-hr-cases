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

    // The employee is sent with chat too, so the assistant only reads policies that apply to them.
    chat: function (caseGr, message, author) {
        return this._post('/chat', {
            case_id: caseGr.getUniqueValue(),
            number: caseGr.getValue('number'),
            message: String(message),
            author: String(author),
            employee: this._employee(caseGr.getValue('opened_by')),
        });
    },

    ingest: function (kbGr) {
        return this._post('/ingest', { sys_id: kbGr.getUniqueValue() });
    },

    // Other spellings of country names seen on cmn_location. The country list itself is the
    // HR Profile country field's choices (ISO code = value, name = label).
    COUNTRY_ALIASES: {
        usa: 'US',
        'united states of america': 'US',
        deutschland: 'DE',
        uk: 'GB',
        'great britain': 'GB',
        england: 'GB',
        brasil: 'BR',
    },

    /** ISO code for a country name, or null when the app does not know the country. */
    countryCode: function (name) {
        var key = String(name || '')
            .trim()
            .toLowerCase();
        if (!key) return null;
        if (this.COUNTRY_ALIASES[key]) return this.COUNTRY_ALIASES[key];
        var choice = new GlideRecord('sys_choice');
        choice.addQuery('name', 'x_2312287_hrorch_hr_profile');
        choice.addQuery('element', 'country');
        choice.addQuery('inactive', false);
        choice.query();
        while (choice.next()) {
            var code = choice.getValue('value');
            if (choice.getValue('label').toLowerCase() == key || code.toLowerCase() == key)
                return code;
        }
        return null;
    },

    /**
     * Country and employee type for the person who opened the case: the HR Profile first, then the
     * country of the user's location. An unknown country is sent as null, so the agent only sees
     * global policies and the suggestion goes to HR for review.
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
                result.country = this.countryCode(user.location.country);
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
                return {
                    ok: false,
                    status: status,
                    error: this._describeError(status, text, response.getErrorMessage()),
                };
            }
            return { ok: true, status: status, body: text ? JSON.parse(text) : null };
        } catch (e) {
            return { ok: false, status: 0, error: String(e) };
        }
    },

    // The service answers failures with {"error": code, "detail": message}.
    _describeError: function (status, text, transportError) {
        try {
            var body = JSON.parse(text);
            if (body && body.error)
                return body.error + ': ' + body.detail + ' (HTTP ' + status + ')';
        } catch (e) {
            // not JSON: fall through
        }
        return 'HTTP ' + status + ': ' + String(text || transportError || '').substring(0, 300);
    },

    type: 'AgentClient',
};
