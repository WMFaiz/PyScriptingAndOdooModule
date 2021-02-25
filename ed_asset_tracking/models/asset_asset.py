# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from odoo.exceptions import Warning
from odoo import tools
from PIL import Image
import os
import io
from array import array

class asset_asset(models.Model):
    _name = 'asset.asset'
    _description = 'asset.asset'
    _rec_name = 'name'

    # @api.multi
    # def _get_default_location(self):
    #     obj = self.env['asset.location'].search([('warehouse','=',True)])
    #     if not obj:
    #         raise Warning(_("Please create asset location first"))
    #     loc = obj[0]
    #     return loc 

    name = fields.Char(string='Asset Name', required=True)
    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used as image for the asset, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of the asset. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved, "\
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
        help="Small-sized image of the asset. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")
    location = fields.Many2one('asset.location', string="Current Location", required=True)
    category = fields.Many2one('asset.category', string="Category")
    purchase_value = fields.Float(string='Purchase Value')
    asset_code = fields.Char(string='Asset Code')
    purchase_date = fields.Datetime(string='Purchase Date')
    model_name = fields.Char(string='Model Name')
    serial_no = fields.Char(string='Serial No')
    warranty_start = fields.Date(string='Warranty Start')
    warranty_end = fields.Date(string='Warranty End')
    manufacturer = fields.Char(string='Manufacturer')
    note = fields.Text(string='Internal Notes')
    status = fields.Char(string='Status', default='Active')
    state = fields.Selection([
        ('active', 'Active'),
        ('scrapped', 'Scrapped')], string='State',track_visibility='onchange', default='active', copy=False)
    tangible = fields.Boolean(string='Tangible')
    move_ids = fields.One2many('asset.move','asset', string='From Location')
    barcode = fields.Char(string='Barcode')
    rfid = fields.Char(string='RFID')

    # @api.multi
    # def convert_image(self):
    #     for data in self:
    #         print(type(data.image_medium))
    #         imageStream = io.BytesIO(data.image_medium)
    #         imageFile = Image.open(imageStream)
    #         imageSave = imageFile.save("/home/bv_wmfaiz/.local/share/Odoo/addons/12.0/ed_asset_tracking")
    #         print("imageFile.size=%s" % imageFile.size)
            

    @api.multi
    def move_to_scrap(self):
        for asset in self:
            location_obj = self.env['asset.location'].search([('scrap','=',True)])
            if not location_obj:
                raise Warning(_("Please set scrap location first"))
            move_vals = {
                'from_location' : asset.location.id,
                'asset' : asset.id,
                'to_Location' : location_obj.id,
                'status': 'Scrapped'
                }
            asset_move = self.env['asset.move'].create(move_vals)
            asset_move.move_asset_to_scrap()
            asset.location = location_obj.id
            asset.status = 'Scrapped'
            asset.state = 'scrapped'
        return True    