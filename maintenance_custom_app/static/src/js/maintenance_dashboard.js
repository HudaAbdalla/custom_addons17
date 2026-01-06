/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class MaintenanceDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ stats: [] });

        onWillStart(async () => {
            this.state.stats = await this.orm.call(
                "maintenance.dashboard",
                "get_state_counts",
                []
            );
        });
    }

    getStateLabel(state) {
        const mapping = {
            draft: "Draft",
            in_progress: "In Progress",
            done: "Done",
        };
        return mapping[state] || state;
    }
}

MaintenanceDashboard.template = "colored_kpi_dashboard.Template";

registry.category("actions").add("maintenance_dashboard", MaintenanceDashboard);
