// Reference data shipped with the app: HR teams, synthetic people, HR profiles and roles.
import { Record } from '@servicenow/sdk/core'
import { hrAgent, integration, policyAdmin } from './roles.now'

// ---- HR teams ---------------------------------------------------------------------

export const groupLeave = Record({
    $id: Now.ID['group_leave'],
    table: 'sys_user_group',
    data: {
        name: 'HR Leave',
        description: 'Parental, annual, sick and bereavement leave',
        active: true,
    },
})
export const groupBenefits = Record({
    $id: Now.ID['group_benefits'],
    table: 'sys_user_group',
    data: {
        name: 'HR Benefits',
        description: 'Health insurance, retirement, enrollment and wellbeing',
        active: true,
    },
})
export const groupPayroll = Record({
    $id: Now.ID['group_payroll'],
    table: 'sys_user_group',
    data: {
        name: 'HR Payroll',
        description: 'Pay, payslips, corrections, overtime and expenses',
        active: true,
    },
})
export const groupManual = Record({
    $id: Now.ID['group_manual'],
    table: 'sys_user_group',
    data: {
        name: 'HR Manual Triage',
        description: 'Cases the routing rules or the AI could not place',
        active: true,
    },
})

// ---- people (synthetic) -------------------------------------------------------------

export const hanaWeber = Record({
    $id: Now.ID['user_hana'],
    table: 'sys_user',
    data: {
        user_name: 'hana.weber',
        first_name: 'Hana',
        last_name: 'Weber',
        email: 'hana.weber@example.com',
        title: 'Leave lead',
        active: true,
    },
})
export const benCarter = Record({
    $id: Now.ID['user_ben'],
    table: 'sys_user',
    data: {
        user_name: 'ben.carter',
        first_name: 'Ben',
        last_name: 'Carter',
        email: 'ben.carter@example.com',
        title: 'Benefits lead',
        active: true,
    },
})
export const priyaNair = Record({
    $id: Now.ID['user_priya'],
    table: 'sys_user',
    data: {
        user_name: 'priya.nair',
        first_name: 'Priya',
        last_name: 'Nair',
        email: 'priya.nair@example.com',
        title: 'Payroll lead',
        active: true,
    },
})
export const samOrtiz = Record({
    $id: Now.ID['user_sam'],
    table: 'sys_user',
    data: {
        user_name: 'sam.ortiz',
        first_name: 'Sam',
        last_name: 'Ortiz',
        email: 'sam.ortiz@example.com',
        title: 'HR operations manager',
        active: true,
    },
})

export const anna = Record({
    $id: Now.ID['user_anna'],
    table: 'sys_user',
    data: {
        user_name: 'anna.schmidt',
        first_name: 'Anna',
        last_name: 'Schmidt',
        email: 'anna.schmidt@example.com',
        active: true,
    },
})
export const john = Record({
    $id: Now.ID['user_john'],
    table: 'sys_user',
    data: {
        user_name: 'john.miller',
        first_name: 'John',
        last_name: 'Miller',
        email: 'john.miller@example.com',
        active: true,
    },
})
export const aarav = Record({
    $id: Now.ID['user_aarav'],
    table: 'sys_user',
    data: {
        user_name: 'aarav.sharma',
        first_name: 'Aarav',
        last_name: 'Sharma',
        email: 'aarav.sharma@example.com',
        active: true,
    },
})
export const olivia = Record({
    $id: Now.ID['user_olivia'],
    table: 'sys_user',
    data: {
        user_name: 'olivia.brown',
        first_name: 'Olivia',
        last_name: 'Brown',
        email: 'olivia.brown@example.com',
        active: true,
    },
})

// HR profiles drive country-specific policy search.
Record({
    $id: Now.ID['profile_anna'],
    table: 'x_2312287_hrorch_hr_profile',
    data: { user: anna, country: 'DE', employee_type: 'full_time' },
})
Record({
    $id: Now.ID['profile_john'],
    table: 'x_2312287_hrorch_hr_profile',
    data: { user: john, country: 'US', employee_type: 'full_time' },
})
Record({
    $id: Now.ID['profile_aarav'],
    table: 'x_2312287_hrorch_hr_profile',
    data: { user: aarav, country: 'IN', employee_type: 'full_time' },
})
Record({
    $id: Now.ID['profile_olivia'],
    table: 'x_2312287_hrorch_hr_profile',
    data: { user: olivia, country: 'GB', employee_type: 'part_time' },
})

// Read-only account the AI agent service uses. Set its password on the instance.
export const integrationUser = Record({
    $id: Now.ID['user_integration'],
    table: 'sys_user',
    data: {
        user_name: 'hr_ai_integration',
        first_name: 'HR AI',
        last_name: 'Integration',
        web_service_access_only: true,
        active: true,
    },
})

// ---- memberships and roles ------------------------------------------------------------

Record({
    $id: Now.ID['gm_hana'],
    table: 'sys_user_grmember',
    data: { group: groupLeave, user: hanaWeber },
})
Record({
    $id: Now.ID['gm_ben'],
    table: 'sys_user_grmember',
    data: { group: groupBenefits, user: benCarter },
})
Record({
    $id: Now.ID['gm_priya'],
    table: 'sys_user_grmember',
    data: { group: groupPayroll, user: priyaNair },
})
Record({
    $id: Now.ID['gm_sam'],
    table: 'sys_user_grmember',
    data: { group: groupManual, user: samOrtiz },
})

Record({
    $id: Now.ID['ur_hana'],
    table: 'sys_user_has_role',
    data: { user: hanaWeber, role: hrAgent },
})
Record({
    $id: Now.ID['ur_ben'],
    table: 'sys_user_has_role',
    data: { user: benCarter, role: hrAgent },
})
Record({
    $id: Now.ID['ur_priya'],
    table: 'sys_user_has_role',
    data: { user: priyaNair, role: hrAgent },
})
Record({
    $id: Now.ID['ur_sam'],
    table: 'sys_user_has_role',
    data: { user: samOrtiz, role: policyAdmin },
})
Record({
    $id: Now.ID['ur_integration'],
    table: 'sys_user_has_role',
    data: { user: integrationUser, role: integration },
})

// Routing rules and HR policy articles are owned by HR in the ServiceNow UI, so they are not part
// of this package; a redeploy would overwrite UI edits. scripts/seed-hr-data.js creates the
// starting set once and never changes existing records.
