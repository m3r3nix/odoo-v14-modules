# -*- coding: utf-8 -*-
{
    'name': "View Mods",

    'summary': "Modify default views for MERENIX use cases",

    'description': "Modify default views for MERENIX use cases",

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.0',

    'depends': [
        'base',
        'product',
        'purchase',
        'purchase_stock',
        'sale_management',
        'account_intrastat',
    ],

    'data': [
        'views/product_template.xml',
        'views/sale_order.xml',
        'views/webclient_templates.xml',
    ],
}
