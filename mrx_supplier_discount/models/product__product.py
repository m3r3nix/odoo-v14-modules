# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import float_compare


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Add some extra fields to the model
    mrx_pricegroup = fields.Many2one('mrx.manufacturer.pricegroup', string='Price Group', store=True, help="Price group or product group provided by the manufacture")
    mrx_pricing_unit = fields.Integer(string='Pricing Unit', default=1, required=True, store=True, help="How many items to get for this price? 1/10/100/1000")
    mrx_packaging_unit = fields.Integer(string='Packaging Unit', default=1, required=True, store=True, help="How many pieces in one package?")
    mrx_moq = fields.Integer(string='MOQ', default=1, required=True, store=True, help="Minimum order quantity")

    @api.onchange('mrx_pricegroup')
    def _fill_category_if_same_as_price_group(self):
        if self.mrx_pricegroup:
            category_id = self.env['product.category'].search([('parent_id.name', '=', self.mrx_product_manufacturer.name), ('name', '=', self.mrx_pricegroup.name)], limit=1)
            if category_id:
                self.categ_id = category_id


class ProductProduct(models.Model):
    _inherit = "product.product"

    ### Select vendor by cheapest purchase price in MTO
    # Override function from: ../addons/product/models/product.py
    # Only content of last bracket has been modified. Recordset sorted by "min_qty" and "mrx_computed_purchase_price"
    def _prepare_sellers(self, params=False):
        # This search is made to avoid retrieving seller_ids from the cache.
        return self.env['product.supplierinfo'].search([('product_tmpl_id', '=', self.product_tmpl_id.id),
                                                        ('name.active', '=', True)]).sorted(lambda s: (-s.min_qty, s.mrx_computed_purchase_price))

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
