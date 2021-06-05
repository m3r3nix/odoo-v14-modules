# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Add extra filed to product template model
    intrastat_origin_country_code = fields.Char(related='intrastat_origin_country_id.code', string='Country Code', readonly=True, store=True, copy=True, size=2)
