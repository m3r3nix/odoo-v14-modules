# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mrx_so_po_relation(models.Model):
#     _name = 'mrx_so_po_relation.mrx_so_po_relation'
#     _description = 'mrx_so_po_relation.mrx_so_po_relation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
