# -*- coding: utf-8 -*-

from odoo import models, fields, api
#import logging
#_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mrx_so_profit = fields.Float(compute='_compute_mrx_so_profit', string="Profit", readonly=True, store=True)

    @api.depends('state', 'amount_untaxed', 'invoice_ids.state', 'mrx_po_ids.amount_untaxed', 'mrx_po_ids.state', 'mrx_po_ids.invoice_count', 'mrx_po_bill_ids.state')
    def _compute_mrx_so_profit(self):
        for record in self:
            if record.state != 'cancel':
                sum_so_bills = sum_po_bills = 0.0
                posted_invoices = record.invoice_ids.filtered(lambda move: move.state == 'posted')
#                _logger.warning("Sales Invoices are posted: %s:", posted_invoices)
                if posted_invoices:
                    for bill in posted_invoices:
                        sum_so_bills += bill.amount_untaxed
                else:
                    sum_so_bills = record.amount_untaxed
#                _logger.warning("SUM SO Invoices: %s:", sum_so_bills)
                if record.mrx_po_ids:
                    for po in record.mrx_po_ids:
                        if po.state == "purchase" or po.state == "done":
                            posted_invoices = po.invoice_ids.filtered(lambda move: move.state == 'posted')
#                            _logger.warning("Vendor Bills are posted: %s:", posted_invoices)
                            if posted_invoices:
                                for bill in posted_invoices:
                                    sum_po_bills += bill.amount_untaxed
                            else:
                                sum_po_bills += po.amount_untaxed
#                _logger.warning("SUM PO Invoices: %s:", sum_po_bills)
                record.mrx_so_profit = sum_so_bills - sum_po_bills
            else:
                record.mrx_so_profit = 0.0
#                _logger.warning("SO Canceled: %s:", record.mrx_so_profit)
