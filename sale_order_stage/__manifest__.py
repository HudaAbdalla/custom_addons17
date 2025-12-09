# -*- coding: utf-8 -*-
{
    'name': "Sale Order Management Approve Stage ",

    'summary': " Module to manage  custom sale order stages and approvals ",

    'description': """
    
    """,

    'author': "Eng.Huda ",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'sale_management' ,
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_inherit_views.xml',
       
    ],
    'installable': True,
    'application': True
}

