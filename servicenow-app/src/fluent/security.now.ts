// Access rules. Tables get field-level rules from their role lists (tables.now.ts); the table-level
// and special-case rules live here so the whole security model is in one place.
import { Acl } from '@servicenow/sdk/core'
import { hrAgent, integration, policyAdmin } from './roles.now'

// Employees can read the HR cases they opened.
Acl({
    $id: Now.ID['acl_case_read_own'],
    type: 'record',
    table: 'x_2312287_hrorch_hr_case',
    operation: 'read',
    roles: [],
    script: 'answer = current.opened_by == gs.getUserID();',
    description: 'Employees can read HR cases they opened',
})

// The AI service reads policy articles and cases, nothing else.
Acl({
    $id: Now.ID['acl_kb_read_integration'],
    type: 'record',
    table: 'kb_knowledge',
    operation: 'read',
    roles: [integration],
    description: 'AI agent integration user can read knowledge articles',
})

// Table-level read for HR roles. The table definitions only generate field-level (.*) read rules.
Acl({
    $id: Now.ID['acl_case_read_roles'],
    type: 'record',
    table: 'x_2312287_hrorch_hr_case',
    operation: 'read',
    roles: [hrAgent, integration],
    description: 'HR agents and the AI integration user can read HR cases',
})
Acl({
    $id: Now.ID['acl_rule_read_roles'],
    type: 'record',
    table: 'x_2312287_hrorch_routing_rule',
    operation: 'read',
    roles: [hrAgent, policyAdmin],
    description: 'HR roles can read routing rules',
})
Acl({
    $id: Now.ID['acl_citation_read_roles'],
    type: 'record',
    table: 'x_2312287_hrorch_ai_citation',
    operation: 'read',
    roles: [hrAgent],
    description: 'HR agents can read AI citations',
})
Acl({
    $id: Now.ID['acl_profile_read_roles'],
    type: 'record',
    table: 'x_2312287_hrorch_hr_profile',
    operation: 'read',
    roles: [hrAgent, integration],
    description: 'HR agents and the AI integration user can read HR profiles',
})

// Work notes on task-based tables are restricted by default; the AI reads them to answer @ai in
// context.
Acl({
    $id: Now.ID['acl_case_work_notes_read'],
    type: 'record',
    table: 'x_2312287_hrorch_hr_case',
    field: 'work_notes',
    operation: 'read',
    roles: [hrAgent, integration],
    description: 'HR agents and the AI integration user can read work notes',
})
