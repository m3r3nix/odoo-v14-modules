# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mrx_pos_number = fields.Integer(compute='_compute_pos_number', string='Pos.', readonly=True)
    
    @api.depends('sequence', 'order_id')
    def _compute_pos_number(self):
#        if not self._origin:
        for order in self:
 #           mrx_order_id = order._origin.id
            pos_number = 1
            for line in order.order_line:
                line.mrx_pos_number = pos_number
                pos_number += 1


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrx_pos_number = fields.Integer(related='order_id.order_line.mrx_pos_number', string='Pos.', readonly=True)
    
#    @api.depends('sequence', 'order_id')
#    def _compute_pos_number(self):
#        if not self._origin:
#            for order in self.mapped('order_id'):
 #           mrx_order_id = order._origin.id
#                mrx_pos_number = 1
#                for line in self.order_id.order_line:
#                    line._origin.mrx_pos_number = mrx_pos_number
#                    mrx_pos_number += 1
#                else:
#                    mrx_line = line._origin
#                    mrx_line.mrx_pos_number = mrx_pos_number
#                    mrx_pos_number += 1

#    @api.onchange('sequence')
#    def _onchange_pos_number(self):
#        if self._origin
#            for order in self._origin.mapped('order_id'):
#                mrx_pos_number = 1
#                for line in order.order_line:
#                    line._origin.mrx_pos_number = mrx_pos_number
#                    mrx_pos_number += 1
#        else
#            for order in self.mapped('order_id'):
#                mrx_pos_number = 1
#                for line in order.order_line:
#                    line.mrx_pos_number = mrx_pos_number
#                    mrx_pos_number += 1