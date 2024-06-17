# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

# from odoo import http


# class AzPadron(http.Controller):
#     @http.route('/az_padron/az_padron', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/az_padron/az_padron/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('az_padron.listing', {
#             'root': '/az_padron/az_padron',
#             'objects': http.request.env['az_padron.az_padron'].search([]),
#         })

#     @http.route('/az_padron/az_padron/objects/<model("az_padron.az_padron"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('az_padron.object', {
#             'object': obj
#         })
