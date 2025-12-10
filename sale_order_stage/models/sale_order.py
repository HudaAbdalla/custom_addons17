

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Add new stage to the state field
    state = fields.Selection(selection_add=[
        ('draft', 'Quotation'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ])

    approval_limit = 10000  # later you can convert this into a system parameter

    # ---------------------------------------------------------------------
    # Create Activity for Sales Managers
    # ---------------------------------------------------------------------
    def _create_approval_activity(self):
        """Creates a To-Do activity for all Sales Managers when approval needed."""
        manager_group = self.env.ref("sales_team.group_sale_manager")
        manager_users = manager_group.users

        for order in self:
            for user in manager_users:
                self.env["mail.activity"].create({
                    "res_id": order.id,
                    "res_model_id": self.env.ref("sale.model_sale_order").id,
                    "user_id": user.id,
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "summary": "Sale Order Approval Required",
                    "note": f"Sale Order {order.name} needs manager approval. "
                            f"Total Amount: {order.amount_total}.",
                })

    # ---------------------------------------------------------------------
    # Override action_confirm (Stop confirmation if amount > limit)
    # ---------------------------------------------------------------------
    def action_confirm(self):
        for order in self:
            # Move to approval state if amount is too high
            if order.amount_total > order.approval_limit and order.state != 'awaiting_approval':
                order.state = 'awaiting_approval'
                order._create_approval_activity()   # <-- Create activity for sales managers
                return  # Stop confirmation until approved

        # Normal Odoo confirmation flow
        return super(SaleOrder, self).action_confirm()

    # ---------------------------------------------------------------------
    # Manager Approval Button
    # ---------------------------------------------------------------------
    def action_approve_order(self):
        """Sales Manager clicks Approve → Order becomes confirmable."""
        for order in self:
            if not self.env.user.has_group('sales_team.group_sale_manager'):
                raise UserError("Only Sales Managers can approve this order.")

            # Remove all pending approval activities
            activities = self.env["mail.activity"].search([
                ('res_id', '=', order.id),
                ('res_model', '=', 'sale.order')
            ])
            activities.unlink()

            # Move order to 'sent' so confirmation is allowed
            order.state = 'sent'

        # Final confirmation
        return super(SaleOrder, self).action_confirm()

    # ---------------------------------------------------------------------
    # Allow confirmation from awaiting_approval
    # ---------------------------------------------------------------------
    def _check_confirmation_allowed(self):
        """Extend allowed states to include 'awaiting_approval'."""
        confirmable_states = ('draft', 'sent', 'awaiting_approval')
        for order in self:
            if order.state not in confirmable_states:
                raise UserError(
                    f"The following orders are not in a state requiring confirmation: {order.name}"
                )
