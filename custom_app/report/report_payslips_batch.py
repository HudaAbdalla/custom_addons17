from odoo import models
from datetime import datetime

class PayslipBatchXlsxReport(models.AbstractModel):
    _name = 'report.custom_app.report_payslip'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, payslip_runs):
        """
        payslip_runs → hr.payslip.run recordset
        """
        for run in payslip_runs:

            sheet = workbook.add_worksheet("Payslips")
            bold = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

            # Header
            sheet.write(0, 0, 'Payslip Batch:', bold)
            sheet.write(0, 1, run.name)

            sheet.write(1, 0, 'Date From:', bold)
            sheet.write(1, 1, run.date_start, date_format)

            sheet.write(2, 0, 'Date To:', bold)
            sheet.write(2, 1, run.date_end, date_format)

            # Table header
            row = 5
            sheet.write(row, 0, 'Employee', bold)
            sheet.write(row, 1, 'Payslip Number', bold)
            sheet.write(row, 2, 'Credit Note', bold)
            sheet.write(row, 3, 'Status', bold)

            # Table body
            row += 1
            for slip in run.slip_ids:
                sheet.write(row, 0, slip.employee_id.name or "")
                sheet.write(row, 1, slip.number or "")
                sheet.write(row, 2, "Yes" if slip.credit_note else "No")
                sheet.write(row, 3, slip.state or "")
                row += 1
