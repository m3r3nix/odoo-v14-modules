# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Creates own table in database to store Manufacturer's name
class ProductManufacturer(models.Model):
    _name = 'mrx.product.manufacturer'
    _description = 'List of Manufacturers'

    name = fields.Char(required=True, store=True, copy=True)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Manufacturer already exists!')]

# Create Manufacturer field in product table
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    mrx_product_manufacturer = fields.Many2one('mrx.product.manufacturer', string='Manufacturer', index=True)
