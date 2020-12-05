# -*- coding: utf-8 -*-

from odoo import fields, models


# Create own table in database to store vendor discounts by product category
class VendorDiscount(models.Model):
    _name = 'mrx.product.vendordiscount'
    _description = 'Price groups & Discounts by Vendor'
    _order = 'partner_id, manufacturer_id, name'
    
    partner_id = fields.Many2one('res.partner', string='Vendor', domain=[('supplier_rank', '>', 0)], ondelete='cascade', required=True)
    manufacturer_id = fields.Many2one('mrx.product.manufacturer', string='Manufacturer', required=True)
    name = fields.Char(string='Price Group', index=True, required=True, help="Name of the product price group or discount group")
    discount = fields.Float(string='Discount %', default=0.0, digits='Discount', required=True, help="Discount percent given by this vendor")
    
    _sql_constraints = [('discount_uniq', 'unique(partner_id, manufacturer_id, name)', 'This type of discount already exists!')]
