# -*- coding: utf-8 -*-
{
    'name': "mrx_manufacturer",

    'summary': "Add Manufacturer of product field",

    'description': "Add Manufacturer of product field",

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
#        'views/views.xml',
#        'views/templates.xml',
        'views/product_template.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
#    'demo': [
#        'demo/demo.xml',
#    ],
}
