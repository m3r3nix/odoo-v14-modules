# -*- coding: utf-8 -*-

from odoo import fields, models


# Create own table in database to store name of Manufacturers
class ProductManufacturer(models.Model):
    _name = 'mrx.product.manufacturer'
    _description = 'List of Manufacturers'
    _order = 'name'

    name = fields.Char(required=True, store=True, copy=True, index=True)

    _sql_constraints = [('unique_name', 'unique(name)', 'Manufacturer already exists!')]


# Add Manufacturer field to the product template table
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    mrx_product_manufacturer = fields.Many2one('mrx.product.manufacturer', string='Manufacturer', index=True)
