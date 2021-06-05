# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    mrx_pos_number = fields.Integer(compute='_compute_pos_number', string='Pos.')

    def _compute_pos_number(self):
        counter = 1
        for line in self.order_id.order_line:
            line.mrx_pos_number = counter
            counter += 1
