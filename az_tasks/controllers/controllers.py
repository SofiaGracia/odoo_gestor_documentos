# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

# from odoo import http


# class AzExpedients(http.Controller):
#     @http.route('/az_expedients/az_expedients', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/az_expedients/az_expedients/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('az_expedients.listing', {
#             'root': '/az_expedients/az_expedients',
#             'objects': http.request.env['az_expedients.az_expedients'].search([]),
#         })

#     @http.route('/az_expedients/az_expedients/objects/<model("az_expedients.az_expedients"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('az_expedients.object', {
#             'object': obj
#         })
