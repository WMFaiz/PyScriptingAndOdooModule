# -*- coding: utf-8 -*-

import lazop
import requests
import webbrowser
import json
import base64
import urllib
import requests
import io
from PIL import Image
from io import BytesIO
import xml.etree.ElementTree as ET
from datetime import datetime
from odoo import models, fields, api,  _

# url = 'https://api.lazada.com.my/rest'
# appkey = '116869'
# appSecret = 'B5k0VSbhliemszkcwK3spfolsQrX7WHv'
# access_token = '50000601720iYFiqbtRfWggq8lVycKlR16701d88lvHusCG09urayqVrlVsqK0'

# url = 'https://api.lazada.com.my/rest'
# appkey = 'bv1stop'
# appSecret = 'passwd#123'

class lazada_configuration(models.Model):
    _name = 'lazada.configuration'
    _description = 'lazada.configuration'
    _rec_name = 'Shop_name'


    image = fields.Binary("Company Image", attachment=True,
        help="This field holds the image used as image for the asset, limited to 1024x1024px.")
    image_medium = fields.Binary("Company Logo", attachment=True,
        help="Medium-sized image of the asset. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved, "\
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    image_small = fields.Binary("Company image", attachment=True,
        help="Small-sized image of the asset. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")
    Shop_name = fields.Char(string='Shop Name', required=True)
    URL = fields.Char(string='Url', required=True)
    API_Key = fields.Char(string='API key', required=True)
    API_Secret = fields.Char(string='API Secret', required=True)
    warehouse = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    company = fields.Many2one('res.company', string='Company', required=True)
    stockLocation = fields.Many2one('stock.location', string='Stock Location', required=True)
    API_Code = fields.Char(string='API Code')
    API_Token = fields.Char(string='API Token')

    # @api.multi
    # def testMethods(self):
    #     test1 = self.image_medium
    #     test2 = base64.encodestring(test1)
    #     test3 = Image.open(io.BytesIO(test2))
    #     test3.show()
    #     test3.save("/home/bv_wmfaiz/.local/share/Odoo/addons/12.0/lazada-connector")

    @api.multi
    def Client(self):
        for rec in self:
            url = rec['URL']
            api_key = rec['API_Key']
            api_secret = rec['API_Secret']
            client = lazop.LazopClient(url, api_key, api_secret)
            return client

    @api.multi
    def lazada_connect(self):
        for rec in self:
            url = rec['URL']
            api_key = rec['API_Key']
            api_secret = rec['API_Secret']
            api_code = rec['API_Code']
            api_token = rec['API_Token']
            if api_token == False:
                productRequest = lazop.LazopRequest('/auth/token/create','GET')
                productRequest.add_api_param('code',api_code)
                productResponse = self.Client().execute(productRequest)
                convertJson = str(productResponse.body).replace("\'", "\"")
                responseJson = json.loads(convertJson)
                if 'InvalidCode' in str(responseJson):
                    webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
                    print('Code:','Need productRequest')
                else:
                    self.API_Token = responseJson.get('access_token')
                    print('Token:','Succesfuly')
            elif api_code == False:
                webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
                print('Code:','Need to productRequest')
            elif api_token == False and api_code == False:
                webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
                print('Code:','Need to productRequest')
            elif api_token is None and api_code is not None:
                productRequest = lazop.LazopRequest('/auth/token/create','GET')
                productRequest.add_api_param('code',api_code)
                productResponse = self.Client().execute(productRequest)
                convertJson = str(productResponse.body).replace("\'", "\"")
                responseJson = json.loads(convertJson)
                self.API_Token = responseJson.get('access_token')
                print('Token:','None')
            elif api_token is not None and api_code is not None:
                productRequest = lazop.LazopRequest('/product/item/get','GET')
                productResponse = self.Client().execute(productRequest, api_token)
                responseOut = str(productResponse.body)
                print(responseOut)
                if 'IllegalAccessToken' in responseOut or 'Unexpected internal' in responseOut:
                    productRequest = lazop.LazopRequest('/auth/token/refresh','GET')
                    productRequest.add_api_param('refresh_token', api_token)
                    productResponse = self.Client().execute(productRequest)
                    convertJson = str(productResponse.body).replace("\'", "\"")
                    responseJson = json.loads(convertJson)
                    self.API_Token = responseJson.get('refresh_token')
                    print('Token:','Refresh')
                else:
                    print('Token:','Valid')
            elif api_token is not None and api_code is None:
                webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
                print('Code:','Need to productRequest')

    @api.multi
    def lazada_token(self,url, api_key, api_secret, api_token):
        productRequest = lazop.LazopRequest('/product/item/get','GET')
        client = lazop.LazopClient(url, api_key, api_secret)
        productResponse = client.execute(productRequest, api_token)
        responseOut = str(productResponse.body)
        if 'IllegalAccessToken' in responseOut or 'Unexpected internal' in responseOut:
            productRequest = lazop.LazopRequest('/auth/token/refresh','GET')
            productRequest.add_api_param('refresh_token', api_token)
            productResponse = client.execute(productRequest)
            convertJson = str(productResponse.body).replace("\'", "\"")
            responseJson = json.loads(convertJson)
            self.API_Token = responseJson.get('refresh_token')
            return str(responseJson.get('refresh_token'))
        else:
            return api_token