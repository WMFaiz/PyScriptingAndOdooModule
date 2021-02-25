# -*- coding: utf-8 -*-
from odoo import http

# class Shopee(http.Controller):
#     @http.route('/shopee/shopee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shopee/shopee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shopee.listing', {
#             'root': '/shopee/shopee',
#             'objects': http.request.env['shopee.shopee'].search([]),
#         })

#     @http.route('/shopee/shopee/objects/<model("shopee.shopee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shopee.object', {
#             'object': obj
#         })