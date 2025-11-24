# -*- coding: utf-8 -*-
{
    'name': "huda excercise module",

    'summary': "custom app for excercise",

    'description': """
custom app for excercise
""",

    'author': "Eng.Huda ",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','bi_hr_payroll','report_xlsx'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/hr_payslip_view.xml',
        # 'views/report_payslip_batch.xml'
        # 'views/templates.xml',
        'report/report_actions.xml',
        'report/sale_order_report_templates.xml',
  
    ],
    'installable': True,
    'application': True
}

