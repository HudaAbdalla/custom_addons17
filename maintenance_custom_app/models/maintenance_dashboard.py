from odoo import models, api
# import logging

# _logger = logging.getLogger(__name__)

class MaintenanceDashboard(models.Model):
    _name = "maintenance.dashboard"
    _description = "Maintenance Dashboard"
    

    
    
    @api.model
    def get_state_counts(self):
        query = """
            SELECT
                state,
                COUNT(id) AS total
            FROM maintenance_request
            GROUP BY state
        """
        self.env.cr.execute(query)
        # _logger.info("Maintenance Dashboard State Counts: %s", self.env.cr.dictfetchall())
        
        return self.env.cr.dictfetchall()