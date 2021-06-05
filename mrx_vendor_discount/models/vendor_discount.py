# -*- coding: utf-8 -*-

from odoo import fields, models


# Create own table in database to store vendor discounts by price groups
class VendorDiscount(models.Model):
    _name = 'mrx.vendor.discount'
    _description = 'Price Groups & Discounts by Vendor'
    _order = 'partner_id, manufacturer_id, name'
    
    partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='cascade', required=True)
    manufacturer_id = fields.Many2one(related='name.manufacturer_id', readonly=True)
    name = fields.Many2one('mrx.manufacturer.price.group', string='Price Group', required=True)
    discount = fields.Float(string='Discount %', default=0.0, digits='Discount', required=True, help="Discount percent given by this vendor")

    _sql_constraints = [
        ('discount_uniq', 'UNIQUE(partner_id, name)', 'This type of discount already exists!'),
    ]
