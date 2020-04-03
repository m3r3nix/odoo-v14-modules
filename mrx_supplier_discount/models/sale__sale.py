# -*- coding: utf-8 -*-

from functools import partial
from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, get_lang

class ProductTemplate(models.Model):
    _inherit = "product.template"

    mrx_pricing_unit = fields.Integer(string='Pricing Unit', default=1, required=True, store=True, help="How many items to get for this price? 1/10/100/1000")
    mrx_packaging_unit = fields.Integer(string='Packaging Unit', default=1, required=True, store=True, help="How many pieces in one package?")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    ## Inherited function: ../addons/sale/models/sale.py line 314
    #  "total" calculation line has been changed only
    def _compute_amount_undiscounted(self):
        for order in self:
            total = 0.0
            for line in order.order_line:
                total += line.price_subtotal + (line.price_unit / line.mrx_pricing_unit) * (1 - (line.discount or 0.0) / 100.0) * line.product_uom_qty
            order.amount_undiscounted = total

    ## Inherited function: ../addons/sale/models/sale.py line 816
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

    ## Inherited function: ../addons/sale/models/sale.py line 1015
    #  "mrx_pricing_unit" has been added to the api.depends line and "price" calculation line has been changed
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'mrx_pricing_unit')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = (line.price_unit / line.mrx_pricing_unit) * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    ## Inherited function: ../addons/sale/models/sale.py line 1070
    #  "mrx_pricing_unit" has been added to the api.depends line and "price_reduce" line has been changed
    @api.depends('price_unit', 'discount', 'mrx_pricing_unit')
    def _get_price_reduce(self):
        for line in self:
            line.price_reduce = (line.price_unit / line.mrx_pricing_unit) * (1.0 - line.discount / 100.0)

    ## Inherited function: ../addons/sale/models/sale.py line 1396
    #  "Only mrx_pricing_unit" has been added to the return array in order to generate proper sales invoice
    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.
        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit / self.mrx_pricing_unit,
#            'mrx_pricing_unit': self.mrx_pricing_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.display_type:
            res['account_id'] = False
        return res

    ## Inherited function: ../addons/sale/models/sale.py line 1460
    #  Only "mrx_pricing_unit" line has been added extra
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        # This line has been added extra
        self.mrx_pricing_unit = product.mrx_pricing_unit

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result