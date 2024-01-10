# -*- coding: utf-8 -*-
{
    'name': "Delivery Note on Invoice",

    'summary': """
        Display delivery note number on invoice line
    """,

    'description': """
        Display delivery note number on invoice line
    """,

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '17.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'sale',
        'stock',
    ],

    # always loaded
    'data': [
        'views/account_move_views.xml',
    ],
}
