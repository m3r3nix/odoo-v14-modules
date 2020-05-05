# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mrx_so_profit = fields.Float(compute='_compute_mrx_so_profit', string="Profit", readonly=True, store=True)

    @api.depends('amount_untaxed', 'invoice_ids', 'invoice_ids.state', 'mrx_po_ids', 'mrx_po_ids.state', 'mrx_po_ids.invoice_count', 'mrx_po_bill_ids', 'mrx_po_bill_ids.state')
    def _compute_mrx_so_profit(self):
        for record in self:
            sum_so_bills = sum_po_bills = 0.0
            if record.invoice_status == "invoiced" and record.invoice_ids:
                for bill in record.invoice_ids:
                    if bill.state == "posted":
                        sum_so_bills += bill.amount_untaxed
#                    else:
#                        break
            else:
                sum_so_bills = record.amount_untaxed
            if record.mrx_po_ids:
                for po in record.mrx_po_ids:
                    if po.state == "purchase" or po.state == "done":
                        if po.invoice_status == "invoiced" and po.invoice_ids:
                            for bill in po.invoice_ids:
                                if bill.state == "posted":
                                    sum_po_bills += bill.amount_untaxed
                        else:
                            sum_po_bills += po.amount_untaxed
            record.mrx_so_profit = sum_so_bills - sum_po_bills

# Hozzá kell adni a po_bill_ids-t az SO-hoz, hogy a po_bill-ek state-jére is tudjam triggerelni a számolást
# po_bill_ids talán új tab-ra, ha nem mutat jól...
#
#
#for record in self:
#  sum_so_bills = sum_po_bills = 0.0
#  if record.invoice_ids:
#    for bill in record.invoice_ids:
#      if bill.state == "open" or bill.state == "paid":
#        sum_so_bills += bill.amount_untaxed
#  else:
#    sum_so_bills = record.amount_untaxed
#  if record.x_studio_field_po_ids:
#    for po in record.x_studio_field_po_ids:
#      if po.state == "purchase" or po.state == "done":
#        if po.invoice_status == "invoiced" and po.invoice_ids:
#          for bill in po.invoice_ids:
#            sum_po_bills += bill.amount_untaxed
#        else:
#          sum_po_bills += po.amount_untaxed
#  record['x_studio_profit'] = sum_so_bills - sum_po_bills