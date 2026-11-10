// Roles: HR agent, policy admin (owns routing rules) and the read-only AI integration role.
import { Role } from '@servicenow/sdk/core'

// Works HR cases, sees AI suggestions and approves AI-proposed closures.
export const hrAgent = Role({
    $id: Now.ID['role_hr_agent'],
    name: 'x_2312287_hrorch.hr_agent',
    description: 'HR agent: works HR cases and approves AI-proposed actions',
})

// Owns routing rules.
export const policyAdmin = Role({
    $id: Now.ID['role_policy_admin'],
    name: 'x_2312287_hrorch.policy_admin',
    description: 'Policy admin: maintains HR routing rules',
    containsRoles: [hrAgent],
})

// Read-only role for the AI agent service's integration user.
export const integration = Role({
    $id: Now.ID['role_integration'],
    name: 'x_2312287_hrorch.integration',
    description: 'AI agent service: read-only access to HR cases and policy articles',
})
