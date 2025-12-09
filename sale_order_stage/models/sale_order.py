from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[
        ('draft', 'Quotation'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ])

    approval_limit = 10000  # you can later make this a setting

    def action_confirm(self):
        """
        Override confirm to block large orders until approved.
        """
        for order in self:
            # If already approved or not needing approval → normal flow
            if order.state in ('sale', 'done'):
                return super().action_confirm()

            # If amount exceeds limit and not yet approved → block
            if order.amount_total > self.approval_limit and order.state != 'awaiting_approval':
                order.state = 'awaiting_approval'
                return

        return super().action_confirm()

    def action_approve_order(self):
        """Manager approval button."""
        for order in self:
            if not self.env.user.has_group('sales_team.group_sale_manager'):
                raise UserError("Only Sales Managers can approve this order.")

            # Set state back so Odoo allows confirmation
            order.state = 'sent' if order.state == 'awaiting_approval' else order.state

        # Now call normal confirm (Odoo will NOT complain)
        return super(SaleOrder, self).action_confirm()

    def _check_confirmation_allowed(self):
        """
        Odoo default checks only allow 'draft' and 'sent'.
        We must extend it to allow 'awaiting_approval'.
        """
        # call original, but include awaiting_approval
        confirmable_states = ('draft', 'sent', 'awaiting_approval')
        for order in self:
            if order.state not in confirmable_states:
                raise UserError(
                    "The following orders are not in a state requiring confirmation: %s" % order.name
                )
