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
    'depends': ['base','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'report/sale_order_report_action.xml',
        'report/sale_order_report_templates.xml',
  
    ],
    'installable': True,
    'application': True
}

