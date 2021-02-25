# -*- coding: utf-8 -*-

import pyshopee
import lazop
import requests
from datetime import datetime, date
import xml.etree.ElementTree as ET 
import base64
import urllib
import requests
from PIL import Image
from io import BytesIO
from odoo import models, fields, api,  _
from odoo.exceptions import Warning

class ProductTemplateInherit(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    # lazada
    # lazada_dup_var = fields.Many2one('product.template', string='Name')
    PrimaryCategory = fields.Char(string='Primary Category *')
    LazadaProductName = fields.Char(string='Lazada Product Name  *')
    SPUId = fields.Char(string='SPU ID') 
    AssociatedSku = fields.Char(string='Associated SKU')
    # Name = fields.Char(string='Name *')
    short_description = fields.Char(string='Short Description *') 
    Brand = fields.Char(string='Brand *')
    Kid_years = fields.Char(string='Kid Years')
    delivery_option_sof = fields.Char(string='Delivery Option SOF')
    SellerSku = fields.Char(string='Seller SKU  *')
    Quantity = fields.Integer(string='Quantity')
    # Price = fields.Float(string='Price *')
    Color = fields.Char(string='Color *')
    CoreConstruction = fields.Char(string='Core Construction *')
    # LinenFabric = fields.Char(string='Linen Fabric *')
    # SalePrice = fields.Float(string='Sale Price')
    SaleStartDate = fields.Datetime(string='Sale Start Date')
    SaleEndDate = fields.Datetime(string='Sale End Date')
    Inventories = fields.Char(string='Inventories')
    Inventory = fields.Char(string='Inventory')
    Size = fields.Char(string='Size *')
    Package_length = fields.Float(string='Package Length *')
    Package_height = fields.Float(string='Package Height *')
    Package_weight = fields.Float(string='Package Weight *')
    Package_width = fields.Float(string='Package Width *')
    Package_content = fields.Char(string='Package Content *')
    # Image = fields.Char(string='Image')
    Model_ = fields.Char(string='Model')
    Long_description = fields.Char(string='Long Description')
    Product_description = fields.Char(string='Product Description')
    SpecialPrice = fields.Float(string='Special Price')
    Warranty_type = fields.Selection(selection=[
                                        ('No Warranty', 'No Warranty'),
                                        ('Local Manufacturer Warranty', 'Local Manufacturer Warranty'),
                                        ('International Manufacturer Warranty', 'International Manufacturer Warranty'),
                                        ('Local Supplier Warranty', 'Local Supplier Warranty'),
                                        ('International Seller Warranty', 'International Seller Warranty')
                                    ], string='Warranty Type', default='No Warranty')
    # Warranty_period = fields.Char(string='Warranty Period')
    Warranty_period = fields.Selection(selection=[
                                        ('None', 'None'),
                                        ('1 Month', '1 Month'),
                                        ('2 Month', '2 Month'),
                                        ('3 Month', '3 Month'),
                                        ('4 Month', '4 Month'),
                                        ('5 Month', '5 Month'),
                                        ('6 Month', '6 Month'),
                                        ('7 Month', '7 Month'),
                                        ('8 Month', '8 Month'),
                                        ('9 Month', '9 Month'),
                                        ('10 Month', '10 Month'),
                                        ('11 Month', '11 Month'),
                                        ('12 Month', '12 Month'),
                                        ('Others', 'Others')
                                    ], string='Warranty Period', default='None')
    Warranty_policy = fields.Char(string='Warranty Policy')

    item_id = fields.Char(string="Item ID")
    shopsku = fields.Char(string='Shop SKU')
    SkuId = fields.Char(string='SKU ID')
    orderId = fields.Char(string='Order ID')
    warehouse =  fields.Many2one('stock.warehouse',string='Warehouse')
    

    web_url = fields.Char(string="Image URL", copy=False)

    @api.onchange('web_url')
    def onchange_image(self):
        link = self.web_url
        if link:
            r = requests.get(link)
            Image.open(BytesIO(r.content))
            profile_image = base64.encodestring(urllib.request.urlopen(link).read())
            val = {
                'image_medium': profile_image
            }
            return {'value': val}

    # @api.multi
    # def testProduct(self):
    #     return {
    #         'name': 'My Window',
    #         'domain': [],
    #         'res_model': 'product.template',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'context': {},
    #         'target': 'new',
    #     }
 
    @api.multi
    def lazada_create(self):
        for rec in self:
            Name = rec['name']
            LazadaProductName = rec['LazadaProductName']
            SalesPrice = rec['list_price']
            Image = rec['web_url']
            date_rec_start = rec['SaleStartDate']
            date_rec_end = rec['SaleEndDate']
            # formatFrom ="%Y-%m-%d %H:%M:%S"
            # formatTo ="%Y-%m-%dT%H:%M:%S+08:00"
            date_str_start = str(date_rec_start).split('.')[0]
            date_str_end = str(date_rec_end).split('.')[0]
            # date_GMT_start = datetime.strptime(date_str_start,formatFrom).strftime(formatTo)
            # date_GMT_end = datetime.strptime(date_str_end,formatFrom).strftime(formatTo)
            Special_Price = rec['SpecialPrice']
            # print(Special_Price)
            print("")
            
            lazada_models = self.env['lazada.configuration'].search([])             
            url = lazada_models.mapped('URL')[0]
            appkey = lazada_models.mapped('API_Key')[0]
            appSecret = lazada_models.mapped('API_Secret')[0]
            appToken = lazada_models.mapped('API_Token')[0]
            # print(appToken)

            client = lazop.LazopClient(url, appkey ,appSecret)
            request = lazop.LazopRequest('/product/create')

            print(LazadaProductName)

            requestCat = lazop.LazopRequest('/product/category/suggestion/get','GET')
            requestCat.add_api_param('product_name', LazadaProductName)
            responseCat = client.execute(requestCat, appToken)
            print("")

            data = responseCat.body['data']
            catSuggest = data['categorySuggestions']
            print(catSuggest)
            print("")

            # for json_dict in catSuggest:
            #     for key,value in json_dict.items():
            #         print("{0} | {1}".format(key, value))
            #         # print("")
            # print("")

            catSuggestData = catSuggest[0]
            print(catSuggestData)
            print("")

            catPath = catSuggestData['categoryPath']
            catName = catSuggestData['categoryName']
            catId = catSuggestData['categoryId']

            PrimaryCategory = str(catId)

            if float(Special_Price) == 0.00 or float(Special_Price) == 0:
                SpecialPrice = ""
                date_str_start = ""
                date_str_end = ""
                # print(SpecialPrice)
                payload = self.lazada_create_form(PrimaryCategory,
                                              self.LazadaProductName,
                                              self.SPUId,
                                              self.AssociatedSku,
                                              self.short_description,
                                              self.Long_description,
                                              self.Product_description,
                                              self.Brand,
                                              self.Kid_years,
                                              self.Warranty_type,
                                              self.Warranty_period,
                                              self.Warranty_policy,
                                              self.Model_,
                                              self.SellerSku,
                                              str(self.Quantity),
                                              self.CoreConstruction,
                                              str(SalesPrice),
                                              str(SpecialPrice),
                                              date_str_start,
                                              date_str_end,
                                              self.Color,
                                              self.Size,
                                              str(self.Package_length),
                                              str(self.Package_height),
                                              str(self.Package_weight), 
                                              str(self.Package_width),
                                              self.Package_content,
                                              str(Image))
                print(payload)

            else:
                payload = self.lazada_create_form(PrimaryCategory,
                                            self.LazadaProductName,
                                            self.SPUId,
                                            self.AssociatedSku,
                                            self.short_description,
                                            self.Long_description,
                                            self.Product_description,
                                            self.Brand,
                                            self.Kid_years,
                                            self.Warranty_type,
                                            self.Warranty_period,
                                            self.Warranty_policy,
                                            self.Model_,
                                            self.SellerSku,
                                            str(self.Quantity),
                                            self.CoreConstruction,
                                            str(SalesPrice),
                                            str(self.SpecialPrice),
                                            date_str_start,
                                            date_str_end,
                                            self.Color,
                                            self.Size,
                                            str(self.Package_length),
                                            str(self.Package_height),
                                            str(self.Package_weight), 
                                            str(self.Package_width),
                                            self.Package_content,
                                            str(Image))
                print(payload)

            request.add_api_param('payload', payload)
            response = client.execute(request,appToken)

            print(response.body)

            code = response.body["code"]
            Details = "Create Product Failed: "+code
            
            if int(code) == 0:
                self.env.user.notify_success(message='Product Created')
            else:
                self.env.user.notify_danger(message=Details)
            # print(response.type)
            # print(response.body)

    # @api.multi
    # def lazada_test(self):
    #     for rec in self:
    #         name = rec['name'] 
    #         sales_price = rec['list_price'] 
    #         price = rec['standard_price'] 
    #         print("Name:",name)
    #         print("Sales Price:",sales_price)
    #         print("Price:",price)

    @api.multi
    def lazada_delete(self):
        for rec in self:
            sellerSku = rec['SellerSku']
            lazada_models = self.env['lazada.configuration'].search([])             
            url = lazada_models.mapped('URL')[0]
            appkey = lazada_models.mapped('API_Key')[0]
            appSecret = lazada_models.mapped('API_Secret')[0]
            appToken = lazada_models.mapped('API_Token')[0]
            client = lazop.LazopClient(url, appkey ,appSecret)
            request = lazop.LazopRequest('/product/remove')
            request.add_api_param('seller_sku_list', '[\"'+sellerSku+'\"]')
            response = client.execute(request, appToken)
            # print(response.type)
            # print(response.body)
            code = response.body["code"]
            Details = "Delete Product Failed: "+code
            print(code)
            
            if int(code) == 0:
                self.env.user.notify_success(message='Product Deleted')
            else:
                self.env.user.notify_danger(message=Details)

    @api.multi
    def lazada_update(self):
        for rec in self:
            Name = rec['name']
            SalesPrice = rec['list_price']
            Image = rec['web_url']
            date_rec_start = rec['SaleStartDate']
            date_rec_end = rec['SaleEndDate']
            formatFrom ="%Y-%m-%d %H:%M:%S"
            formatTo ="%Y-%m-%dT%H:%M:%S+08:00"
            date_str_start = str(date_rec_start).split('.')[0]
            date_str_end = str(date_rec_end).split('.')[0]
            # date_GMT_start = datetime.strptime(date_str_start,formatFrom).strftime(formatTo)
            # date_GMT_end = datetime.strptime(date_str_end,formatFrom).strftime(formatTo)
            Special_Price = rec['SpecialPrice']
            print(Special_Price)
            
            lazada_models = self.env['lazada.configuration'].search([])             
            url = lazada_models.mapped('URL')[0]
            appkey = lazada_models.mapped('API_Key')[0]
            appSecret = lazada_models.mapped('API_Secret')[0]
            appToken = lazada_models.mapped('API_Token')[0]
            # print(appToken)

            client = lazop.LazopClient(url, appkey ,appSecret)
            request = lazop.LazopRequest('/product/update')

            if float(Special_Price) == 0.00 or float(Special_Price) == 0:
                SpecialPrice = ""
                date_str_start = ""
                date_str_end = ""
                # print(SpecialPrice)
                payload = self.lazada_create_form(self.PrimaryCategory,
                                              Name,
                                              self.SPUId,
                                              self.AssociatedSku,
                                              self.short_description,
                                              self.Long_description,
                                              self.Product_description,
                                              self.Brand,
                                              self.Kid_years,
                                              self.Warranty_type,
                                              self.Warranty_period,
                                              self.Warranty_policy,
                                              self.Model_,
                                              self.SellerSku,
                                              str(self.Quantity),
                                              self.CoreConstruction,
                                              str(SalesPrice),
                                              str(SpecialPrice),
                                              date_str_start,
                                              date_str_end,
                                              self.Color,
                                              self.Size,
                                              str(self.Package_length),
                                              str(self.Package_height),
                                              str(self.Package_weight), 
                                              str(self.Package_width),
                                              self.Package_content,
                                              str(Image))
                print(payload)

            else:
                payload = self.lazada_create_form(self.PrimaryCategory,
                                            Name,
                                            self.SPUId,
                                            self.AssociatedSku,
                                            self.short_description,
                                            self.Long_description,
                                            self.Product_description,
                                            self.Brand,
                                            self.Kid_years,
                                            self.Warranty_type,
                                            self.Warranty_period,
                                            self.Warranty_policy,
                                            self.Model_,
                                            self.SellerSku,
                                            str(self.Quantity),
                                            self.CoreConstruction,
                                            str(SalesPrice),
                                            str(self.SpecialPrice),
                                            date_str_start,
                                            date_str_end,
                                            self.Color,
                                            self.Size,
                                            str(self.Package_length),
                                            str(self.Package_height),
                                            str(self.Package_weight), 
                                            str(self.Package_width),
                                            self.Package_content,
                                            str(Image))
                print(payload)

            
            request.add_api_param('payload', payload)
            response = client.execute(request,appToken)
            print(response.type)
            print(response.body)

            code = response.body["code"]
            Details = "Update Product Failed: "+code
            # # message = response.body["detail"]
            # # message = response.body["message"]
            # # detail_1 = response.body["detail"][0]["field"]
            # # detail_2 = response.body["detail"][0]["message"]
            # # Details = detail_1+": "+detail_2
            # print(code)
            # # print(message)
            # # print(detail_1)
            # # print(detail_2)
            # # print(detail_1+": "+detail_2)
            
            if int(code) == 0:
                self.env.user.notify_success(message='Product Updated')
            else:
                self.env.user.notify_danger(message=Details)

    # @api.one
    def lazada_create_form(self,PrimaryCategory,LazadaProductName,SPUId,AssociatedSku,short_description,Long_description,Product_description,Brand,Kid_years,Warranty_type,Warranty_period,Warranty_policy,Model_,SellerSku,Quantity,CoreConstruction,Price,SpecialPrice,SaleStartDate,SaleEndDate,Color,Size,Package_length,Package_height,Package_weight,Package_width,Package_content,url):

        Request = ET.Element('Request')
        product = ET.SubElement(Request, 'Product')
        primary_category = ET.SubElement(product, 'PrimaryCategory')
        spu_id = ET.SubElement(product, 'SPUId')
        assoc_sku = ET.SubElement(product, 'AssociatedSku')
        attr = ET.SubElement(product, 'Attributes')
        # --->more here
        name = ET.SubElement(attr, 'name')
        short_desc = ET.SubElement(attr, 'short_description')
        long_desc = ET.SubElement(attr,'description')
        prod_desc = ET.SubElement(attr,'product_description')
        brand = ET.SubElement(attr, 'brand')
        model = ET.SubElement(attr, 'model')
        kid_years = ET.SubElement(attr, 'kid_years')
        warranty_type = ET.SubElement(attr, 'warranty_type')
        warranty_period = ET.SubElement(attr, 'warranty_period')
        warranty_policy = ET.SubElement(attr, 'warranty_policy')
        # <---end
        skus = ET.SubElement(product, 'Skus')
        sku = ET.SubElement(skus, 'Sku')
        # --->more here
        seller_sku = ET.SubElement(sku, 'SellerSku')
        color_family = ET.SubElement(sku, 'color_family')
        size = ET.SubElement(sku, 'size')
        quantity = ET.SubElement(sku, 'quantity')
        # core_construction = ET.SubElement(attr, 'Core_Construction')
        core_construction = ET.SubElement(sku, 'Core_Construction')
        # =======
        # linen_fabric = ET.SubElement(sku, 'Linen_Fabric')
        # filling = ET.SubElement(sku, 'Filling')
        # =======
        price = ET.SubElement(sku, 'price')
        spec_price = ET.SubElement(sku, 'special_price')
        spec_from_date = ET.SubElement(sku, 'special_from_date')
        spec_to_date = ET.SubElement(sku, 'special_to_date')
        package_length = ET.SubElement(sku, 'package_length')
        package_height = ET.SubElement(sku, 'package_height')
        package_weight = ET.SubElement(sku, 'package_weight')
        package_width = ET.SubElement(sku, 'package_width')
        package_content = ET.SubElement(sku, 'package_content')
        Images = ET.SubElement(sku, 'Images')
        Image = ET.SubElement(Images, 'Image')



        # # DATA PUSH TEST
        # primary_category.text = "1811"
        # # print(primary_category)
        # # ATTRIBUTES
        # name.text = "Sweater"
        # short_desc.text = "shortDesc"
        # brand.text = "No Brand"
        # model.text = "model"
        # kid_years.text = "5 - 10 Years"
        # # SKU
        # seller_sku.text = "fikri-api-test"
        # color_family.text = "RED"
        # size.text = "10"
        # quantity.text = "8"
        # price.text = "28.00"
        # package_length.text = "20"
        # package_height.text = "10"
        # package_weight.text = "3"
        # package_width.text = "6"
        # package_content.text = "content"
        # Image.text = "https://png.pngtree.com/png-clipart/20190516/original/pngtree-phantom-esports-logo-design-for-gaming-mascot-or-twitch-png-image_4261649.jpg"
        Image.text = url
        # linen_fabric.text = "Knitted"
        # filling.text = "Inner Spring/Coil"
        # dummy = "Look Here: "

        primary_category.text = PrimaryCategory
        spu_id.text = SPUId
        assoc_sku.text = AssociatedSku
        # SPUId.text = SPUId
        # AssociatedSku.text = AssociatedSku
        name.text = LazadaProductName
        short_desc.text = short_description
        long_desc.text = Long_description
        prod_desc.text = Product_description
        brand.text = Brand
        kid_years.text = Kid_years
        model.text = Model_
        # delivery_option_sof.text = delivery_option_sof
        seller_sku.text = SellerSku
        quantity.text = Quantity
        core_construction.text = CoreConstruction
        price.text = Price
        spec_price.text = SpecialPrice
        spec_from_date.text = SaleStartDate
        spec_to_date.text = SaleEndDate
        color_family.text = Color
        size.text = Size
        # SalePrice.text = SalePrice
        # SaleStartDate.text = SaleStartDate
        # SaleEndDate.text = SaleEndDate
        # Inventories.text = Inventories
        # Inventory.text = Inventory
        # WarehouseCode.text = WarehouseCode
        # Quantity.text = Quantity
        package_length.text = Package_length
        package_height.text = Package_height
        package_weight.text = Package_weight
        package_width.text = Package_width
        package_content.text = Package_content
        warranty_type.text = Warranty_type
        warranty_period.text = Warranty_period
        warranty_policy.text = Warranty_policy


        # Image.text = Image

        Request = ET.tostring(Request, encoding='unicode')

        return Request
