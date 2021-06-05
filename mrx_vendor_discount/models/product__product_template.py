# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Add some extra fields to the model
    mrx_price_group = fields.Many2one('mrx.manufacturer.price.group', string='Price Group', store=True, help="Price group or product group provided by the manufacture")
    mrx_pricing_unit = fields.Integer(string='Pricing Unit', default=1, required=True, store=True, help="How many items to get for this price? 1/10/100/1000")
    mrx_packaging_unit = fields.Integer(string='Packaging Unit', default=1, required=True, store=True, help="How many pieces in one package?")
    mrx_moq = fields.Integer(string='MOQ', default=1, required=True, store=True, help="Minimum order quantity")

    @api.onchange('mrx_price_group')
    def _fill_category_if_same_as_price_group(self):
        if self.mrx_price_group:
            category_id = self.env['product.category'].search([('parent_id.name', '=', self.mrx_product_manufacturer.name), ('name', '=', self.mrx_price_group.name)], limit=1)
            if category_id:
                self.categ_id = category_id