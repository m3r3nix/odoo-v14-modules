# -*- coding: utf-8 -*-
{
    'name': "PDF Report Custom Mods",

    'summary': """
        This module contains my custom modifications for PDF reports""",

    'description': """
        This module contains my custom modifications for PDF reports such as invoice, delivery note, etc...
    """,

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '17.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'account_intrastat',
        'stock',
        'mrx_delivery_note_on_invoice',
    ],

    # always loaded
    'data': [
        'views/res_company_views.xml',
        'report/default_layout.xml',
        'report/delivery_note_mods.xml',
        'report/invoice_mods.xml',
        'report/purchaseorder_mods.xml',
        'report/so_proforma_mods.xml',
    ],
}
