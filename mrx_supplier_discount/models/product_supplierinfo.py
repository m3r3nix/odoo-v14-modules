# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import api, fields, models


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    # Add some extra fields to the model
    mrx_product_manufacturer = fields.Many2one(
        related='product_tmpl_id.mrx_product_manufacturer',
        readonly=True,
    )
    mrx_price_group = fields.Many2one(
        'mrx.product.vendordiscount',
        string='Price Group',
        store=True,
    )
    mrx_discount_type = fields.Selection(
        selection=[('net_price','Net Price'),('price_group','Price Group'),('product_only','Product Only')],
        default='price_group',
        help='Discount type to be used for this product',
        string='Discount Type',
        store=True,
        required=True,
    )
    mrx_discount = fields.Float(
        compute='_compute_discount',
        digits='Discount',
        help='Discount percentage given by the supplier. The value of this field is handed over to other modules.',
        string='Discount %',
        store=True,
    )
    mrx_computed_purchase_price = fields.Float(
        compute='_compute_purchase_price',
        digits='Product Price',
        string='Purchase Price',
        readonly=True,
        store=True,
    )
    mrx_packaging_unit = fields.Integer(
        default=1,
        string='Packaging Unit',
        help='How many units are in one package?',
        store=True,
    )
    mrx_pricing_unit = fields.Integer(
        default=1,
        string='Pricing Unit',
        help='How many units to get for this price?',
        store=True,
    )

    # If "net_price" is used, then set discount to 0.0
    def get_net_price_discount(self, line):
        return 0.0

    # Set vendor discount for the given price group
    def get_price_group_discount(self, line):
        if line.name and line.mrx_product_manufacturer and line.mrx_price_group and line.mrx_discount_type == 'price_group':
            discount_id = self.env['mrx.product.vendordiscount']._search([('partner_id', '=', line.name.id), ('manufacturer_id', '=', line.mrx_product_manufacturer.id), ('name', '=', line.mrx_price_group.name)], limit=1)
            return self.env['mrx.product.vendordiscount'].browse(discount_id).discount
        else:
            return 0.0

    # If "product_only" is used, then set discount to the typed amount by the user
    def get_product_only_discount(self, line):
        return line.mrx_discount

    # Decide how to compute product discount: Net Price / Price Group / Product Only
    @api.depends('mrx_discount_type', 'mrx_price_group')
    def _compute_discount(self):
        for line in self:
            method_name = 'get_' + str(line.mrx_discount_type) + '_discount'
            method = getattr(self, method_name)
            line.mrx_discount = method(line)

    # Compute purchase price based on the above specified criteria
    @api.depends('price', 'mrx_discount', 'mrx_pricing_unit')
    def _compute_purchase_price(self):
        for line in self:
            line.mrx_computed_purchase_price = (line.price / line.mrx_pricing_unit) * (1 - (line.mrx_discount or 0.0) / 100)
