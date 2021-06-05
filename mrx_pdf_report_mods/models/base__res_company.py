# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    mrx_local_tax_id = fields.Char(string="Tax ID", store="True", help="Local Tax ID which is used domestically")
