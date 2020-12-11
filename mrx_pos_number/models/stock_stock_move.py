# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    mrx_pos_number_receipt = fields.Integer(related='purchase_line_id.mrx_pos_number', string='Pos.')
