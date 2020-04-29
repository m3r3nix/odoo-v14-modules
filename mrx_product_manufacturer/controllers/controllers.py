# -*- coding: utf-8 -*-
# from odoo import http


# class MrxManufacturer(http.Controller):
#     @http.route('/mrx_manufacturer/mrx_manufacturer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrx_manufacturer/mrx_manufacturer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrx_manufacturer.listing', {
#             'root': '/mrx_manufacturer/mrx_manufacturer',
#             'objects': http.request.env['mrx_manufacturer.mrx_manufacturer'].search([]),
#         })

#     @http.route('/mrx_manufacturer/mrx_manufacturer/objects/<model("mrx_manufacturer.mrx_manufacturer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrx_manufacturer.object', {
#             'object': obj
#         })
