from odoo import api, fields, models, _
from datetime import datetime, timedelta

# class ResPartner(models.Model):
#     _inherit = 'res.partner'

#     @api.model
#     def cron_archive_customers_no_invoices(self):
#         """Archives customers with no invoices for 1 month.
#            Skips contacts linked to active users.
#         """

#         one_month_ago = datetime.today() - timedelta(days=30)

#         # Find non-archived customers
#         customers = self.search([
#             ("customer_rank", ">", 0),
#             ("active", "=", True),
#         ])

#         customers_to_archive = self.env['res.partner']
#         skipped_due_to_users = self.env['res.partner']

#         for partner in customers:

#             # 🔴 Skip customers linked to active users
#             if partner.user_ids.filtered(lambda u: u.active):
#                 skipped_due_to_users |= partner
#                 continue

#             # Check invoices
#             invoices = self.env['account.move'].search_count([
#                 ("partner_id", "=", partner.id),
#                 ("move_type", "in", ["out_invoice", "out_refund"]),
#                 ("invoice_date", ">=", one_month_ago)
#             ])

#             if invoices == 0:
#                 customers_to_archive |= partner

#         # Archive allowed customers
#         customers_to_archive.write({"active": False})
#         archived_count = len(customers_to_archive)

#         # Prepare message for admin
#         message = _("Automatic Archive: %s customers were archived (no invoices for 1 month).") % archived_count

#         if skipped_due_to_users:
#             message += _("<br/><br/>⚠ The following customers were skipped because they are linked to active users:<br/>• %s") % (
#                 "<br/>• ".join(skipped_due_to_users.mapped("name"))
#             )

#         # Notify admin
#         admin = self.env.ref("base.user_admin")
#         admin.partner_id.message_post(
#             body=message,
#             subject="Customer Auto-Archive",
#             message_type="notification",
#             subtype_xmlid="mail.mt_comment",
#         )

#         return True







 
# from odoo import api, fields, models, _
# from datetime import datetime, timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def cron_archive_customers_no_invoices(self):
        """Archives customers with no invoices for 1 month.
           Skips contacts linked to active users.
           Sends in-app notification to admin.
        """

        # 🔹 Compute the threshold date (1 month ago)
        one_month_ago = datetime.today() - timedelta(days=30)  # Change 30 to 1 for testing

        # 🔹 Get all active customers
        customers = self.search([
            ("customer_rank", ">=", 0),
            ("active", "=", True),
        ])

        customers_to_archive = self.env['res.partner']
        skipped_due_to_users = self.env['res.partner']

        for partner in customers:

            # 🔴 Skip customers linked to active users
            if partner.user_ids.filtered(lambda u: u.active):
                skipped_due_to_users |= partner
                continue

            # 🔹 Count invoices in last month
            invoices = self.env['account.move'].search_count([
                ("partner_id", "=", partner.id),
                ("move_type", "in", ["out_invoice", "out_refund"]),
                ("invoice_date", ">=", one_month_ago)
            ])

            if invoices == 0:
                customers_to_archive |= partner

        # 🔹 Archive allowed customers
        customers_to_archive.write({"active": False})
        archived_count = len(customers_to_archive)

        # 🔹 Prepare admin notification message
        message = _("Automatic Archive: %s customers were archived (no invoices for 1 month).") % archived_count

        if skipped_due_to_users:
            message += _("\n\n⚠ The following customers were skipped because they are linked to active users:\n• %s") % (
    "\n• ".join(skipped_due_to_users.mapped("name"))
            )

        # 🔹 Send in-app notification to admin
        admin = self.env.ref("base.user_admin", raise_if_not_found=False)
        if not admin:
            admin = self.env['res.users'].search([('login', '=', 'admin')], limit=1)

        if admin:
            admin.partner_id.message_notify(
                subject="Customer Auto-Archive",
                body=message,
                partner_ids=[admin.partner_id.id],
              
            )

        return True
