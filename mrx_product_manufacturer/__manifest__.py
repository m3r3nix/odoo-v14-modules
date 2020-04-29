# -*- coding: utf-8 -*-
{
    'name': "mrx_product_manufacturer",

    'summary': "Add Manufacturer of product option",

    'description': "Add Manufacturer of product option",

    'author': "MERENIX Elektrohandel e.K.",
    'website': "https://www.merenix.de",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '13.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'purchase',
        'sale_management',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
