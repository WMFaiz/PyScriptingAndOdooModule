# -*- coding: utf-8 -*-
from odoo import http

# class EdAssetTracking(http.Controller):
#     @http.route('/ed_asset_tracking/ed_asset_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ed_asset_tracking/ed_asset_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ed_asset_tracking.listing', {
#             'root': '/ed_asset_tracking/ed_asset_tracking',
#             'objects': http.request.env['ed_asset_tracking.ed_asset_tracking'].search([]),
#         })

#     @http.route('/ed_asset_tracking/ed_asset_tracking/objects/<model("ed_asset_tracking.ed_asset_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ed_asset_tracking.object', {
#             'object': obj
#         })