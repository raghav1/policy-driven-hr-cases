// Checks that the instance can reach the AI agent service over HTTPS.
// Run: npx now-sdk exec --auth pdi -f scripts/check-agent.js \
//   --scope 77e3b6970d2d4d759440ba33ca5637df \
//          --reason "Check AI service connectivity"
// Expect: 200 {"status":"ok","active_chunks":...}
var base = gs.getProperty('hr_orchestration.agent.base_url');
var r = new sn_ws.RESTMessageV2();
r.setEndpoint(base + '/health');
r.setHttpMethod('get');
r.setHttpTimeout(20000);
var resp = r.execute();
gs.info(
    'GET ' +
        base +
        '/health -> ' +
        resp.getStatusCode() +
        ' ' +
        resp.getBody() +
        ' ' +
        (resp.getErrorMessage() || '')
);
