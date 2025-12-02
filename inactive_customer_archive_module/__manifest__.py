# -*- coding: utf-8 -*-
{
    'name': "archive customers with no invoices for 1 month",

    'summary': "Module to archive inactive customers automatically ",

    'description': """
    
        This module automatically archives customers who have not had any invoices for a period of one month.
    """,

    'author': "Eng.Huda ",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'account' ,
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
       
        'data/archived_customers_no_invoices_cron.xml',
  
    ],
    'installable': True,
    'application': True
}

