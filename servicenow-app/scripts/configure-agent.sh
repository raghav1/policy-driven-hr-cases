#!/bin/sh
# Points the ServiceNow app at the AI agent service. Run after install, and again if the URL changes.
# The settings live in global scope so app installs never reset them.
# Reads SERVICE_API_KEY and PUBLIC_HOST from ../.env and never prints the key.
# Usage: sh scripts/configure-agent.sh [auth-alias]
set -eu
cd "$(dirname "$0")/.."
AUTH="${1:-pdi}"
KEY=$(grep '^SERVICE_API_KEY=' ../.env | cut -d= -f2)
HOST=$(grep '^PUBLIC_HOST=' ../.env | cut -d= -f2)
[ -n "$KEY" ] && [ -n "$HOST" ] || { echo "Set SERVICE_API_KEY and PUBLIC_HOST in .env first" >&2; exit 1; }

umask 077
SCRIPT=$(mktemp)
trap 'rm -f "$SCRIPT"' EXIT
cat > "$SCRIPT" <<EOF
function setProp(name, value, description, isPrivate) {
    var p = new GlideRecord('sys_properties');
    if (!p.get('name', name)) {
        p.initialize();
        p.setValue('name', name);
        p.setValue('type', 'string');
        p.setValue('description', description);
        p.setValue('read_roles', 'admin');
        p.setValue('write_roles', 'admin');
        p.setValue('ignore_cache', true);
        if (isPrivate) p.setValue('is_private', true);
        p.setValue('value', value);
        p.insert();
    } else {
        p.setValue('value', value);
        p.update();
    }
    gs.info('configured ' + name);
}
setProp('hr_orchestration.agent.base_url', 'https://$HOST', 'Base URL of the AI agent service', false);
setProp('hr_orchestration.agent.api_key', '$KEY', 'API key sent to the AI agent service in X-API-Key', true);
EOF
npx now-sdk exec --auth "$AUTH" -f "$SCRIPT" --scope global \
    --reason "Configure AI agent service URL and key" 2>&1 | grep -E 'configured|rror'
