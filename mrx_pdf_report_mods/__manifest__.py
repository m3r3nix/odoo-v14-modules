# -*- coding: utf-8 -*-
{
    'name': "PDF Report custom mods",

    'summary': """
        This module contains my custom modifications for PDF reports""",

    'description': """
        This module contains my custom modifications for PDF reports such as invoice, delivery note, etc...
    """,

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'stock',
    ],

    # always loaded
    'data': [
        'views/res_company_views.xml',
        'report/default_layout.xml',
        'report/invoice_mods.xml',
    ],
}
