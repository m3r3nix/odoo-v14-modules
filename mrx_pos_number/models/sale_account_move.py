# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mrx_pos_number = fields.Integer(string='Pos.', store=True)

    # def _compute_pos_number(self):
    #     # if not self.move_id.invoice_origin:
    #         counter = 1
    #         for line in self.move_id.invoice_line_ids:
    #             line.mrx_pos_number = counter
    #             counter += 1
