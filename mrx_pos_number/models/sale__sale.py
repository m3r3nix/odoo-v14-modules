# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrx_pos_number = fields.Integer(compute='_compute_pos_number', string='Pos.')

    def _compute_pos_number(self):
        counter = 1
        for line in self.order_id.order_line:
            line.mrx_pos_number = counter
            counter += 1

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['mrx_pos_number'] = self.mrx_pos_number
        return res
