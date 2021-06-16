# -*- coding: utf-8 -*-

from odoo import fields, models


# Create own table in database to store vendor discounts by price groups
class VendorDiscount(models.Model):
    _name = 'mrx.vendor.discount'
    _description = 'Price Groups & Discounts by Vendor'
    _order = 'partner_id, manufacturer_id, price_group_id'
    _rec_name = 'price_group_id'

    partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='cascade', required=True)
    manufacturer_id = fields.Many2one('mrx.product.manufacturer', string='Manufacturer', required=True)
    price_group_id = fields.Many2one('mrx.manufacturer.price.group', string='Price Group', required=True, index=True)
    discount = fields.Float(string='Discount %', default=0.0, digits='Discount', required=True, help="Discount percent given by this vendor")

    _sql_constraints = [
        ('discount_uniq', 'UNIQUE(partner_id, manufacturer_id, price_group_id)', 'This type of discount already exists!'),
    ]
