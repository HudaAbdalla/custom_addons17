from odoo import models, fields

class MaintenanceRequest(models.Model):
    _name = "maintenance.request"
    _description = "Maintenance Request"
    _inherit = ["mail.thread", "mail.activity.mixin"] # To enable chatter functionality
    _order = "date_request desc"

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True
    )
    date_request = fields.Date(
        string="Request Date",
        default=fields.Date.today,
        tracking=True
    )
    cost = fields.Float(
        string="Cost",
        tracking=True
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        tracking=True
    )
#  status bar
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        tracking=True
    )

    # --- Buttons / Status transitions ---
    def action_in_progress(self):
        for rec in self:
            rec.state = "in_progress"

    def action_done(self):
        for rec in self:
            rec.state = "done"
