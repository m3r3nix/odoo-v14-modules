# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrx_pos_number = fields.Integer(compute='_compute_pos_number', string='Pos.', readonly=True, store=True)
    
    @api.depends('sequence', 'order_id')
    def _compute_pos_number(self):
        for order in self.mapped('order_id'):
            mrx_pos_number = 1
            for line in order.order_line:
                line.mrx_pos_number = mrx_pos_number
                mrx_pos_number += 1
