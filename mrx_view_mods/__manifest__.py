# -*- coding: utf-8 -*-
{
    'name': "mrx_view_mods",

    'summary': "Modify default views for MERENIX",

    'description': "Modify default views for MERENIX",

    'author': "MERENIX Elektrohandel e.K.",
    'website': "https://www.merenix.de",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'purchase',
        'purchase_stock',
        'sale_management',
    ],

    # always loaded
    'data': [
#        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/sale_order.xml',
    ],
}
