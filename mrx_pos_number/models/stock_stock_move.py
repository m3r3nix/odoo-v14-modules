# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Add some extra fields to the model
    mrx_pos_number_delivery = fields.Integer(related='sale_line_id.mrx_pos_number', string='Pos.')
    mrx_pos_number_receipt = fields.Integer(related='purchase_line_id.mrx_pos_number', string='Pos.')
