# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from odoo.exceptions import Warning

class asset_category(models.Model):
    _name = 'asset.category'
    _description = 'asset.category'
    # _rec_name = 'name'

    name = fields.Char(string='Asset Category', required=True)
    category_no = fields.Char(string='Asset Category No.')