# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Add some extra fields to the model
    mrx_price_group = fields.Many2one('mrx.manufacturer.price.group', string='Price Group', store=True, index=True, help="Price group or product group provided by the manufacture")
    mrx_pricing_unit = fields.Integer(string='Pricing Unit', default=1, required=True, store=True, help="How many items to get for this price? 1/10/100/1000")
    mrx_packaging_unit = fields.Integer(string='Packaging Unit', default=1, required=True, store=True, help="How many pieces in one package?")
    mrx_moq = fields.Integer(string='MOQ', default=1, required=True, store=True, help="Minimum order quantity")

    @api.onchange('mrx_product_manufacturer')
    def _autofill_category_if_manufacturer_exists(self):
        if self.mrx_product_manufacturer and self.categ_id.id == 1:
            category_id = self.env['product.category'].search([('name', '=', self.mrx_product_manufacturer.name)], limit=1)
            if category_id:
                self.categ_id = category_id

    @api.onchange('mrx_price_group')
    def _autofill_category_if_price_group_exists(self):
        if self.mrx_price_group:
            category_id = self.env['product.category'].search([('parent_id.name', '=', self.mrx_product_manufacturer.name), ('name', '=', self.mrx_price_group.name)], limit=1)
            if category_id:
                self.categ_id = category_id

    ### I have turned this function into an automated action, but I leave it here for now
    # @api.depends('seller_ids')
    # def _copy_best_purchase_price_to_cost(self):
    #     for line in self:
    #         if line.seller_ids:
    #             sellers = line.seller_ids.filtered(lambda s: s.name.active).sorted(lambda s: (s.mrx_computed_purchase_price))
    #             date = fields.Date.context_today(self)
    #             res = self.env['product.supplierinfo']

    #             for seller in sellers:
    #                 if seller.date_start and seller.date_start > date:
    #                     continue
    #                 if seller.date_end and seller.date_end < date:
    #                     continue
    #                 if not res or res.name == seller.name:    
    #                     res |= seller

    #             seller = res.sorted('mrx_computed_purchase_price')[:1]

    #             line.standard_price = seller.mrx_computed_purchase_price

    #             if len(line.product_variant_ids) == 1:
    #                 line.product_variant_ids.standard_price = seller.mrx_computed_purchase_price
