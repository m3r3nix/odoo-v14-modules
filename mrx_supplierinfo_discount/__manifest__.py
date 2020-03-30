# -*- coding: utf-8 -*-
# App manifest
{
    'name': 'Product Supplier Discount',  # Name comes first, others listed in alphabetical order
    'author': 'MERENIX Elektrohandel e.K',
    'auto_install': False,
    'category': 'Product',
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_vendordiscount.xml',
        'views/res_partner.xml',
        'views/product_category.xml',
        'views/product_supplierinfo.xml',
        'views/purchase.xml',
#        'views/account_invoice.xml',
    ],
    'depends': [
        'base',
        'product',
        'purchase',
        'purchase_stock',
        'sale_management',
        'mrx_so_pricing_unit',
    ],
    'description': '',  # Leave description empty to display the README file
    'installable': True,
    'summary': 'Supplier discount information for products implemented into Products, Purchase and Accounting apps',
    'version': '13.0.0.0',
    'website': '',
}
