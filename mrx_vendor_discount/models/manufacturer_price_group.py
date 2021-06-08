# -*- coding: utf-8 -*-

from odoo import fields, models


# Create own table in database to store price groups
class PriceGroup(models.Model):
    _name = 'mrx.manufacturer.price.group'
    _description = 'Price Groups by Manufacturer'
    _order = 'manufacturer_id, name'

    name = fields.Char(string='Price Group', index=True, required=True, help="Name of the product price group or discount group")
    manufacturer_id = fields.Many2one('mrx.product.manufacturer', string='Manufacturer', required=True)
    discount_ids = fields.One2many('mrx.vendor.discount', 'price_group_id', string="Vendors")

    _sql_constraints = [('pricegroup_uniq', 'UNIQUE(manufacturer_id, name)', 'This type of price group already exists!')]


class ProductManufacturer(models.Model):
    _inherit = 'mrx.product.manufacturer'

    price_group_ids = fields.One2many('mrx.manufacturer.price.group', 'manufacturer_id', string="Price Groups")
