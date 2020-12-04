# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Own function. Triggers the recompute of "price_unit", "mrx_discount" and "mrx_pricing_unit" fields if the vendor changed on the PO.
    @api.onchange('partner_id')
    def _compute_discount_by_seller(self):
        for order in self:
            order.order_line._compute_discount_by_seller()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    mrx_discount = fields.Float(string='Discount (%)', default=0.0, digits='Discount', help="Discount percentage given by the supplier from the list price", store=True)
    mrx_pricing_unit = fields.Integer(string='Pricing Unit', default=1, help="How many units to get for the given list price", store=True)

    ## Inherited function: ../addons/purchase/models/purchase.py
    #  "mrx_pricing_unit" and "mrx_discount" has been added to the api.depends line
    @api.depends('product_qty', 'price_unit', 'taxes_id', 'mrx_discount', 'mrx_pricing_unit')
    def _compute_amount(self):
        super()._compute_amount()

    def _prepare_compute_all_values(self):
        self.ensure_one()
        res = super()._prepare_compute_all_values()
        res['price_unit'] = (self.price_unit / self.mrx_pricing_unit) * (1.0 - (self.mrx_discount or 0.0) / 100.0)
        return res

    ## Inherited function: ../addons/purchase/models/purchase.py
    # Set mrx_discount and mrx_pricing unit from supplierinfo when product_id changes
    @api.onchange('product_id')
    def onchange_product_id(self):
        super().onchange_product_id()
        self._compute_discount_by_seller()

    ## Inherited function: ../addons/purchase/models/purchase.py
    #  See 2nd comment inside...
    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order.date(),
            uom_id=self.product_uom,
            params=params)

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        # If not seller, use the standard price. It needs a proper currency conversion.
        if not seller:
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                self.product_id.standard_price,
                self.product_id.supplier_taxes_id,
                self.taxes_id,
                self.company_id,
            )
            if price_unit and self.order_id.currency_id and self.order_id.company_id.currency_id != self.order_id.currency_id:
                price_unit = self.order_id.company_id.currency_id._convert(
                    price_unit,
                    self.order_id.currency_id,
                    self.order_id.company_id,
                    self.date_order or fields.Date.today(),
                )
            self.price_unit = price_unit
            return

        # Following 3 lines have been added extra. Import list price from supplierinfo only when product_id changes
        if self.price_unit:
            price_unit = self.price_unit
        else:
            price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit

    ## Inherited function: ../addons/purchase/models/purchase.py line
    #  "discount" and "mrx_pricing_unit" has been added to the return array
    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=False)
        res.update({
            'discount': self.mrx_discount,
            'mrx_pricing_unit': self.mrx_pricing_unit,
        })
        return res

    ## Inherited function: ../addons/purchase/models/purchase.py
    #  Override original function in order to set value of discount and pricing unit fields on automatically generated PO.
    #  "mrx_discount" and "mrx_pricing_unit" has been added to the return array
    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, supplier, po):
        res = super()._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id, supplier, po)

        # This section has been copied from original function in order to set seller
        partner = supplier.name
        uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        seller = product_id.with_company(company_id)._select_seller(
            partner_id=partner,
            quantity=uom_po_qty,
            date=po.date_order and po.date_order.date(),
            uom_id=product_id.uom_po_id)

        res.update({
            'mrx_pricing_unit': seller.mrx_pricing_unit,
            'mrx_discount': seller.mrx_discount,
        })
        return res

    # Own function. Get value of "mrx_discount" and "mrx_pricing_unit" from supplierinfo if vendor is set.
    def _compute_discount_by_seller(self):
        for line in self:
            seller = line.product_id._select_seller(
                partner_id=line.partner_id,
                quantity=line.product_qty,
                date=line.order_id.date_order and line.order_id.date_order.date(),
                uom_id=line.product_uom)
            if not seller:
                line.price_unit = 0.0
                line.mrx_discount = 0.0
                line.mrx_pricing_unit = 1
            else:                
                line.price_unit = seller.price
                line.mrx_discount = seller.mrx_discount
                line.mrx_pricing_unit = seller.mrx_pricing_unit