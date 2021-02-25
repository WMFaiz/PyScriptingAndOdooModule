import pyshopee
import requests
import lazop
import json
import base64
import urllib
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime, date
from odoo import models, fields, api,  _
from odoo.exceptions import Warning

class Product_Lazada(models.Model):
    _name = 'product.lazada'

    name = fields.Char(string='Name')
    skuid = fields.Char(string='Sku Id')
    sellersku = fields.Char(string='Seller Sku')
    shopsku = fields.Char(string='Shop Sku')
    price = fields.Char(string='Price')
    quantity = fields.Char(string='Quantity')
    available = fields.Char(string='Available')
    primary_category = fields.Char(string='Primary Category')
    item_id = fields.Char(string='Item ID')
    dateStart = fields.Datetime(string='Date Time Start', required=True)
    dateEnd = fields.Datetime(string='Date Time End', required=True)

    @api.multi
    def download_product_lazada(self):
        for rec in self:
            date_rec_start = rec['dateStart']
            date_rec_end = rec['dateEnd']
            formatFrom ="%Y-%m-%d %H:%M:%S"
            formatTo ="%Y-%m-%dT%H:%M:%S+0800"
            date_str_start = str(date_rec_start).split('.')[0]
            date_str_end = str(date_rec_end).split('.')[0]
            date_GMT_start = datetime.strptime(date_str_start,formatFrom).strftime(formatTo)
            date_GMT_end = datetime.strptime(date_str_end,formatFrom).strftime(formatTo)
            lazada_rec = self.env['lazada.configuration'].search([])
            url = lazada_rec.mapped('URL')[0]
            key = lazada_rec.mapped('API_Key')[0]
            secret = lazada_rec.mapped('API_Secret')[0]
            token = lazada_rec.mapped('API_Token')[0]
            # print('url:', url)
            # print('key:', key)
            # print('secret:', secret)
            # print('token:', token)
            # lazada_token = self.lazada_token(url, key, secret, token)
            client = lazop.LazopClient(url, key, secret)
            request = lazop.LazopRequest('/products/get','GET')
            request.add_api_param('offset', '0')
            request.add_api_param('create_after', date_GMT_start)
            request.add_api_param('create_before', date_GMT_end)
            request.add_api_param('update_after', date_GMT_start)
            request.add_api_param('update_before', date_GMT_end)
            # request.add_api_param('limit', '1')
            response = client.execute(request,token)
            # total_products = response.body["data"]["total_products"]
            # print(response.body)
            # productEnv = self.env['product.lazada']
            productEnv = self.env['product.template']
            products = response.body["data"]["products"]
            for product in products:
            #     # skus = product.get('skus')
                name = product.get('attributes').get('name')
                brand = product.get('attributes').get('brand')
                short_description = product.get('attributes').get('short_description')
                skuid = product.get('skus')[0].get('SkuId')
                link = product.get('skus')[0].get('Images')[0]
                package_content = product.get('skus')[0].get('package_content')
                SalePrice = product.get('skus')[0].get('SalePrice')
                color_family = product.get('skus')[0].get('color_family')
                price = product.get('skus')[0].get('price')
                sellersku = product.get('skus')[0].get('SellerSku')
                shopsku = product.get('skus')[0].get('ShopSku')
                price = product.get('skus')[0].get('price')
                quantity = product.get('skus')[0].get('quantity')
                available = product.get('skus')[0].get('Available')
                package_length = product.get('skus')[0].get('package_length')
                package_weight = product.get('skus')[0].get('package_weight')
                package_width = product.get('skus')[0].get('package_width')
                package_height = product.get('skus')[0].get('package_height')
                primary_category = product.get('primary_category')
                item_id = product.get('item_id')
                checkItem = self.env['product.template'].search([('item_id','=',item_id)])
                if checkItem.id == False:
                    if link is None or link == "":
                        productEnv.create({
                            'name':name,
                            'item_id':item_id,
                            'shopsku':shopsku,
                            'SkuId':skuid,
                            'list_price': price,
                            'image_medium':link,
                            'PrimaryCategory':primary_category,
                            'web_url':link,
                            'Brand': brand,
                            'Color':color_family,
                            'short_description':short_description,
                            'Package_content':package_content,
                            'SellerSku':sellersku,
                            'Package_length':package_length,
                            'Package_height':package_height,
                            'Package_weight':package_weight,
                            'Package_width':package_width,
                        })
                    else:
                        r = requests.get(link)
                        Image.open(BytesIO(r.content))
                        profile_image = base64.encodestring(urllib.request.urlopen(link).read())
                        productEnv.create({
                                'name':name,
                                'item_id':item_id,
                                'shopsku':shopsku,
                                'SkuId':skuid,
                                'list_price': price,
                                'image_medium':profile_image,
                                'PrimaryCategory':primary_category,
                                'web_url':link,
                                'Brand': brand,
                                'Color':color_family,
                                'short_description':short_description,
                                'Package_content':package_content,
                                'SellerSku':sellersku,
                                'Package_length':package_length,
                                'Package_height':package_height,
                                'Package_weight':package_weight,
                                'Package_width':package_width,
                            })
    @api.one
    def lazada_token(self,url, api_key, api_secret, api_token):
        request = lazop.LazopRequest('/product/item/get','GET')
        client = lazop.LazopClient(url, api_key, api_secret)
        response = client.execute(request, api_token)
        responseOut = str(response.body)
        if 'IllegalAccessToken' in responseOut or 'Unexpected internal' in responseOut:
            request = lazop.LazopRequest('/auth/token/refresh','GET')
            request.add_api_param('refresh_token', api_token)
            response = client.execute(request)
            convertJson = str(response.body).replace("\'", "\"")
            responseJson = json.loads(convertJson)
            return responseJson.get('refresh_token')
        else:
            return api_token