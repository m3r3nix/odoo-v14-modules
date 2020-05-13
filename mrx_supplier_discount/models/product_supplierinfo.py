# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo
from odoo import api, fields, models  # alphabetically ordered

# Model
class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    # Fields declaration
    mrx_pricing_type = fields.Selection(
        selection=[('net_price','Net Price'),('discount','List Price')],
        default='discount',
        help="Pricing type to be used for the product supplier",
        string='Pricing Type',
        store=True,
        required=True,
    )
    mrx_category_discount = fields.Float(
        compute='_compute_category_discount',
        string='Category Discount',
        help="Product category discount given by this vendor",
        readonly=True,
    )
    mrx_unique_discount = fields.Float(
        default=0.0,
        digits='Discount',
        help="Have to be filled only if vendor gives a unique discount for this product. In this case category discount will be not applied!",
        string='Unique Discount',
        store=True,
    )
    mrx_unique_discount_boolean = fields.Boolean(
        default=False,
        string="Unique?",
        help="If it's checked, then category discount will be ignored!",
        store=True,
    )
    mrx_discount = fields.Float(
        compute='_compute_discount',
        digits='Discount',
        help="Discount percentage given by the supplier. The value of this field is handed over to other modules.",
        string='Discount',
        readonly=True,
    )
    mrx_computed_purchase_price = fields.Float(
        compute='_compute_purchase_price',
        digits='Product Price',
        string='Purchase Price',
        readonly=True,
        store=True,
    )
    mrx_pricing_unit = fields.Integer(
        default=1,
        string='Pricing Unit',
        help='How many units to get for this price?',
        store=True,
    )
    mrx_packaging_unit = fields.Integer(
        default=1,
        string='Packaging Unit',
        help='How many units are in one package?',
        store=True,
    )
    mrx_product_category = fields.Many2one(
        related='product_tmpl_id.categ_id',
        ondelete='cascade',
        readonly=True,
    )

    # Compute and search fields, in the same order of fields declaration
    # # Get and set vendor discount for the given product category
    @api.depends('name', 'product_tmpl_id')
    def _compute_category_discount(self):
        for line in self:
            if line.name and line.product_tmpl_id:
                discount_id = self.env['mrx.product.category.vendordiscount']._search([('name', '=', line.product_tmpl_id.categ_id.id), ('partner_id', '=', line.name.id)], limit=1)
                line.mrx_category_discount = self.env['mrx.product.category.vendordiscount'].browse(discount_id).discount
            else:
                line.mrx_category_discount = 0.0

    # Decide how to compute product discount. Net Price / List Price / Unique Discount / Category Discount
    @api.depends('mrx_pricing_type', 'mrx_unique_discount_boolean', 'mrx_unique_discount', 'mrx_category_discount')
    def _compute_discount(self):
        for line in self:
            if line.mrx_pricing_type == 'net_price' or line.mrx_unique_discount_boolean == True:
                line.mrx_discount = line.mrx_unique_discount
            else:
                line.mrx_unique_discount = 0.0
                line.mrx_discount = line.mrx_category_discount

    # Compute purchase price based on the above specified criteria
    @api.depends('price', 'mrx_discount', 'mrx_pricing_unit')
    def _compute_purchase_price(self):
        for line in self:
            line.mrx_computed_purchase_price = (line.price / line.mrx_pricing_unit) * (1 - (line.mrx_discount or 0.0) / 100)

    # Constraints and onchanges
    # # Copy some data automatically from the product template to reduce user's work
    @api.onchange('product_tmpl_id')
    def _copy_product_data(self):
        if self.product_tmpl_id:
            self.mrx_packaging_unit = self.product_tmpl_id.mrx_packaging_unit
            self.price = self.product_tmpl_id.list_price
            self.mrx_pricing_unit = self.product_tmpl_id.mrx_pricing_unit
            self.min_qty = self.product_tmpl_id.mrx_moq

    #  Set product discount and calculate purchase price live on the form
    @api.onchange('mrx_pricing_type', 'price', 'mrx_pricing_unit', 'mrx_unique_discount_boolean', 'mrx_unique_discount')
    def _onchange_listprice_discount(self):
        if self.mrx_pricing_type == 'net_price' or self.mrx_unique_discount_boolean == True:
            self.mrx_discount = self.mrx_unique_discount
        else:
            self.mrx_unique_discount = 0.0
            self.mrx_discount = self.mrx_category_discount

        if self.mrx_unique_discount < -100 or self.mrx_unique_discount > 100:
            return {
                'warning': {
                    'title': "Warning", 'message': "Discount percent should be between -100 and 100!"
                },
            }

        if self.mrx_pricing_unit < 1 or self.mrx_pricing_unit > 1000000:
            return {
                'warning': {
                    'title': "Warning", 'message': "Pricing Unit should be between 1 and 1.000.000!"
                },
            }
        
        self.mrx_computed_purchase_price = (self.price / self.mrx_pricing_unit) * (1 - (self.mrx_discount or 0.0) / 100)
