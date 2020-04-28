# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mrx_view_mods(models.Model):
#     _name = 'mrx_view_mods.mrx_view_mods'
#     _description = 'mrx_view_mods.mrx_view_mods'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
