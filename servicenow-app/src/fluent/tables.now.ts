// Data model: HR cases, routing rules, AI citations and HR profiles.
import {
    BooleanColumn,
    ChoiceColumn,
    DecimalColumn,
    IntegerColumn,
    MultiLineTextColumn,
    ReferenceColumn,
    StringColumn,
    Table,
} from '@servicenow/sdk/core'
import { hrAgent, integration, policyAdmin } from './roles.now'

// Field names follow the HR Service Delivery case model where one exists, so the
// app can move to sn_hr_core_case on a licensed instance.
export const x_2312287_hrorch_hr_case = Table({
    name: 'x_2312287_hrorch_hr_case',
    label: 'HR Case',
    extends: 'task',
    display: 'number',
    autoNumber: { prefix: 'HRC', number: 1000, numberOfDigits: 7 },
    allowWebServiceAccess: true,
    readRoles: [hrAgent, integration],
    writeRoles: [hrAgent],
    createRoles: [hrAgent],
    deleteRoles: [policyAdmin],
    schema: {
        category: ChoiceColumn({ label: 'Category', choices: { leave: 'Leave', benefits: 'Benefits', payroll: 'Payroll', other: 'Other', unknown: 'Unknown' }, dropdown: 'dropdown_with_none' }),
        topics: StringColumn({ label: 'Topics', maxLength: 200 }),
        severity: ChoiceColumn({ label: 'Severity', choices: { low: 'Low', medium: 'Medium', high: 'High' }, dropdown: 'dropdown_with_none' }),
        routing_rule: ReferenceColumn({ label: 'Routing rule', referenceTable: 'x_2312287_hrorch_routing_rule' }),
        ai_status: ChoiceColumn({
            label: 'AI status',
            choices: { pending: 'Pending', completed: 'Completed', failed: 'Failed', off: 'AI off' },
            default: 'pending',
        }),
        ai_confidence: DecimalColumn({ label: 'AI confidence', scale: 2 }),
        ai_reasoning: MultiLineTextColumn({ label: 'AI reasoning', maxLength: 2000 }),
        ai_suggestion: MultiLineTextColumn({ label: 'AI draft reply', maxLength: 8000 }),
        ai_suggestion_posted: BooleanColumn({ label: 'AI suggestion posted', default: false }),
        ai_proposed_action: ChoiceColumn({
            label: 'AI proposed action',
            choices: { close: 'Close case', approved: 'Approved', rejected: 'Rejected' },
            dropdown: 'dropdown_with_none',
        }),
        ai_proposed_resolution: MultiLineTextColumn({ label: 'AI proposed resolution', maxLength: 2000 }),
        ai_trace_id: StringColumn({ label: 'AI trace ID', maxLength: 40 }),
        ai_model: StringColumn({ label: 'AI model', maxLength: 80 }),
    },
})

// HR edits these rows to change routing. First active match by order wins.
export const x_2312287_hrorch_routing_rule = Table({
    name: 'x_2312287_hrorch_routing_rule',
    label: 'HR Routing Rule',
    display: 'name',
    allowWebServiceAccess: true,
    readRoles: [hrAgent],
    writeRoles: [policyAdmin],
    createRoles: [policyAdmin],
    deleteRoles: [policyAdmin],
    schema: {
        name: StringColumn({ label: 'Name', maxLength: 100, mandatory: true }),
        order: IntegerColumn({ label: 'Order', mandatory: true, default: '100' }),
        active: BooleanColumn({ label: 'Active', default: true }),
        category: ChoiceColumn({ label: 'When category is', choices: { any: 'Any', leave: 'Leave', benefits: 'Benefits', payroll: 'Payroll', other: 'Other', unknown: 'Unknown' }, default: 'any', mandatory: true }),
        severity: ChoiceColumn({ label: 'And severity is', choices: { any: 'Any', low: 'Low', medium: 'Medium', high: 'High' }, default: 'any', mandatory: true }),
        assignment_group: ReferenceColumn({ label: 'Assign to group', referenceTable: 'sys_user_group', mandatory: true }),
        assigned_to: ReferenceColumn({ label: 'Assign to person', referenceTable: 'sys_user' }),
        description: MultiLineTextColumn({ label: 'Description', maxLength: 1000 }),
    },
})

// What the AI relied on, pinned to the article version it saw.
export const x_2312287_hrorch_ai_citation = Table({
    name: 'x_2312287_hrorch_ai_citation',
    label: 'AI Citation',
    display: 'article',
    readRoles: [hrAgent],
    writeRoles: [policyAdmin],
    createRoles: [policyAdmin],
    deleteRoles: [policyAdmin],
    schema: {
        hr_case: ReferenceColumn({ label: 'HR case', referenceTable: 'x_2312287_hrorch_hr_case', mandatory: true }),
        source: ChoiceColumn({ label: 'Source', choices: { triage: 'Triage suggestion', chat: '@ai reply' } }),
        ref_number: IntegerColumn({ label: 'Reference' }),
        article: StringColumn({ label: 'Article', maxLength: 40 }),
        kb_article: ReferenceColumn({ label: 'Knowledge article', referenceTable: 'kb_knowledge' }),
        article_version: IntegerColumn({ label: 'Article version' }),
        section: StringColumn({ label: 'Section', maxLength: 255 }),
        quote: MultiLineTextColumn({ label: 'Quoted text', maxLength: 4000 }),
        chunk_id: StringColumn({ label: 'Chunk ID', maxLength: 100 }),
        start_char: IntegerColumn({ label: 'Start position' }),
        end_char: IntegerColumn({ label: 'End position' }),
        trace_id: StringColumn({ label: 'AI trace ID', maxLength: 40 }),
    },
})

// Employee attributes the AI uses to pick country-specific policies.
// Kept in a scoped table rather than new columns on sys_user, so platform tables stay untouched.
export const x_2312287_hrorch_hr_profile = Table({
    name: 'x_2312287_hrorch_hr_profile',
    label: 'HR Profile',
    display: 'user',
    readRoles: [hrAgent, integration],
    writeRoles: [policyAdmin],
    createRoles: [policyAdmin],
    deleteRoles: [policyAdmin],
    schema: {
        user: ReferenceColumn({ label: 'Employee', referenceTable: 'sys_user', mandatory: true }),
        country: ChoiceColumn({
            label: 'Country',
            choices: { US: 'United States', DE: 'Germany', IN: 'India', GB: 'United Kingdom' },
            dropdown: 'dropdown_with_none',
        }),
        employee_type: ChoiceColumn({
            label: 'Employee type',
            choices: { full_time: 'Full-time', part_time: 'Part-time' },
            dropdown: 'dropdown_with_none',
        }),
    },
})
