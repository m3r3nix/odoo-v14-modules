# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    intrastat_origin_country_code = fields.Char(related='intrastat_origin_country_id.code', string='Country Code', readonly=True, size=2)