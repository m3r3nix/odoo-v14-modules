# -*- coding: utf-8 -*-
{
    'name': "mrx_profit",

    'summary': "Calculate profit for an order like sum(so.bills)-sum(po.bills)",

    'description': "Calculate profit for an order like sum(so.bills)-sum(po.bills)",

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale_management',
                'purchase',
                'account',
    ],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
