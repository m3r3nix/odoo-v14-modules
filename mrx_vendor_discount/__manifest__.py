# -*- coding: utf-8 -*-
# App manifest
{
    'name': 'Vendor Discount',  # Name comes first, others listed in alphabetical order
    'author': 'MERENIX Elektrohandel e.K',
    'auto_install': False,
    'category': 'Product',
    'data': [
        'security/ir.model.access.csv',
        # "mrx_pricing_unit" does not implemented into accounting app yet, instead it gets already calculated value of "price_unit"
        # 'views/account__invoice.xml',
        'views/base__res_partner.xml',
        'views/manufacturer_price_group_views.xml',
        'views/product__product_views.xml',
        'views/purchase__portal_templates.xml',
        'views/purchase__purchase_views.xml',
        'views/sale__sale_views.xml',
        'views/vendor_discount_views.xml',
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
    'summary': 'Vendor discount information for products. Implemented into Partner, Products, Purchase and Accounting apps',
    'version': '14.0.1.1',
    'website': '',
}
