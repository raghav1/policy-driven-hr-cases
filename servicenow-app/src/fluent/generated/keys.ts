import '@servicenow/sdk/global'

declare global {
    namespace Now {
        namespace Internal {
            interface Keys extends KeysRegistry {
                explicit: {
                    acl_case_read_own: {
                        table: 'sys_security_acl'
                        id: 'a1fb00d6264643eb8afe7a646f0e070a'
                    }
                    acl_case_read_roles: {
                        table: 'sys_security_acl'
                        id: '8fc5d732415b4fe3a1143bf0017586a9'
                    }
                    acl_case_work_notes_read: {
                        table: 'sys_security_acl'
                        id: 'd8f6546105b54e2387f7da218f7cc5d5'
                    }
                    acl_citation_read_roles: {
                        table: 'sys_security_acl'
                        id: '3eeb5e7c6ac44059960ae5a52396bd68'
                    }
                    acl_kb_read_integration: {
                        table: 'sys_security_acl'
                        id: '9457f9464bcd477b826f392305c7704a'
                    }
                    acl_profile_read_roles: {
                        table: 'sys_security_acl'
                        id: '72a6a2c58e9a4f1aaed57a128a348549'
                    }
                    acl_rule_read_roles: {
                        table: 'sys_security_acl'
                        id: 'd3e2042b4bf04e99a9922a57062b71c4'
                    }
                    bom_json: {
                        table: 'sys_module'
                        id: 'fef7e30e91fd44eaa9704d09a61e9e60'
                    }
                    br_kb_changed: {
                        table: 'sys_script'
                        id: '70e746ea00bc4bbb8bac5dc6ad6a3f7f'
                    }
                    br_mention: {
                        table: 'sys_script'
                        id: 'ae1c9cafcbdf4412b50c9c6555448336'
                    }
                    br_triage: {
                        table: 'sys_script'
                        id: '15cf4573eba64288aa9ce55f351781b7'
                    }
                    event_ai_mention: {
                        table: 'sysevent_register'
                        id: 'f2b919ae255f48f0ba23f25d2c86e2fa'
                    }
                    event_kb_changed: {
                        table: 'sysevent_register'
                        id: 'ee7b841216aa4bddab1b871ccae03715'
                    }
                    event_triage: {
                        table: 'sysevent_register'
                        id: '1869810fee2044f480b9b6d503c92d16'
                    }
                    gm_ben: {
                        table: 'sys_user_grmember'
                        id: '1227dadc5bcf441bb91eb87932183be0'
                    }
                    gm_hana: {
                        table: 'sys_user_grmember'
                        id: '6227925f3d1849088693dbc87c90a807'
                    }
                    gm_priya: {
                        table: 'sys_user_grmember'
                        id: '3ba4209581d64072a3c1f16ed43b7bf3'
                    }
                    gm_sam: {
                        table: 'sys_user_grmember'
                        id: '45965b239a7a4e5b89c4913eaf0649d1'
                    }
                    group_benefits: {
                        table: 'sys_user_group'
                        id: 'eb23e238532a43d88cc5f61380d0b084'
                    }
                    group_leave: {
                        table: 'sys_user_group'
                        id: 'fe58e364367b49838d6be399954ff859'
                    }
                    group_manual: {
                        table: 'sys_user_group'
                        id: '06c1cf98e3734cf7a918d907f7fe2c45'
                    }
                    group_payroll: {
                        table: 'sys_user_group'
                        id: '47a3aed40b0147769613d9a910ba1e24'
                    }
                    kb_hr_policies: {
                        table: 'kb_knowledge_base'
                        id: '84c62f821ef04a88a3c1be472f655efa'
                        deleted: true
                    }
                    kb_KB0090001: {
                        table: 'kb_knowledge'
                        id: '00d8c5fb8c824853a4a9b1f303ed6db6'
                        deleted: true
                    }
                    kb_KB0090002: {
                        table: 'kb_knowledge'
                        id: '0cab520b5a65430ca481544cc45c3852'
                        deleted: true
                    }
                    kb_KB0090003: {
                        table: 'kb_knowledge'
                        id: '9e17fedd994d4944a980c9a71aad18b8'
                        deleted: true
                    }
                    kb_KB0090004: {
                        table: 'kb_knowledge'
                        id: 'ccfb10c8140c4feca15ffed4db9d2ba5'
                        deleted: true
                    }
                    kb_KB0090005: {
                        table: 'kb_knowledge'
                        id: '10359691f7f145e9af0e98123f56ccec'
                        deleted: true
                    }
                    kb_KB0090006: {
                        table: 'kb_knowledge'
                        id: '7b42ba41d19f4ce6830878319ed9ddef'
                        deleted: true
                    }
                    kb_KB0090007: {
                        table: 'kb_knowledge'
                        id: 'ecef8fa25da54d3a87d64cd2833c03db'
                        deleted: true
                    }
                    kb_KB0090008: {
                        table: 'kb_knowledge'
                        id: 'df4083699fb640568cf5730e21e94776'
                        deleted: true
                    }
                    kb_KB0090009: {
                        table: 'kb_knowledge'
                        id: '38892bf75dae4bf09ec93f197f1029e4'
                        deleted: true
                    }
                    kb_KB0090010: {
                        table: 'kb_knowledge'
                        id: 'bf29ea0743d0445fb00a1b5bb5da8a57'
                        deleted: true
                    }
                    kb_KB0090011: {
                        table: 'kb_knowledge'
                        id: '9e369b98061c4aaa8ad930c64b118868'
                        deleted: true
                    }
                    kb_KB0090012: {
                        table: 'kb_knowledge'
                        id: '8458f9d6c9ad4013893fde2c7e1a4cd5'
                        deleted: true
                    }
                    kb_KB0090013: {
                        table: 'kb_knowledge'
                        id: '066d07f951464b9b975a4542f7c7b598'
                        deleted: true
                    }
                    kb_KB0090014: {
                        table: 'kb_knowledge'
                        id: '429e773a49684838a52f8387e8a46678'
                        deleted: true
                    }
                    kb_KB0090015: {
                        table: 'kb_knowledge'
                        id: '7be08fa893394d0f9e7f4c5316ccff80'
                        deleted: true
                    }
                    kb_KB0090016: {
                        table: 'kb_knowledge'
                        id: '2586dbf4842141f4bd12aad2ac3609c3'
                        deleted: true
                    }
                    kb_KB0090017: {
                        table: 'kb_knowledge'
                        id: '2b377443261a443ea3f44e0aa184e8be'
                        deleted: true
                    }
                    kb_KB0090018: {
                        table: 'kb_knowledge'
                        id: '4c7dace8822241acb423d563c06f853a'
                        deleted: true
                    }
                    kb_KB0090019: {
                        table: 'kb_knowledge'
                        id: 'b9ae3d29fdfd4ca496d087aab9b2487f'
                        deleted: true
                    }
                    kb_KB0090020: {
                        table: 'kb_knowledge'
                        id: '73e711de68c74b968e46123e3d87e06b'
                        deleted: true
                    }
                    kb_KB0090021: {
                        table: 'kb_knowledge'
                        id: '10f48f1711c648bfb96b797c23d66afb'
                        deleted: true
                    }
                    kb_KB0090022: {
                        table: 'kb_knowledge'
                        id: '61f67ecdd3f741daa372aaafb5cc0048'
                        deleted: true
                    }
                    kb_KB0090023: {
                        table: 'kb_knowledge'
                        id: '3ba05b447f4346e59d7d02bc2f62f735'
                        deleted: true
                    }
                    kb_KB0090024: {
                        table: 'kb_knowledge'
                        id: 'c729a29dbf074596be6dbbd4b9241a57'
                        deleted: true
                    }
                    kb_KB0090025: {
                        table: 'kb_knowledge'
                        id: 'c39736524f2d468799f1e4c71b92c1eb'
                        deleted: true
                    }
                    kb_KB0090026: {
                        table: 'kb_knowledge'
                        id: 'f42a21305ba1410db4ea607beb3a0382'
                        deleted: true
                    }
                    kb_KB0090027: {
                        table: 'kb_knowledge'
                        id: '211f73e57b564982bfed91920dbc6519'
                        deleted: true
                    }
                    kb_KB0090028: {
                        table: 'kb_knowledge'
                        id: '037fa6be4b374ff79456499d3234e7c6'
                        deleted: true
                    }
                    kb_KB0090029: {
                        table: 'kb_knowledge'
                        id: 'aa0fc8ab74b2410da939112e346f0b02'
                        deleted: true
                    }
                    kb_KB0090030: {
                        table: 'kb_knowledge'
                        id: '5b526c1ee94341f6be7866493e38d90c'
                        deleted: true
                    }
                    kb_KB0090031: {
                        table: 'kb_knowledge'
                        id: '2e38487a858c4748bc607491ef31c76a'
                        deleted: true
                    }
                    kb_KB0090032: {
                        table: 'kb_knowledge'
                        id: 'a1a38e8cc54f4f72a07a2a2abf9eabd5'
                        deleted: true
                    }
                    kb_KB0090033: {
                        table: 'kb_knowledge'
                        id: 'ef455752a34d45b2b4794943728f0b05'
                        deleted: true
                    }
                    kb_KB0090034: {
                        table: 'kb_knowledge'
                        id: '0933312c3c464b2ca55e376c5c6c7695'
                        deleted: true
                    }
                    kb_KB0090035: {
                        table: 'kb_knowledge'
                        id: '913f096780b0481bbb0a63850e627444'
                        deleted: true
                    }
                    kb_KB0090036: {
                        table: 'kb_knowledge'
                        id: 'a1785b785c9c4f0d9f2c007daa265fc3'
                        deleted: true
                    }
                    kb_KB0090037: {
                        table: 'kb_knowledge'
                        id: 'd6e5e7519ecf409aa8ade699ce86594b'
                        deleted: true
                    }
                    kb_KB0090038: {
                        table: 'kb_knowledge'
                        id: 'b5fb195d9f024a169b13ffc05a088e8d'
                        deleted: true
                    }
                    kb_KB0090039: {
                        table: 'kb_knowledge'
                        id: 'a2a364062ed249559fce54c6e96d4e40'
                        deleted: true
                    }
                    kb_KB0090040: {
                        table: 'kb_knowledge'
                        id: '4bf5287473654c94ba7ae327eb15bacc'
                        deleted: true
                    }
                    kb_KB0090041: {
                        table: 'kb_knowledge'
                        id: 'd3e4b3e0d65b4986bc0f90a7b154d43b'
                        deleted: true
                    }
                    kb_KB0090042: {
                        table: 'kb_knowledge'
                        id: '39774c99f8ab41199e28e8a4ec55586b'
                        deleted: true
                    }
                    kb_KB0090043: {
                        table: 'kb_knowledge'
                        id: 'f864a3b3a3dd4c99b2f3e13c08e21fce'
                        deleted: true
                    }
                    kb_KB0090044: {
                        table: 'kb_knowledge'
                        id: 'a644cd9c8f1e40d08cfe6646ccc440d0'
                        deleted: true
                    }
                    kb_KB0090045: {
                        table: 'kb_knowledge'
                        id: '77d918d03ed145f9b4d221dc34bfbe99'
                        deleted: true
                    }
                    kb_KB0090046: {
                        table: 'kb_knowledge'
                        id: '1294514c706d450d8cde2297023f3081'
                        deleted: true
                    }
                    kb_KB0090047: {
                        table: 'kb_knowledge'
                        id: 'cb7b3f805ecd4e3486649b53eb9186a3'
                        deleted: true
                    }
                    kb_KB0090048: {
                        table: 'kb_knowledge'
                        id: '376c9d1907814d95a5b29866eb4b5efd'
                        deleted: true
                    }
                    kb_KB0090049: {
                        table: 'kb_knowledge'
                        id: 'afe36c508cac444f8614b22a0baf8e98'
                        deleted: true
                    }
                    kb_KB0090050: {
                        table: 'kb_knowledge'
                        id: '5e072af6c0764fd89b68594804580c84'
                        deleted: true
                    }
                    kb_KB0090051: {
                        table: 'kb_knowledge'
                        id: '392efa1e69024da5a36f6cf037c71033'
                        deleted: true
                    }
                    menu: {
                        table: 'sys_app_application'
                        id: '02f96a404382416bb8d2926147715ff7'
                    }
                    mod_all: {
                        table: 'sys_app_module'
                        id: '99ef2ef7617645d5a4ce449ccf70992c'
                    }
                    mod_cites: {
                        table: 'sys_app_module'
                        id: '59f2d5bac5b54b82b3f5d34c2b2d5e05'
                    }
                    mod_open: {
                        table: 'sys_app_module'
                        id: '56f9c35743a648d3b72468527178c9fc'
                    }
                    mod_props: {
                        table: 'sys_app_module'
                        id: 'ffae736b23294cfdbe1e1237e2fda612'
                    }
                    mod_rules: {
                        table: 'sys_app_module'
                        id: '524768527f1f485e91b7c05afb8359c6'
                    }
                    package_json: {
                        table: 'sys_module'
                        id: 'f95914be1bfa42c08322974dfccd82ed'
                    }
                    profile_aarav: {
                        table: 'x_2312287_hrorch_hr_profile'
                        id: '260ddcfa3d2d4c9eab5e79b95a371d02'
                    }
                    profile_anna: {
                        table: 'x_2312287_hrorch_hr_profile'
                        id: 'a9481d85163043c6a722b38f422be86a'
                    }
                    profile_john: {
                        table: 'x_2312287_hrorch_hr_profile'
                        id: '32108c5eb95441eca0de50da5b2a0486'
                    }
                    profile_olivia: {
                        table: 'x_2312287_hrorch_hr_profile'
                        id: 'dd0a6cbb232e42b8ba25176b36297297'
                    }
                    prop_api_key: {
                        table: 'sys_properties'
                        id: '12605cf926eb42cfb82a584a33fdf80e'
                        deleted: true
                    }
                    prop_base_url: {
                        table: 'sys_properties'
                        id: 'f08fc7ea43304ded8e50f59d151f31ed'
                        deleted: true
                    }
                    prop_enabled: {
                        table: 'sys_properties'
                        id: '9d6cfe0198eb45c9b23ca57d01cd0ad3'
                    }
                    prop_threshold: {
                        table: 'sys_properties'
                        id: 'c15a2ac829584d96b902c5dc93082009'
                    }
                    prop_timeout: {
                        table: 'sys_properties'
                        id: 'cd668911017e478d8ed4690a5ad30fda'
                    }
                    rp_submit_hr_case: {
                        table: 'sc_cat_item_producer'
                        id: '4993ecfc0fa44c2eb7e404f56391fe5d'
                    }
                    rule_benefits: {
                        table: 'x_2312287_hrorch_routing_rule'
                        id: 'a846d005290345e3ad67597eb883015d'
                        deleted: true
                    }
                    rule_default: {
                        table: 'x_2312287_hrorch_routing_rule'
                        id: 'e8050c35f6df49baa61e297835b53b2b'
                        deleted: true
                    }
                    rule_leave: {
                        table: 'x_2312287_hrorch_routing_rule'
                        id: '2f41b0aabdcc4ae3852c6987b4b6191a'
                        deleted: true
                    }
                    rule_payroll: {
                        table: 'x_2312287_hrorch_routing_rule'
                        id: '9f85078f1c484b149d2fd7fe706d94d6'
                        deleted: true
                    }
                    rule_payroll_high: {
                        table: 'x_2312287_hrorch_routing_rule'
                        id: 'c4775e503eca4d83846f6486bac8a881'
                        deleted: true
                    }
                    sa_ai_mention: {
                        table: 'sysevent_script_action'
                        id: 'b4a1b6e6c5734c1b8bc19a9be8a5801b'
                    }
                    sa_kb_changed: {
                        table: 'sysevent_script_action'
                        id: '49a644dbe2fa4a1699214b39b9c56981'
                    }
                    sa_triage: {
                        table: 'sysevent_script_action'
                        id: 'df291d955db4446abddd8a453c10643f'
                    }
                    si_agent_client: {
                        table: 'sys_script_include'
                        id: '83d2aac60e2c44eca9d7a1b5fafea3de'
                    }
                    si_case_orchestrator: {
                        table: 'sys_script_include'
                        id: 'ec7cddabdec1499b9407be0837a1d76e'
                    }
                    si_routing_engine: {
                        table: 'sys_script_include'
                        id: 'cca341908eea48f1a0726e478c8b8fb1'
                    }
                    'src_server_script-includes_AgentClient_server_js': {
                        table: 'sys_module'
                        id: '60e11e16f1bc4bdd938d7b0e00a78db2'
                    }
                    'src_server_script-includes_CaseOrchestrator_server_js': {
                        table: 'sys_module'
                        id: '5ee7a5f412db47478ef3c4a7fc75dbcb'
                    }
                    'src_server_script-includes_RoutingEngine_server_js': {
                        table: 'sys_module'
                        id: '43d99ab69ce34d07a553a488748e04a1'
                    }
                    ua_approve_close: {
                        table: 'sys_ui_action'
                        id: 'b618199413fe4882b0da4f28278ca816'
                    }
                    ua_reject_close: {
                        table: 'sys_ui_action'
                        id: 'bf2420f20d1e4f6fa5088d8f31702762'
                    }
                    ua_rerun_triage: {
                        table: 'sys_ui_action'
                        id: '40b9bbfd9e7c4ecab2635d8cda2d6bb5'
                    }
                    ur_ben: {
                        table: 'sys_user_has_role'
                        id: '444693602ce0430e9cf55635264ae308'
                    }
                    ur_hana: {
                        table: 'sys_user_has_role'
                        id: '303787892e054fa285b6ae9dab6d5a86'
                    }
                    ur_integration: {
                        table: 'sys_user_has_role'
                        id: '93643374f4734e1984159dbcbede6824'
                    }
                    ur_priya: {
                        table: 'sys_user_has_role'
                        id: '24e987467b6749e19c6d14d93a16c452'
                    }
                    ur_sam: {
                        table: 'sys_user_has_role'
                        id: 'bf3d6c82a5f54ea586da82619e75bf95'
                    }
                    user_aarav: {
                        table: 'sys_user'
                        id: '0857bc6d6a8948a2a8ae6bd5afb0f66a'
                    }
                    user_anna: {
                        table: 'sys_user'
                        id: 'eab99da74d904065bd5ea760f3bf3da9'
                    }
                    user_ben: {
                        table: 'sys_user'
                        id: '795f65e101a54ba4a67764696740d349'
                    }
                    user_hana: {
                        table: 'sys_user'
                        id: '2a58f1eb455f48a6a121be7389e63750'
                    }
                    user_integration: {
                        table: 'sys_user'
                        id: '73e7de62a4f64f2ab2d64c6667c1d0ac'
                    }
                    user_john: {
                        table: 'sys_user'
                        id: 'eea0931bed1e426e835b96b927f15ddf'
                    }
                    user_olivia: {
                        table: 'sys_user'
                        id: 'a6fccd8a34f24c0e9400924b0946950e'
                    }
                    user_priya: {
                        table: 'sys_user'
                        id: 'ee7b288cd64a403282508bc3fced0268'
                    }
                    user_sam: {
                        table: 'sys_user'
                        id: 'eed96db1238846cdaeacd967f0a4ee9d'
                    }
                }
                composite: [
                    {
                        table: 'sys_dictionary'
                        id: '00bafd3b886b4cb1a102a27945cda79e'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'article_version'
                        }
                    },
                    {
                        table: 'sys_db_object'
                        id: '059fce99cf884e97a70342c1a0eb329e'
                        deleted: true
                        key: {
                            name: 'sys_user'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '062e027905124f0ab4b3f291a3a63642'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            value: 'benefits'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '093d5f55f0904c0ca821809f2a3546ee'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                            value: 'leave'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '09a57d09c8254ce9867da7718e7f0227'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'kb_article'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '0a4b5cf503e249a6b9702213da5706d5'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_resolution'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '0b32424897bc4ee28d2804604faab566'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'assigned_to'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '0cb97846892a4344a56f4bcdfc77ee1c'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'name'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '0f78c47b86194f24ac66a47cf32a0b56'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'close_notes'
                            position: '9'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '12375987908849ed83d560bfea9e28a9'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_employee_type'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '128e323642cd4f479173925312aec2c5'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_action'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '12a84473bbcf484d9289277a3779a237'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.end_split'
                            position: '9'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '130e2f8bb82645949068a771c4448b1e'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'CA'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '145f7a0b67dc4e16aab5fc6a2b90e367'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_confidence'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '14dd1bdcb345469b88be0863bc673447'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                            value: 'payroll'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '14e27012364b459b8da23db458ac3974'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'order'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '15fb6558338440a19689443a9c7c29d5'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '16e44203326a46b6a24397e8bcaaff97'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'priority'
                            position: '8'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '17b06c1fa1ec46d48f60871c0f6549a3'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'active'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '17c00ec1e3d447a5b62ad5ef9e9d80da'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'NL'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '1949a7e3c24146cdb1c3d3290bd00dd4'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'employee_type'
                            value: 'full_time'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '197fcd6ec0a8469ab77f06b692459153'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '1b528ba4e6ff417cae3ee3272b5e29e6'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'assignment_group'
                        }
                    },
                    {
                        table: 'sys_ui_form_section'
                        id: '1c5e7ea361fe4719b22c888e7af4a60a'
                        key: {
                            sys_ui_form: {
                                id: '7ecc96ceb3f44094af70ef361c51acfe'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '1f105994179e4eeeacf9b23f6c9c2420'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'NULL'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '1fd62aa9b1b6460180ec2208f716df2e'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                            value: 'IN'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '20fdf0ff7148426fa53e9f865c9b41c4'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'user'
                        }
                    },
                    {
                        table: 'ua_table_licensing_config'
                        id: '214587874cf6488b8f1b2e1f1fdc928f'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '21ff4df636a84b3ea199e30ea0c4a820'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            value: 'other'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '24d1b86c866c4c8c9d5c04b4764db41b'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'topics'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '25156a8a456e47f5a1fc4af795069a13'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'employee_type'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '252ca1b6b9f2483c8c17146d6cf5a372'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '2643a7691d1d4e6c9b3040eb569d4b99'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                            value: 'GB'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '26929af31cae4c10bfbadb3ddccf201f'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '2818ac653a384f5ea975fecb5982383f'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_action_role'
                        id: '2bd7d021b11f4ff5a8d87e34c44051cb'
                        key: {
                            sys_ui_action: '40b9bbfd9e7c4ecab2635d8cda2d6bb5'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '2c1bee3871f443569dca9b7f70a9deaa'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'description'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '2ce0c951c41d47eebd156d87181f1bdd'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_employee_type'
                            value: 'part_time'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '2d8fee632a6541f6a22546f7fc07496a'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_suggestion_posted'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '2de3fb8088844f53a19cb07d97f1c521'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                            value: 'low'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '2edbc5046edb400296e5968a3f8ce636'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'severity'
                            position: '5'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '2f64a7227202478d8598924b66036b57'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'routing_rule'
                            position: '11'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '2fa447215b9f4cad8195e8ccbe65aa2a'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'end_char'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '30d6d8c301be4c7abecb883544896b8c'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'assigned_to'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '3197549a907947699965829ee0751f17'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'FR'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '32c97a8818ad41518e71082df07c6f32'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '3546e50b67f943f0b46db87823609dfd'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'trace_id'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '356f1bf3f54b43b6aeac9215999f701c'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'comments'
                            position: '15'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '362663be38b04e7d9358ae585425338e'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'DE'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '399a99466cb14d15938e5ec755ddce7b'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                            value: 'failed'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '3bcda955bae243b081eb2e548863f09d'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'severity'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '3d4d80a771df4195a7b9c35dde16dc12'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'article'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '3ecf321c8507465188bff28a4a036816'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'opened_by'
                            position: '2'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '3f06be84b2454d818968825b51542124'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'NULL'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: '3f2149343740420e8c9c3c1be8b6e014'
                        key: {
                            sys_security_acl: '3eeb5e7c6ac44059960ae5a52396bd68'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '3f33e3354aae4de8954cbc698be04a06'
                        deleted: true
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_action'
                            value: 'approved'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '3f455cfd40a8486eadf85659abee3df9'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '3fe1d52f785a4a3ea2a72c0990c80040'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_suggestion_posted'
                            position: '3'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '403f04f0fed943029e051b4011948785'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'NULL'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '4249aa85fe394e1e916b007aced26e80'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                        }
                    },
                    {
                        table: 'sys_db_object'
                        id: '42a26c67f0e74bbda5433844f823cdcf'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                        }
                    },
                    {
                        table: 'sys_user_role'
                        id: '4622e5f94ef3413590556d3b0bca914a'
                        key: {
                            name: 'x_2312287_hrorch.hr_agent'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '47a372b5a90e4c198cbacada77e36e91'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'name'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '487d48ff4c534b5d82428b38b13450b1'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_suggestion'
                            position: '11'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '48d4cf1f7ec0489797ee5b18cffd9e28'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                        }
                    },
                    {
                        table: 'sys_ui_section'
                        id: '4b4c0c94eb1d45b09a756b612900195a'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            caption: 'HR Case'
                            view: {
                                id: 'Default view'
                                key: {
                                    name: 'NULL'
                                }
                            }
                            sys_domain: 'global'
                        }
                    },
                    {
                        table: 'item_option_new'
                        id: '4bc34378871b4632a1de23ce6312a8e9'
                        key: {
                            cat_item: '4993ecfc0fa44c2eb7e404f56391fe5d'
                            variable_set: 'NULL'
                            name: 'case_details'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '4cbb3c187e404bcd977f6b0f59b6ba63'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'MX'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_user_role'
                        id: '4f6c24d3166d4510ab1514ba1617bb2c'
                        key: {
                            name: 'x_2312287_hrorch.policy_admin'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '4fbd67fdac3d42a195733d78d4131b7d'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'work_notes'
                            position: '16'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '510e8eb92f7144198ecc00809941f8a0'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'assigned_to'
                            position: '10'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '513048361ef147b0b069a44071669dfd'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'ref_number'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '514e910b75114feea9b0a1dd82fef074'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '51907c33afd845a685df399dc1931fde'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_model'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '52e74b487c424e1a9eca03ea3fccf410'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_suggestion_posted'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '535c842f3eff43f489b8c492d9cae3a8'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                            value: 'US'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'ua_table_licensing_config'
                        id: '53de477dcaf9468c99ac2544a4a429b5'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '542b7ac8df9c4976a01275bcdb390536'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'hr_case'
                        }
                    },
                    {
                        table: 'sys_db_object'
                        id: '5442b3c5580043e3ac18a15defa0e7fb'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '546e943429834a70b9a405a5d5fac3c8'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'close_notes'
                            position: '8'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '55d64ff938f747c4a2594f7e3d62caa5'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'number'
                            position: '1'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '5686debbe7944cbc86a6c577243b86ea'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'source'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '584c344f5f2e488794ac7935febb1dc1'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_employee_type'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '585157595af04659851ea72b9a06f2fb'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'end_char'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: '5aa6082f3f0b44ef9ffd1c7594b8858e'
                        key: {
                            sys_security_acl: '9457f9464bcd477b826f392305c7704a'
                            sys_user_role: {
                                id: 'f78ddb4e72514873b3564d5a264f8702'
                                key: {
                                    name: 'x_2312287_hrorch.integration'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '5b927a34ad4e4c1a8f930ace44ea3e7a'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                            value: 'benefits'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '5ba0dd1cf0b64d2ba0632453d152be90'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'ref_number'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '5bd39cf2113746a8bf63e998dd87a770'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'superseded'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '5c593ca303af4d439044d364a1cb1110'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'section'
                        }
                    },
                    {
                        table: 'sc_cat_item_category'
                        id: '5ef23e04ec99499aa7a4a7fd741bafb8'
                        key: {
                            sc_cat_item: '4993ecfc0fa44c2eb7e404f56391fe5d'
                            sc_category: 'e15706fc0a0a0aa7007fc21e1ab70c2f'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '613d5c7ca1b947678c9d34b165f43957'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'topics'
                            position: '4'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '61f8222111664b05ae49bfdd120c7ea8'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                            value: 'off'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '629901c4ace54422ad61c8a4f16cdd28'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                            value: 'high'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '63eb84d9d88b4c34894b646ad1552b9e'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_employee_type'
                            value: 'full_time'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: '6488dd5575574e279e5616ca01166f07'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'source'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '64a00298d7ab49558c77556aca80590c'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'section'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '6677853569704a82aea2883dfef871a4'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'activity.xml'
                            position: '17'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '669c62dc4e0d478e80a0003646590960'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_proposed_action'
                            position: '6'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '6923915265bf41ca83ee3026a433f628'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'hr_case'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_section'
                        id: '69b486d4c6784a63b2bd5fb3e61318fc'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            caption: 'AI assistant'
                            view: {
                                id: 'Default view'
                                key: {
                                    name: 'NULL'
                                }
                            }
                            sys_domain: 'global'
                        }
                    },
                    {
                        table: 'sys_db_object'
                        id: '69eaa104a4e0425e8ece73e796aa3076'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '6b40e0b14dd34074b258bcb995e95138'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'employee_type'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '6cc96016e8bf48b48a9c05f26e0cc859'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '6ccc4deaeed9493491d2908b916027d6'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_trace_id'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '6f4cbcff28c44bfdabaeb9cc5097ad87'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'severity'
                            value: 'medium'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '7241d786103f426fbda0b4c86e332ad3'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'US'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '72c0ed17d51a4e838f0d845c9ef03144'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'severity'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '75b013fa550c4bcbb6abf2c6c020382e'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_action'
                            value: 'close'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '7aa3a941c86b4e278342d23d3e5319ef'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'routing_rule'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '7ba8bd3b572a4a4ca53146ac6f5137a8'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'quote'
                        }
                    },
                    {
                        table: 'ua_table_licensing_config'
                        id: '7dec37fa9bca4c7a85366153fbea4e44'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                        }
                    },
                    {
                        table: 'sys_ui_form'
                        id: '7ecc96ceb3f44094af70ef361c51acfe'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            view: {
                                id: 'Default view'
                                key: {
                                    name: 'NULL'
                                }
                            }
                            sys_domain: 'global'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '7ece8f8b9caf49cb9bdba7bf43ee9e88'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_proposed_resolution'
                            position: '12'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '801636a820264fdcb3cdd9e2c655c5f4'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'severity'
                            value: 'high'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '8040611aa7d74e99b6424c1f48a1793d'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_action'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '80ca2254ee4a49cc859c57e9340b9489'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '12M.x_2312287_hrorch_hr_case.x_2312287_hrorch_ai_citation.hr_case'
                            position: '14'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '84f946e6da2a4fee90353b431605df76'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'NULL'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '860ae60306064ace83184ddac4851ab3'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'chunk_id'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '86b9aa7d0df44b348b1fb92d4b45dd73'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.end_split'
                            position: '10'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '872925a2781d4c9ba94a40fd5a763323'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                            value: 'rejected'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '8777b0728030474c8ee398ea15c953a3'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_reasoning'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '88462c31be794a05ab92febb07d6edd7'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'NULL'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '88b036edb07941338e49a2769b62e630'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'severity'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '89705e0c64a14fdb9d51a483ab6311b5'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                            value: 'unknown'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '8b3fa5b848cf4118a5026cb2588b7f21'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'short_description'
                            position: '13'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '8c16cf39167e4d9697734169d18f46d5'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            value: 'payroll'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '8f1245dd9c0b41a28538bfc9e493d637'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_model'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '908581ead8ca468eb625ca118cecf541'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'user'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '9108c197e70e4aacbed8dd12b67edccb'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'quote'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '91ab0fdcd6b64270be023372ceb5a08a'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'source'
                            value: 'chat'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: '91dd9c97378c40e7b7db4be83120e52d'
                        key: {
                            sys_security_acl: 'd3e2042b4bf04e99a9922a57062b71c4'
                            sys_user_role: {
                                id: '4f6c24d3166d4510ab1514ba1617bb2c'
                                key: {
                                    name: 'x_2312287_hrorch.policy_admin'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '949892c8cc60422e8a353bce436c5ec4'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                            value: 'completed'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '994289de48a24218861e30fa9d40929b'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.split'
                            position: '5'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: '99a13af36b874ec7aaf472391dd5b067'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: '9a304a26ccf74fddbeef641341b0a87c'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_reasoning'
                            position: '10'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '9a898755e0c7413fa118267d1aa2612b'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'IN'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '9b0645be1e8149fc8ce81674ac4ec9eb'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'AU'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '9b176bd3f20645a5a934235f539141f4'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'GB'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: '9b86ea699a2044f8bc71a79742892eda'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            value: 'unknown'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_number'
                        id: '9bda54d7d2524508bc05f38d947d80fb'
                        key: {
                            category: 'x_2312287_hrorch_hr_case'
                            prefix: 'HRC'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '9c49fe693fea493787cc77c635ba6833'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_reasoning'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: '9ed6413e7e9f42ec82af88d468c0659e'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'source'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'a0c520402b6c41d989eb241447aac091'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'a141c64a261745bfac7db05f46aebb03'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                            value: 'pending'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'a164c9eb53164c80850f181d180772c3'
                        key: {
                            sys_security_acl: '72a6a2c58e9a4f1aaed57a128a348549'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'a19cfae542914610ac0511df25e4401a'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_form_section'
                        id: 'a27140e74df84b43b6108c1c5af1446e'
                        key: {
                            sys_ui_form: {
                                id: '7ecc96ceb3f44094af70ef361c51acfe'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'a52706a4021549b69652346d63bd8738'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'chunk_id'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'a794d02372f04802a17ed1ea701d3346'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                            value: 'approved'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'a799096dd7724008b816a7491707e96f'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'assignment_group'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'aa5056cc05594a45b6bb405b33bf412c'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_suggestion'
                            position: '12'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'aa6c3133f74e4ab58ea3e76d2274a891'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                            value: 'superseded'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'aba5697d561a4169a47117b742a8cd8b'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_trace_id'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'ad1b72e43aaa44978d2698f76ca0728b'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'trace_id'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'adaf9f1d535747d0b279c3f3bb5dca24'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_model'
                            position: '4'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'add151752728491c8d77589b5cffe8dd'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'start_char'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'b27716a3f71a4d2cb95939dd82002cba'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'b48ad8aef3b14455a21fc9290b92df1c'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.end_split'
                            position: '12'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'b59c22c84b334e9294823eab1da99158'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'BR'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'b5a971841d454dd6b3f02c2b62683ee8'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'description'
                            position: '14'
                        }
                    },
                    {
                        table: 'item_option_new'
                        id: 'b67fdf4f1ffd423eb239bd6a99c5ad0e'
                        key: {
                            cat_item: '4993ecfc0fa44c2eb7e404f56391fe5d'
                            variable_set: 'NULL'
                            name: 'case_title'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'b86ab34f95cc4f6cbcd66511667cec38'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.begin_split'
                            position: '0'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'b891d8cd3e7148839d21c6dfeff3527f'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'ba3400e4894441ca98807aff2d7b97e3'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.split'
                            position: '6'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'ba9badbec7174ede84d57d23ee2e1dab'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'source'
                            value: 'triage'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'bbf6b173a7ce4b0fa9819d822b8a83b3'
                        key: {
                            sys_security_acl: '72a6a2c58e9a4f1aaed57a128a348549'
                            sys_user_role: {
                                id: 'f78ddb4e72514873b3564d5a264f8702'
                                key: {
                                    name: 'x_2312287_hrorch.integration'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'bc70377a9d744ce7ae0cd81f31f39b1f'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'ES'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'bd44a9343da546c0a606a0e8732d4c23'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'NULL'
                            language: 'en'
                        }
                    },
                    {
                        table: 'ua_table_licensing_config'
                        id: 'bf55f2ae9d6b431c87b3681f4705dd9c'
                        deleted: true
                        key: {
                            name: 'sys_user'
                        }
                    },
                    {
                        table: 'sys_user_role_contains'
                        id: 'c052c031b59e4f65b08d41c43c0c99a1'
                        key: {
                            role: {
                                id: '4f6c24d3166d4510ab1514ba1617bb2c'
                                key: {
                                    name: 'x_2312287_hrorch.policy_admin'
                                }
                            }
                            contains: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'c055941f42c741ddbecf360185e80dcd'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'c0711251c66f4979b66a39e3bfbaa6d6'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'c280f31014734cc0b44da218b89dc834'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_trace_id'
                            position: '7'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'c28c296e38494cd3843de83b8b3462e2'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                            value: 'medium'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'c4bc0f5c43f24f97887a337ebf7e20fb'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_suggestion'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'c4db89e396e5427f98884742eaa2ed81'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_status'
                            position: '1'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'c58ffaec0ac14c11a03fcb9ed749a102'
                        key: {
                            sys_security_acl: '8fc5d732415b4fe3a1143bf0017586a9'
                            sys_user_role: {
                                id: 'f78ddb4e72514873b3564d5a264f8702'
                                key: {
                                    name: 'x_2312287_hrorch.integration'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'c73b86ec419345cebcd1f82b29e1b17c'
                        key: {
                            sys_security_acl: 'd3e2042b4bf04e99a9922a57062b71c4'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'c776ca82ae3d4a62af7092ef38eeb5f0'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'IE'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'c9732ab7abaf4e00a8699f1a9f5bbc3b'
                        key: {
                            sys_security_acl: '8fc5d732415b4fe3a1143bf0017586a9'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'c9a8bec889464a3a9388ec83444cccc2'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'JP'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'ca2561aa0a6f4c10bc01236f4847df13'
                        deleted: true
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_action'
                            value: 'rejected'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'cb97ef47d1ed4a178e61515c8dbfd82d'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'state'
                            position: '7'
                        }
                    },
                    {
                        table: 'sys_ui_action_role'
                        id: 'cc248df7845f4efd89a06a34a2e90790'
                        key: {
                            sys_ui_action: 'bf2420f20d1e4f6fa5088d8f31702762'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'cd2511a2bc6a45cb88d764a20ca2afcc'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'severity'
                            value: 'any'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'ce348d0090f24132997b1a0419ac6830'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                            value: 'other'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'cfb4bfb045734eb88f8db91789690613'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'order'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'd0a5758222b2441798b2a57d51ff759f'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'd0c958b2ed7140ba83d88677f77a1e12'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_confidence'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'd10e465bc56946b09d42ea78a3dcc459'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_proposal_state'
                            position: '7'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'd3cccdce2ace43a9b3c58ac4c4175c34'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'article_version'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'd4d540539ecc4bbcac787eacb69199db'
                        deleted: true
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '12M.x_2312287_hrorch_hr_case.x_2312287_hrorch_ai_citation.hr_case'
                            position: '13'
                        }
                    },
                    {
                        table: 'ua_table_licensing_config'
                        id: 'd53007775fb94f79993abd51601377c4'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'd610322a6c17469cb738d9b7eff166a5'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'employee_type'
                            value: 'part_time'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'd7fdae898c584c1a82b3c54856ccccaf'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'start_char'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'd8bda282b2474f6ba2dbbfa665dd1018'
                        key: {
                            sys_security_acl: 'd8f6546105b54e2387f7da218f7cc5d5'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'd8d16b9a0d564181b6989423010c319e'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'active'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'd91d6db352104bdfb31cb2ffb98ec90e'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'topics'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'dbca41b57f804dafa18dc2629b495907'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_suggestion'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'dbf82242d7cd404ab443eabd4d7d643c'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                            value: 'DE'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'dd279d9b87b14ac4b86619dd7d911ba9'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'article'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'dd3f08ea417d4dc1a5d917feb3174fea'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'dd78708d9ffd466dbf0b42c26979b2ea'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'routing_rule'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'de2639f6f20041c78d5ca4a6635057e7'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'category'
                            position: '3'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'e0939d71f54e48cab9538d1bf07bc011'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_reasoning'
                            position: '11'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'e0b8a287c79e4da6ab975e26bb20e130'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            value: 'leave'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'e113670636254ef486eb20ec7ecf9ffa'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_status'
                            value: 'pending'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'e366776376524e8aa92ed87cc23739b0'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'category'
                            value: 'any'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: 'e3ca72d4f7434a9ca68df02211ce4986'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'e61f4237be9b4f758d36e9f89787c5ea'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_trace_id'
                            position: '8'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'e915a28a4b6e4cfb85c5c9b31ebf976c'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposal_state'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: 'ebc107a186464f46bedd60f7186af25e'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_country'
                        }
                    },
                    {
                        table: 'sys_ui_action_role'
                        id: 'ec106200af5347fcb3472ae65a8cca29'
                        key: {
                            sys_ui_action: 'b618199413fe4882b0da4f28278ca816'
                            sys_user_role: {
                                id: '4622e5f94ef3413590556d3b0bca914a'
                                key: {
                                    name: 'x_2312287_hrorch.hr_agent'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: 'ece4f4762a094e57b8fd55b49c68a0c3'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'category'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'ee47c5c6b1114062b2f2cb27f4682255'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'assignment_group'
                            position: '9'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'f08ff30dc9364325b6c3ae559939e654'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'superseded'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'f30504a39e9c4fb5bde2a8cd088edde9'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_resolution'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'f4260d3bce144e3c9c6cdc85c2265403'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'ai_proposed_action'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'f4c011c9618a49d9a6fa04d815d414ac'
                        key: {
                            name: 'x_2312287_hrorch_hr_case'
                            element: 'severity'
                            value: 'low'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'f4caa7d54f0d4176aadd2d6ebed47e4b'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'IT'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_security_acl_role'
                        id: 'f72b0c141497467bbe5099d8aae205a9'
                        key: {
                            sys_security_acl: 'd8f6546105b54e2387f7da218f7cc5d5'
                            sys_user_role: {
                                id: 'f78ddb4e72514873b3564d5a264f8702'
                                key: {
                                    name: 'x_2312287_hrorch.integration'
                                }
                            }
                        }
                    },
                    {
                        table: 'sys_user_role'
                        id: 'f78ddb4e72514873b3564d5a264f8702'
                        key: {
                            name: 'x_2312287_hrorch.integration'
                        }
                    },
                    {
                        table: 'sys_db_object'
                        id: 'f78de0b70c3c4578b0adfab52d062b74'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'f7b35c443ca64ced8f81c2e38e0659af'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_proposed_resolution'
                            position: '13'
                        }
                    },
                    {
                        table: 'sc_cat_item_catalog'
                        id: 'f8d7c68531d440279b1c11d3a09d8e8e'
                        key: {
                            sc_cat_item: '4993ecfc0fa44c2eb7e404f56391fe5d'
                            sc_catalog: 'e0d08b13c3330100c8b837659bba8fb4'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'f934cced3447420b978a2070f803b43b'
                        key: {
                            sys_ui_section: {
                                id: '69b486d4c6784a63b2bd5fb3e61318fc'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'AI assistant'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: 'ai_confidence'
                            position: '2'
                        }
                    },
                    {
                        table: 'sys_dictionary'
                        id: 'f96635062e264fbf9189aff029d51faa'
                        key: {
                            name: 'x_2312287_hrorch_ai_citation'
                            element: 'kb_article'
                        }
                    },
                    {
                        table: 'sys_choice'
                        id: 'f99848babc3f47499346ebb41e0a15df'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'country'
                            value: 'CN'
                            language: 'en'
                            dependent_value: 'NULL'
                        }
                    },
                    {
                        table: 'sys_ui_element'
                        id: 'fb55a0cf44f84941aa530dcc963a47b2'
                        key: {
                            sys_ui_section: {
                                id: '4b4c0c94eb1d45b09a756b612900195a'
                                key: {
                                    name: 'x_2312287_hrorch_hr_case'
                                    caption: 'HR Case'
                                    view: {
                                        id: 'Default view'
                                        key: {
                                            name: 'NULL'
                                        }
                                    }
                                    sys_domain: 'global'
                                }
                            }
                            element: '.begin_split'
                            position: '0'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: 'fd3902cb3bae42939201e31437592aa4'
                        deleted: true
                        key: {
                            name: 'sys_user'
                            element: 'x_2312287_hrorch_employee_type'
                        }
                    },
                    {
                        table: 'sys_documentation'
                        id: 'fe8f90ea554149a883ddc8f4b4d9459b'
                        key: {
                            name: 'x_2312287_hrorch_routing_rule'
                            element: 'description'
                            language: 'en'
                        }
                    },
                    {
                        table: 'sys_choice_set'
                        id: 'fea1f07be7d9492ea14f72ee6cb56140'
                        key: {
                            name: 'x_2312287_hrorch_hr_profile'
                            element: 'employee_type'
                        }
                    },
                ]
            }
        }
    }
}
