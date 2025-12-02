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
    'depends': ['hr',
                'base',
                'sale_management',
                'bi_hr_payroll',
                'report_xlsx' ,
                'account' ,
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
       
        # 'data/employee_sequence.xml',
        # 'data/hr_employee_cron.xml',
        'data/archived_customers_no_invoices_cron.xml',

        
        # 'views/hr_employee_view.xml',
        
        'report/report_actions.xml',
        'report/sale_order_report_templates.xml',
  
    ],
    'installable': True,
    'application': True
}

