# -*- coding: utf-8 -*-
# App manifest
{
    'name': 'Product Supplier Discount',  # Name comes first, others listed in alphabetical order
    'author': 'MERENIX Elektrohandel e.K',
    'auto_install': False,
    'category': 'Product',
    'data': [
        'security/ir.model.access.csv',
        # I do not adapt "mrx_pricing_unit" in v13 to the accounting app, (but leave this option open) instead it gets calculated "price_unit"
        # 'views/account_invoice.xml',
        'views/base__res_partner.xml',
        # 'views/product__product_views.xml',
        'views/vendordiscount.xml',
        # 'views/purchase__purchase_views.xml',
        # 'views/sale__sale_views.xml',
    ],
    'depends': [
        'base',
        'product',
        'purchase',
        'purchase_stock',
        'sale_management',
        'mrx_product_manufacturer',
    ],
    'description': '',  # Leave description empty to display the README file
    'installable': True,
    'summary': 'Supplier discount information for products. Implemented into Products, Purchase and Accounting apps',
    'version': '14.0.1.0',
    'website': '',
}
