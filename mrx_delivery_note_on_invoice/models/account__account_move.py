# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mrx_delivery_note_reference = fields.Char(string='Delivery Note', store=True)
