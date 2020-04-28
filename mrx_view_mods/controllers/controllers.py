# -*- coding: utf-8 -*-
# from odoo import http


# class MrxViewMods(http.Controller):
#     @http.route('/mrx_view_mods/mrx_view_mods/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrx_view_mods/mrx_view_mods/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrx_view_mods.listing', {
#             'root': '/mrx_view_mods/mrx_view_mods',
#             'objects': http.request.env['mrx_view_mods.mrx_view_mods'].search([]),
#         })

#     @http.route('/mrx_view_mods/mrx_view_mods/objects/<model("mrx_view_mods.mrx_view_mods"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrx_view_mods.object', {
#             'object': obj
#         })
