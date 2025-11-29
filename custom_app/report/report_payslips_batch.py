from odoo import models, api

class PayslipBatchXlsxReport(models.AbstractModel):
    _name = 'report.custom_app.report_payslip'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, payslip_runs):

        # ------------ Styles ------------
        header_green = workbook.add_format({
            'bold': True, 'font_color': 'white',
            'bg_color': '#4B8A3B', 'align': 'center',
            'valign': 'vcenter', 'border': 1
        })

        table_header = workbook.add_format({
            'bold': True, 'bg_color': '#D8E4BC',
            'align': 'center', 'valign': 'vcenter',
            'border': 1
        })

        cell = workbook.add_format({'border': 1})
        num_cell = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})

        total_row_format = workbook.add_format({
            'bold': True, 'bg_color': '#4B8A3B',
            'font_color': 'white', 'border': 1
        })

        total_num_format = workbook.add_format({
            'bold': True, 'bg_color': '#4B8A3B',
            'font_color': 'white', 'border': 1,
            'num_format': '#,##0.00'
        })


        # ============================================================
        # LOOP THROUGH PAYSLIP RUNS
        # ============================================================
        for run in payslip_runs:

            sheet = workbook.add_worksheet(run.name[:31])

            # Header
            sheet.merge_range(0, 0, 0, 50, "Employee Payroll", header_green)
            row = 2

            # -----------------------------------------------------------
            # 1. FIND RULES THAT HAVE VALUES IN THIS BATCH
            # -----------------------------------------------------------
            rule_totals_batch = {}

            for slip in run.slip_ids:
                for line in slip.line_ids:
                    rule_totals_batch[line.code] = rule_totals_batch.get(line.code, 0.0) + line.total

            # Keep only rules with NON-ZERO totals
            active_rule_codes = sorted(
                [code for code, total in rule_totals_batch.items() if abs(total) > 0]
            )

            # Build headers
            headers = ["Employee"] + active_rule_codes

            # Write headers
            for col, title in enumerate(headers):
                sheet.write(row, col, title, table_header)

            # Prepare totals dict
            totals = {code: 0.0 for code in active_rule_codes}

            # First detail row
            row += 1

            # -----------------------------------------------------------
            # 2. PRINT EMPLOYEE ROWS
            # -----------------------------------------------------------
            for slip in run.slip_ids:

                sheet.write(row, 0, slip.employee_id.name, cell)

                # Build rule_code → amount
                rule_map = {line.code: line.total for line in slip.line_ids}

                for col, code in enumerate(active_rule_codes, start=1):
                    value = rule_map.get(code, 0.0)
                    sheet.write(row, col, value, num_cell)
                    totals[code] += value

                row += 1

            # -----------------------------------------------------------
            # 3. TOTAL ROW
            # -----------------------------------------------------------
            sheet.write(row, 0, "TOTAL", total_row_format)

            for col, code in enumerate(active_rule_codes, start=1):
                sheet.write(row, col, totals[code], total_num_format)

            # Autofit
            sheet.set_column(0, len(headers), 18)
