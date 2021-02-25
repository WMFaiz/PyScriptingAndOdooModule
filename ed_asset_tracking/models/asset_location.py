# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError

class asset_location(models.Model):
    _name = 'asset.location'
    _description = 'asset.location'
    _rec_name = 'name'

    name = fields.Char(string='Location Name', required=True)
    location = fields.Many2one('res.company',string='Location')
    locCode = fields.Char(string='Location Code')
    companyName = fields.Char('name', related='location.name')
    counter = fields.Many2one('stock.warehouse' ,string='Counter')
    sales = fields.Boolean(string='Sales')
    scrap = fields.Boolean(string='Scrap')
    asset_asset = fields.Many2many('asset.asset',string='Asset', readonly=True)
    asset_ids = fields.One2many('asset.asset','location', string='Assets')

    @api.onchange('location')
    def onchange_location(self):
        if self.location.name != False and self.counter.name == False and self.scrap == False:
            self.name = str(self.location.name)
        elif self.counter.name != False and self.location.name == False and self.scrap == False:
            self.name = str(self.counter.name)
        elif self.location.name != False and self.counter.name != False and self.scrap == False:
            self.name = str(self.location.name) + '@' + str(self.counter.name)
        elif self.location.name != False and self.counter.name == False and self.scrap == True:
            self.name = str(self.location.name) + '@Scrap'
        elif self.location.name == False and self.counter.name != False and self.scrap == True:
            self.name = str(self.counter.name) + '@Scrap'
        elif self.location.name != False and self.counter.name != False and self.scrap == True:
            self.name = str(self.location.name) + '@' + str(self.counter.name) + '@Scrap'
        elif self.location.name == False and self.counter.name == False:
            self.name = False


        if str(self.name).find('False') >= 0:
            self.name = str(self.name).replace('False', '')

    @api.onchange('counter')
    def onchange_counter(self):
        if self.location.name != False and self.counter.name == False and self.scrap == False:
            self.name = str(self.location.name)
        elif self.counter.name != False and self.location.name == False and self.scrap == False:
            self.name = str(self.counter.name)
        elif self.location.name != False and self.counter.name != False and self.scrap == False:
            self.name = str(self.location.name) + '@' + str(self.counter.name)
        elif self.location.name != False and self.counter.name == False and self.scrap == True:
            self.name = str(self.location.name) + '@Scrap'
        elif self.location.name == False and self.counter.name != False and self.scrap == True:
            self.name = str(self.counter.name) + '@Scrap'
        elif self.location.name != False and self.counter.name != False and self.scrap == True:
            self.name = str(self.location.name) + '@' + str(self.counter.name) + '@Scrap'
        elif self.location.name == False and self.counter.name == False:
            self.name = False

        if str(self.name).find('False') >= 0:
            self.name = str(self.name).replace('False', '')

    @api.onchange('scrap')
    def onchange_scrap(self):
        if self.scrap == True and self.location.name == False and self.counter.name == False:
            self.name = 'Scrap'
        elif self.scrap == True and self.location.name != False and self.counter.name == False:
            self.name = str(self.name) + '@Scrap'
        elif self.scrap == True and self.location.name == False and self.counter.name != False:
            self.name = str(self.name) + '@Scrap'
        elif self.scrap == True and self.location.name != False and self.counter.name != False:
            self.name = str(self.name) + '@Scrap'
        elif self.scrap == False and self.location.name != False and self.counter.name != False:
            self.name = str(self.name).replace('@Scrap', '')
        elif self.scrap == False and self.location.name != False and self.counter.name == False:
            self.name = str(self.name).replace('@Scrap', '')
        elif self.scrap == False and self.location.name == False and self.counter.name != False:
            self.name = str(self.name).replace('@Scrap', '')
        elif self.scrap == False and self.location.name == False and self.counter.name == False:
            self.name = False

        if str(self.name).find('False') >= 0:
            self.name = str(self.name).replace('False', '')