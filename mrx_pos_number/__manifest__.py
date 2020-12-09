# -*- coding: utf-8 -*-
{
    'name': "Position Number",

    'summary': "Add Pos. number field to SO, PO and DN",

    'description': "Add Pos. number field to SO, PO and DN",

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '14.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'purchase',
        'sale_management',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
