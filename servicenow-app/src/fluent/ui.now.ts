// User interface: navigator menu, HR case form layout and the employee portal form.
import {
    ApplicationMenu,
    CatalogItemRecordProducer,
    Form,
    MultiLineTextVariable,
    Record,
    SingleLineTextVariable,
    default_view,
} from '@servicenow/sdk/core'
import { hrAgent } from './roles.now'

// ---- navigator ------------------------------------------------------------------

const menu = ApplicationMenu({
    $id: Now.ID['menu'],
    title: 'HR Case Orchestration',
    hint: 'Policy-driven HR cases with AI assistance',
    roles: [hrAgent, 'admin'],
    active: true,
})

Record({
    $id: Now.ID['mod_open'],
    table: 'sys_app_module',
    data: {
        title: 'Open HR Cases',
        application: menu,
        link_type: 'LIST',
        name: 'x_2312287_hrorch_hr_case',
        filter: 'active=true^ORDERBYDESCsys_created_on',
        active: true,
        order: 100,
    },
})
Record({
    $id: Now.ID['mod_all'],
    table: 'sys_app_module',
    data: {
        title: 'All HR Cases',
        application: menu,
        link_type: 'LIST',
        name: 'x_2312287_hrorch_hr_case',
        filter: 'ORDERBYDESCsys_created_on',
        active: true,
        order: 110,
    },
})
Record({
    $id: Now.ID['mod_rules'],
    table: 'sys_app_module',
    data: {
        title: 'Routing Rules',
        application: menu,
        link_type: 'LIST',
        name: 'x_2312287_hrorch_routing_rule',
        filter: 'ORDERBYorder',
        active: true,
        order: 200,
    },
})
Record({
    $id: Now.ID['mod_cites'],
    table: 'sys_app_module',
    data: {
        title: 'AI Citations',
        application: menu,
        link_type: 'LIST',
        name: 'x_2312287_hrorch_ai_citation',
        filter: 'ORDERBYDESCsys_created_on',
        active: true,
        order: 300,
    },
})
Record({
    $id: Now.ID['mod_props'],
    table: 'sys_app_module',
    data: {
        title: 'Settings',
        application: menu,
        link_type: 'LIST',
        name: 'sys_properties',
        filter: 'nameSTARTSWITHx_2312287_hrorch^ORnameSTARTSWITHhr_orchestration',
        roles: ['admin'],
        active: true,
        order: 400,
    },
})

// ---- case form --------------------------------------------------------------------

Form({
    table: 'x_2312287_hrorch_hr_case',
    view: default_view,
    sections: [
        {
            caption: 'HR Case',
            content: [
                {
                    layout: 'two-column',
                    leftElements: [
                        { field: 'number', type: 'table_field' },
                        { field: 'opened_by', type: 'table_field' },
                        { field: 'category', type: 'table_field' },
                        { field: 'topics', type: 'table_field' },
                        { field: 'severity', type: 'table_field' },
                    ],
                    rightElements: [
                        { field: 'state', type: 'table_field' },
                        { field: 'priority', type: 'table_field' },
                        { field: 'assignment_group', type: 'table_field' },
                        { field: 'assigned_to', type: 'table_field' },
                        { field: 'routing_rule', type: 'table_field' },
                    ],
                },
                {
                    layout: 'one-column',
                    elements: [
                        { field: 'short_description', type: 'table_field' },
                        { field: 'description', type: 'table_field' },
                        { field: 'comments', type: 'table_field' },
                        { field: 'work_notes', type: 'table_field' },
                        { type: 'formatter', formatterRef: 'Activities_Filtered' },
                    ],
                },
            ],
        },
        {
            caption: 'AI assistant',
            content: [
                {
                    layout: 'two-column',
                    leftElements: [
                        { field: 'ai_status', type: 'table_field' },
                        { field: 'ai_confidence', type: 'table_field' },
                        { field: 'ai_suggestion_posted', type: 'table_field' },
                        { field: 'ai_model', type: 'table_field' },
                    ],
                    rightElements: [
                        { field: 'ai_proposed_action', type: 'table_field' },
                        { field: 'ai_proposal_state', type: 'table_field' },
                        { field: 'ai_trace_id', type: 'table_field' },
                        { field: 'close_notes', type: 'table_field' },
                    ],
                },
                {
                    layout: 'one-column',
                    elements: [
                        { field: 'ai_reasoning', type: 'table_field' },
                        { field: 'ai_suggestion', type: 'table_field' },
                        { field: 'ai_proposed_resolution', type: 'table_field' },
                        {
                            type: 'list',
                            listType: '12M',
                            listRef: 'x_2312287_hrorch_ai_citation.hr_case',
                        },
                    ],
                },
            ],
        },
    ],
})

// ---- employee self-service ----------------------------------------------------------

export const submitHrCase = CatalogItemRecordProducer({
    $id: Now.ID['rp_submit_hr_case'],
    name: 'Submit an HR case',
    shortDescription: 'Ask HR about leave, benefits, payroll or anything else',
    description:
        'Describe your question. An AI assistant may reply with the policy; HR reviews every case.',
    table: 'x_2312287_hrorch_hr_case',
    catalogs: ['e0d08b13c3330100c8b837659bba8fb4'],
    categories: ['e15706fc0a0a0aa7007fc21e1ab70c2f'],
    availability: 'both',
    variables: {
        case_title: SingleLineTextVariable({
            question: 'What do you need help with?',
            order: 100,
            mandatory: true,
        }),
        case_details: MultiLineTextVariable({ question: 'Details', order: 200, mandatory: true }),
    },
    script: `current.short_description = producer.case_title;
current.description = producer.case_details;
current.opened_by = gs.getUserID();
current.contact_type = 'self-service';`,
})
