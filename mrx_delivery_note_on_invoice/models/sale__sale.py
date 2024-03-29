# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        line = self.move_ids.filtered(lambda x: x.state == 'done' and x.picking_code == 'outgoing').sorted('reference', reverse=True)
        if line:
            res['mrx_delivery_note_reference'] = line[0].reference
        return res
