# -*- coding: utf-8 -*-
{
    'name': "SO Profit",

    'summary': "Calculate profit for a sales order like sum(so.bills)-sum(po.bills)",

    'description': "Calculate profit for a sales order like sum(so.bills)-sum(po.bills)",

    'author': "MERENIX Elektrohandel e.K.",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '17.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale_management',
                'sale_purchase_stock',
                'purchase',
                'account',
                'mrx_so_po_relation',
    ],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
