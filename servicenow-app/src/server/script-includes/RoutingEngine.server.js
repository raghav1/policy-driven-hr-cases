/**
 * Picks the assignment for a case from the HR Routing Rule table.
 * Rules are checked by order; the first active rule matching category and severity wins.
 */
var RoutingEngine = Class.create();
RoutingEngine.prototype = {
    initialize: function () {},

    evaluate: function (category, severity) {
        var rule = new GlideRecord('x_2312287_hrorch_routing_rule');
        rule.addActiveQuery();
        rule.orderBy('order');
        rule.query();
        while (rule.next()) {
            var cat = rule.getValue('category');
            var sev = rule.getValue('severity');
            if ((cat == 'any' || cat == category) && (sev == 'any' || sev == severity)) {
                return {
                    sys_id: rule.getUniqueValue(),
                    name: rule.getValue('name'),
                    order: rule.getValue('order'),
                    assignment_group: rule.getValue('assignment_group'),
                    group_name: rule.getDisplayValue('assignment_group'),
                    assigned_to: rule.getValue('assigned_to'),
                };
            }
        }
        return null;
    },

    type: 'RoutingEngine',
};
