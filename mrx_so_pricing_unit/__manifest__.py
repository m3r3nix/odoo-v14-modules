# -*- coding: utf-8 -*-
{
    'name': "Sales Order Pricing Unit",

    'summary': """
        Add pricing unit and packaging unit fields to the product template and to the SO, as well and calculate the price based on that.
        """,

    'description': """
        Add pricing unit and packaging unit fields to the product template and to the SO, as well and calculate the price based on that.
        """,

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",
    'installable': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '13.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale_management'],

    # always loaded
    'data': [
        'views/sale.xml',
    ],
}
