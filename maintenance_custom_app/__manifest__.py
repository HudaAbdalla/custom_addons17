# -*- coding: utf-8 -*-
{
    'name': "Maintenance Request Addon",

    'summary': "Module to manage maintenance requests ...",

    'description': """
    
        This module allows you to create and manage maintenance requests for equipment or facilities.
        Create a model maintenance.request with: 
            -Name, date, cost, employee -Status: draft → in_progress → done
            -Add track for all fields in chatter
            -Enable search by name and employee
            -Add all fields in tree view
            -Submit button to change status from draft to in progress (for Maintenance Officer)
            -Approve button to change status from in progress to done ( for maintenance manager)
            -Add group by status, date and employee
            -Add filter for (draft, in progress and done)""",

    'author': "Eng.Huda ",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'hr' ,
                'mail',
                ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/maintenance_request_views.xml',
        'views/maintenance_dashboard_views.xml',
        'data/maintenance_request_demo.xml',
    ],
    "assets":   {
    "web.assets_backend": [
        "maintenance_custom_app/static/src/js/maintenance_dashboard.js",
        "maintenance_custom_app/static/src/xml/maintenance_dashboard.xml",
        "maintenance_custom_app/static/src/css/dashboard.css"
    ],
    },
    'installable': True,
    'application': True
}

