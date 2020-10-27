# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mrx_po_ids = fields.Many2many('purchase.order', 'purchase_order_sale_order_rel', 'sale_order_id', 'purchase_order_id', string="Purchase Orders", readonly=True, store=True)
    mrx_po_bill_ids = fields.Many2many('account.move', 'sale_order_purchase_order_bill_rel', 'sale_order_id', 'account_move_id', compute='_compute_po_bill_ids', string="Vendor Bills", readonly=True, store=True)

    # Search for po bills based on the origin field on invoice
    @api.depends('mrx_po_ids.invoice_count')
    def _compute_po_bill_ids(self):
        for record in self:
            po_names = []
            if record.mrx_po_ids:
                for line in record.mrx_po_ids:
                    po_names.append(line.name)
                result = self.env['account.move'].search([('invoice_origin','in',po_names)])
                record.mrx_po_bill_ids = result


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    mrx_so_ids = fields.Many2many('sale.order', 'purchase_order_sale_order_rel', 'purchase_order_id', 'sale_order_id', compute='_compute_so_po_ids', string="Sales Orders", readonly=True, store=True)
    mrx_so_bill_ids = fields.Many2many('account.move', 'purchase_order_sale_order_bill_rel', 'purchase_order_id', 'account_move_id', compute='_compute_so_bill_ids', string="Sales Bills", readonly=True, store=True)

    # Search for sales orders based on the origin field in PO
    @api.depends('origin')
    def _compute_so_po_ids(self):
        for line in self:
            if line.origin:
                line.mrx_so_ids = self.env['sale.order'].search([('name','in',line.origin.split(', '))])

    # Search for so bills based on the origin field on invoice
    @api.depends('mrx_so_ids.invoice_count')
    def _compute_so_bill_ids(self):
        for record in self:
            so_names = []
            if record.mrx_so_ids:
                for line in record.mrx_so_ids:
                    so_names.append(line.name)
                result = self.env['account.move'].search([('invoice_origin','in',so_names)])
                record.mrx_so_bill_ids = result