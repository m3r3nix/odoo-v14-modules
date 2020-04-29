#-*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    mrx_po_ids = fields.Many2many('purchase.order', 'purchase_order_sale_order_rel', 'sale_order_id', 'purchase_order_id', readonly=True, store=True)
    
#    mrx_po_bill_ids = fields.Many2many()


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    mrx_so_ids = fields.Many2many('sale.order', 'purchase_order_sale_order_rel', 'purchase_order_id', 'sale_order_id', compute='_compute_so_po_ids', readonly=True, store=True)
    
    # Search for sales orders based on the origin field in PO
    @api.depends('origin')
    def _compute_so_po_ids(self):
        for line in self:
            if line.origin:
                line.mrx_so_ids = self.env['sale.order'].search([('name','=',line.origin.split(', '))])