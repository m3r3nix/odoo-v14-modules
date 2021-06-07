# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    ### Select vendor by cheapest purchase price in MTO
    # Override function from: ../addons/product/models/product.py
    # Only content of last bracket has been modified. Recordset sorted by "min_qty" and "mrx_computed_purchase_price"
    def _prepare_sellers(self, params=False):
        return self.seller_ids.filtered(lambda s: s.name.active).sorted(lambda s: (-s.min_qty, s.mrx_computed_purchase_price))

    # Override function from: ../addons/product/models/product.py
    # Only last line has been modified. Returned recordset sorted by "mrx_computed_purchase_price" instead of "price"
    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False):
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        res = self.env['product.supplierinfo']
        sellers = self._prepare_sellers(params)
        sellers = sellers.filtered(lambda s: not s.company_id or s.company_id.id == self.env.company.id)
        for seller in sellers:
            # Set quantity in UoM of seller
            quantity_uom_seller = quantity
            if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
                quantity_uom_seller = uom_id._compute_quantity(quantity_uom_seller, seller.product_uom)

            if seller.date_start and seller.date_start > date:
                continue
            if seller.date_end and seller.date_end < date:
                continue
            if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
                continue
            if float_compare(quantity_uom_seller, seller.min_qty, precision_digits=precision) == -1:
                continue
            if seller.product_id and seller.product_id != self:
                continue
            if not res or res.name == seller.name:
                res |= seller
        return res.sorted('mrx_computed_purchase_price')[:1]


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    # Add some extra fields to the model
    mrx_product_manufacturer = fields.Many2one(
        related='product_tmpl_id.mrx_product_manufacturer',
        readonly=True,
    )
    mrx_price_group = fields.Many2one(
        'mrx.vendor.discount',
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

    # If "price_group" is used, then get vendor's discount for the given price group
    def get_price_group_discount(self, line):
        if line.name and line.mrx_product_manufacturer and line.mrx_price_group and line.mrx_discount_type == 'price_group':
            return line.mrx_price_group.discount
        else:
            return 0.0

    # If "product_only" is used, then set discount to the typed in amount by the user
    def get_product_only_discount(self, line):
        return line.mrx_discount

    # Decide how to compute product discount: Net Price / Price Group / Product Only
    @api.depends('mrx_discount_type', 'mrx_price_group', 'mrx_price_group.discount')
    def _compute_discount(self):
        for line in self:
            method_name = 'get_' + str(line.mrx_discount_type) + '_discount'
            method = getattr(self, method_name)
            line.mrx_discount = method(line)

    # Compute purchase price based on the above specified criteria
    @api.depends('price', 'mrx_discount', 'mrx_pricing_unit', 'date_start', 'date_end')
    def _compute_purchase_price(self):
        for line in self:
            line.mrx_computed_purchase_price = (line.price / line.mrx_pricing_unit) * (1 - (line.mrx_discount or 0.0) / 100)
            line.product_tmpl_id._copy_best_purchase_price_to_cost()

    @api.onchange('product_tmpl_id')
    def _copy_product_values(self):
        if self.product_tmpl_id:
            self.mrx_packaging_unit = self.product_tmpl_id.mrx_packaging_unit
            self.mrx_pricing_unit = self.product_tmpl_id.mrx_pricing_unit
            self.price = self.product_tmpl_id.list_price
            self.min_qty = self.product_tmpl_id.mrx_moq

    @api.onchange('name')
    def _copy_price_group_value(self):
        if self.product_tmpl_id and self.name:
            self.mrx_price_group = self.env['mrx.vendor.discount'].search([('partner_id', '=', self.name.id), ('manufacturer_id', '=', self.mrx_product_manufacturer.id), ('name', '=', self.product_tmpl_id.mrx_price_group.name)], limit=1)
