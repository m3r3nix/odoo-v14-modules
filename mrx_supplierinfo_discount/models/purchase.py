# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare

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

    ## Inherited function: ../addons/purchase/models/purchase.py line 478 
    #  "mrx_pricing_unit" and "mrx_discount" has been added to the api.depends line. Also "price" and "taxes" lines have been changed
    #  Calculate taxes and subtotal properly from price with discount.
    @api.depends('product_qty', 'price_unit', 'taxes_id', 'mrx_discount', 'mrx_pricing_unit')
    def _compute_amount(self):
        for line in self:
            price = (line.price_unit / line.mrx_pricing_unit) * (1 - (line.mrx_discount or 0.0) / 100.0)
            taxes = line.taxes_id.compute_all(price, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    ## Inherited function: ../addons/purchase/models/purchase.py line 609
    #  See 2. comment inside...
    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0

        self._product_id_change()

        self._suggest_quantity()
        self._onchange_quantity()

        # Following code section has been added extra. Set discount and pricing unit from supplierinfo only when product_id changes
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order.date(),
            uom_id=self.product_uom)
        if not seller:
            self.mrx_discount = 0.0
            self.mrx_pricing_unit = 1
        else:
            self.mrx_discount = seller.mrx_discount
            self.mrx_pricing_unit = seller.mrx_pricing_unit

    ## Inherited function: ../addons/purchase/models/purchase.py line 657
    #  See comment inside...
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

        if not seller:
            if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
                self.price_unit = 0.0
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

    ## Inherited function: ../addons/purchase/models/purchase.py line 718
    #  "discount" and "mrx_pricing_unit" has been added to the return array
    def _prepare_account_move_line(self, move):
        self.ensure_one()
        if self.product_id.purchase_method == 'purchase':
            qty = self.product_qty - self.qty_invoiced
        else:
            qty = self.qty_received - self.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) <= 0:
            qty = 0.0

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        return {
            'name': '%s: %s' % (self.order_id.name, self.name),
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'purchase_line_id': self.id,
            'date_maturity': move.invoice_date_due,
            'product_uom_id': self.product_uom.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit / self.mrx_pricing_unit,
            'discount': self.mrx_discount,
#            Ha nem implementálom az invoice-ba akkor nem kell.
#            'mrx_pricing_unit': self.mrx_pricing_unit,
            'quantity': qty,
            'partner_id': move.partner_id.id,
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'display_type': self.display_type,
        }

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