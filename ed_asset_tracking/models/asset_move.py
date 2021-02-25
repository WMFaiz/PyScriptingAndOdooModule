# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from odoo.exceptions import Warning

class asset_move(models.Model):
    _name = 'asset.move'
    _description = 'asset.move'
    _rec_name = 'asset'

    from_location = fields.Many2one('asset.location',string='From Location', required=True)
    asset = fields.Many2one('asset.asset',string='Asset', required=True)
    to_Location = fields.Many2one('asset.location',string='To Location', required=True)
    status = fields.Char(string='Status', default='Custom')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')], string='State',track_visibility='onchange', default='draft', copy=False)

    @api.multi
    def move_asset_to_scrap(self):
        for move in self:
            move.asset.location = move.to_Location and move.to_Location.id or False
            move.state = 'done'
        return True

    @api.multi
    def move_asset_to_location(self, vals):
        for move in self:
            move.state = 'done'