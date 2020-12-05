# -*- coding: utf-8 -*-

from functools import partial
from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, get_lang

class SaleOrder(models.Model):
    _inherit = "sale.order"

    ## Inherited function: ../addons/sale/models/sale.py
    #  "total" calculation line has been changed only
    def _compute_amount_undiscounted(self):
        for order in self:
            total = 0.0
            for line in order.order_line:
                total += line.price_subtotal + (line.price_unit / line.mrx_pricing_unit) * (1 - (line.discount or 0.0) / 100.0) * line.product_uom_qty
            order.amount_undiscounted = total

    ## Inherited function: ../addons/sale/models/sale.py
    #  "price_reduce" line has been changed only
    def _amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                price_reduce = (line.price_unit / line.mrx_pricing_unit) * (1.0 - line.discount / 100.0)
                taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
                for tax in line.tax_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrx_pricing_unit = fields.Integer(string='Pricing Unit', default=1, required=True, store=True, help="How many items to get for this price? 1/10/100/1000")

    ## Inherited function: ../addons/sale/models/sale.py
    #  "mrx_pricing_unit" has been added to the api.depends line and "price" calculation line has been changed
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'mrx_pricing_unit')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = (line.price_unit / line.mrx_pricing_unit) * (1.0 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    ## Inherited function: ../addons/sale/models/sale.py
    #  "mrx_pricing_unit" has been added to the api.depends line and "price_reduce" line has been changed
    @api.depends('price_unit', 'discount', 'mrx_pricing_unit')
    def _get_price_reduce(self):
        for line in self:
            line.price_reduce = (line.price_unit / line.mrx_pricing_unit) * (1.0 - line.discount / 100.0)

    ## Inherited function: ../addons/sale/models/sale.py
    #  "Only "price_unit" has been updated in the returned array in order to generate proper sales invoice with pricing_unit
    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['price_unit'] = self.price_unit / self.mrx_pricing_unit
        return res

    ## Inherited function: ../addons/sale/models/sale.py
    #  Only "mrx_pricing_unit" line has been added extra
    @api.onchange('product_id')
    def product_id_change(self):
        if self.product_id:
            self.update({'mrx_pricing_unit' : self.product_id.mrx_pricing_unit})
        return super().product_id_change()
