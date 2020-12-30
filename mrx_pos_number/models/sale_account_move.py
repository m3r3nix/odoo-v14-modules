# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mrx_pos_number = fields.Integer(compute='_compute_pos_number', string='Pos.')

    def _compute_pos_number(self):
        counter = 1
        for line in self.move_id.invoice_line_ids:
            line.mrx_pos_number = counter
            counter += 1
