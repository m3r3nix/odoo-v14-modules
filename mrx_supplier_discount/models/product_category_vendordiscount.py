# -*- coding: utf-8 -*-

from odoo import api, fields, models  # alphabetically ordered

# Create own table in database to store vendor discounts by product category
class ProductCategoryVendorDiscount(models.Model):
    _name = "mrx.product.category.vendordiscount"
    _description = "Product Category Discount by Vendor"
    
    discount = fields.Float(string='Discount %', default=0.0, digits='Discount', required=True, help="Discount percent given by this vendor")
    partner_id = fields.Many2one('res.partner', string='Vendor', domain=[('supplier_rank', '>', 0)], ondelete='cascade', required=True)
    name = fields.Many2one('product.category', string='Product Category', index=True, ondelete='cascade', required=True)
    
    _sql_constraints = [('discount_uniq', 'unique(partner_id, name)', 'This type of discount already exists!')]

# Adds one2many field to the product category table
class ProductCategory(models.Model):
    _inherit = "product.category"

    mrx_seller_ids = fields.One2many('mrx.product.category.vendordiscount', 'name', string='Vendors', help="Define vendor discount.")

# Adds one2many field to the partner table
class Partner(models.Model):
    _inherit = "res.partner"
    
    mrx_category_ids = fields.One2many('mrx.product.category.vendordiscount', 'partner_id', string='Product Category', help="Define vendor discount.")
