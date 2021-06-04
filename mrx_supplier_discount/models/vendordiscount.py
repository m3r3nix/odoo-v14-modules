# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductManufacturer(models.Model):
    _inherit = 'mrx.product.manufacturer'

    pricegroup_ids = fields.One2many('mrx.manufacturer.pricegroup', 'manufacturer_id', string="Price Groups")

# Create own table in database to store price groups
class PriceGroup(models.Model):
    _name = 'mrx.manufacturer.pricegroup'
    _description = 'Price Groups by Manufacturer'
    _order = 'manufacturer_id, name'

    manufacturer_id = fields.Many2one('mrx.product.manufacturer', string='Manufacturer', required=True)
    name = fields.Char(string='Price Group', index=True, required=True, help="Name of the product price group or discount group")
    partner_ids = fields.One2many('mrx.product.vendordiscount', 'name', string="Vendors")

    _sql_constraints = [('pricegroup_uniq', 'UNIQUE(manufacturer_id, name)', 'This type of price group already exists!')]


# Create own table in database to store vendor discounts by price groups
class VendorDiscount(models.Model):
    _name = 'mrx.product.vendordiscount'
    _description = 'Price groups & Discounts by Vendor'
    _order = 'partner_id, manufacturer_id, name'
    
    partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='cascade', required=True)
    manufacturer_id = fields.Many2one(related='name.manufacturer_id', readonly=True)
    name = fields.Many2one('mrx.manufacturer.pricegroup', string='Price Group', required=True)
    discount = fields.Float(string='Discount %', default=0.0, digits='Discount', required=True, help="Discount percent given by this vendor")

    _sql_constraints = [
        ('discount_uniq', 'UNIQUE(partner_id, name)', 'This type of discount already exists!'),
    ]
