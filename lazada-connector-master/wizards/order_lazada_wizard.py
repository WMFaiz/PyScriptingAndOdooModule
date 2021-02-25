# -*- coding: utf-8 -*-
import lazop
import requests
import webbrowser
import json
import base64
import urllib
import requests
from PIL import Image
from io import BytesIO
import xml.etree.ElementTree as ET
from datetime import datetime
from odoo import models, fields, api,  _


class order_lazada_wizard(models.TransientModel):
    _name = 'order.lazada.wizard'
    _description = 'Get Order Lazada Wizard'

    # Required
    dateStart = fields.Datetime(string='Date From', required=True)
    dateEnd = fields.Datetime(string='Date To', required=True)
    # FromWarehouse = fields.Many2one('stock.location', string='From Warehouse')
    # ToWarehouse = fields.Many2one('stock.location', string='To Warehouse')

    lazada_config = fields.Many2one('lazada.configuration', string="Authorization", required=True)
    URL = fields.Char('URL', related='lazada_config.URL', readonly=True)
    warehouse = fields.Many2one(string='Warehouse', related='lazada_config.warehouse', required=True)
    fromLocation = fields.Many2one('stock.location', string='From Location', required=True)
    toLocation = fields.Many2one(string='Stock Location', related='lazada_config.stockLocation', required=True)
    company = fields.Many2one(string='Company', related='lazada_config.company', required=True)
    prod_lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', domain="[('product_id','=',product_id)]")
    package_id = fields.Many2one('stock.quant.package', 'Pack', index=True)

    API_Key = fields.Char('API Key', related='lazada_config.API_Key', readonly=True)
    API_Secret = fields.Char('API Secret', related='lazada_config.API_Secret', readonly=True)
    API_Code = fields.Char('API Code', related='lazada_config.API_Code', readonly=True)
    API_Token = fields.Char('API Token', related='lazada_config.API_Token', readonly=True)
    # category = fields.Many2one('product.category', string='Category Product')
    
    # @api.onchange('lazada_config')
    # def test_sync(self):
    #     print(self.dateStart)
    #     print(self.dateEnd)
    #     print(self.lazada_config)
    #     print(self.URL)
    #     print(self.warehouse)
    #     print(self.fromLocation)
    #     print(self.toLocation)
    #     print(self.company)
    #     print(self.prod_lot_id)
    #     print(self.package_id)
    #     print(self.API_Key)
    #     print(self.API_Secret)
    #     print(self.API_Code)
    #     print(self.API_Token)

    @api.multi
    def Sync_product_lazada(self):
        formatFrom ="%Y-%m-%d %H:%M:%S"
        formatTo ="%Y-%m-%dT%H:%M:%S+0800"
        date_str_start = str(self.dateStart).split('.')[0]
        date_str_end = str(self.dateEnd).split('.')[0]
        date_GMT_start = datetime.strptime(date_str_start,formatFrom).strftime(formatTo)
        date_GMT_end = datetime.strptime(date_str_end,formatFrom).strftime(formatTo)

        #Enviroment
        productEnv = self.env['product.template']
        orderEnv = self.env['order.lazada'] 
        customerEnv = self.env['res.partner']
        saleEnv = self.env['sale.order']
        saleOrderEnv = self.env['sale.order.line']
        stockEnv = self.env['stock.inventory']
        moveEnv = self.env['stock.move']
        # stockLineEnv = self.env['stock.inventory.line']
        # stockQuantEnv = self.env['stock.quant']
        # stockLineEnv = self.env['product.product']

        #client
        client = lazop.LazopClient(self.URL, self.API_Key, self.API_Secret)

        #Products
        productRequest = lazop.LazopRequest('/products/get','GET')
        productRequest.add_api_param('offset', '0')
        productRequest.add_api_param('create_after', date_GMT_start)
        productRequest.add_api_param('create_before', date_GMT_end)
        # productRequest.add_api_param('update_after', date_GMT_start)
        # productRequest.add_api_param('update_before', date_GMT_end)
        productResponse = client.execute(productRequest,self.API_Token)
        products = productResponse.body["data"]["products"]
        #Product Looping
        for product in products:
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
            checkItem = productEnv.search([('item_id','=',item_id)])
            if checkItem.id == False:
                if link is None or link == "":
                    product_item = productEnv.create({
                        'name':name,
                        'LazadaProductName':name,
                        'item_id':item_id,
                        'shopsku':shopsku,
                        'SkuId':skuid,
                        'list_price': price,
                        # 'image_medium':link,
                        'PrimaryCategory':primary_category,
                        'Quantity':quantity,
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
                        'type':'product',
                        'company_id':self.company.id,
                        # 'property_stock_production':fromLocation.id,
                        # 'property_stock_inventory':fromLocation.id
                    })
                    stock = stockEnv.create({
                        'name': name + ' - ' + str(datetime.now()).split(".")[0],
                        'filter': 'product',
                        'product_id': product_item.id,
                        'state':'done',
                        'line_ids':[(0,0,{
                            'product_qty': quantity,
                            'location_id':self.fromLocation.id,
                            'product_id':product_item.id
                        })],
                        'move_ids':[(0,0,{
                            'name': _('INV:') + name,
                            'product_id': product_item.id,
                            'product_uom': 1,
                            'product_uom_qty': quantity,
                            'date': datetime.now(),
                            # 'company_id': self.company.id,
                            # # 'inventory_id': self.inventory_id.id,
                            'state': 'done',
                            # # 'restrict_partner_id': self.partner_id.id,
                            'location_id': self.fromLocation.id,
                            'location_dest_id': self.toLocation.id,
                            'move_line_ids': [(0, 0, {
                                'product_id': product_item.id,
                                'lot_id': self.prod_lot_id.id,
                                'product_uom_qty': 0,  # bypass reservation here
                                'product_uom_id': 1,
                                'qty_done': quantity,
                                # 'package_id': out and self.package_id.id or False,
                                'result_package_id': self.package_id.id or False,
                                'location_id': self.fromLocation.id,
                                'location_dest_id': self.toLocation.id,
                                # 'owner_id': self.partner_id.id,
                            })]
                        })]
                    })
                    # print(stock)
                else:
                    # r = requests.get(link)
                    # Image.open(BytesIO(r.content))
                    # profile_image = base64.encodestring(urllib.request.urlopen(link).read())
                    product_item = productEnv.create({
                        'name':name,
                        'LazadaProductName':name,
                        'item_id':item_id,
                        'shopsku':shopsku,
                        'SkuId':skuid,
                        'list_price': price,
                        # 'image_medium':profile_image,
                        'image_medium':"",
                        'PrimaryCategory':primary_category,
                        'Quantity':quantity,
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
                        'type':'product',
                        'company_id':self.company.id,
                        # 'property_stock_production':fromLocation.id,
                        # 'property_stock_inventory':fromLocation.id
                    })
                    stock = stockEnv.create({
                        'name': name + ' - ' + str(datetime.now()).split(".")[0],
                        'filter': 'product',
                        'product_id': product_item.id,
                        'state':'done',
                        'line_ids':[(0,0,{
                            'product_qty': quantity,
                            'location_id':self.fromLocation.id,
                            'product_id':product_item.id
                        })],
                        'move_ids':[(0,0,{
                            'name': _('INV:') + name,
                            'product_id': product_item.id,
                            'product_uom': 1,
                            'product_uom_qty': quantity,
                            'date': datetime.now(),
                            # 'company_id': self.company.id,
                            # # 'inventory_id': self.inventory_id.id,
                            'state': 'done',
                            # # 'restrict_partner_id': self.partner_id.id,
                            'location_id': self.fromLocation.id,
                            'location_dest_id': self.toLocation.id,
                            'move_line_ids': [(0, 0, {
                                'product_id': product_item.id,
                                'lot_id': self.prod_lot_id.id,
                                'product_uom_qty': 0,  # bypass reservation here
                                'product_uom_id': 1,
                                'qty_done': quantity,
                                # 'package_id': out and self.package_id.id or False,
                                'result_package_id': self.package_id.id or False,
                                'location_id': self.fromLocation.id,
                                'location_dest_id': self.toLocation.id,
                                # 'owner_id': self.partner_id.id,
                            })]
                        })]
                    })

        #Orders
        request = lazop.LazopRequest('/orders/get','GET')
        request.add_api_param('offset', '0')
        request.add_api_param('created_after', date_GMT_start)
        request.add_api_param('created_before', date_GMT_end)
        request.add_api_param("status", "pending");
        response = client.execute(request,self.API_Token)
        orders = response.body["data"]["orders"]

        #Orders Looping
        for order in orders:
            # general information
            voucher = order.get('voucher')
            warehouse_code = order.get('warehouse_code')
            order_number = order.get('order_number')
            created_at = order.get('created_at')
            voucher_code = order.get('voucher_code')
            gift_option = order.get('gift_option')
            shipping_fee_discount_platform = order.get('shipping_fee_discount_platform')
            customer_last_name = order.get('customer_last_name')
            updated_at = order.get('updated_at')
            promised_shipping_times = order.get('promised_shipping_times')
            price = order.get('price')
            national_registration_number = order.get('national_registration_number')
            shipping_fee_original = order.get('shipping_fee_original')
            payment_method = order.get('payment_method')
            customer_first_name = order.get('customer_first_name')
            shipping_fee_discount_seller = order.get('shipping_fee_discount_seller')
            branch_number = order.get('branch_number')
            tax_code = order.get('tax_code')
            delivery_info = order.get('delivery_info')
            statuses = order.get('statuses')[0]
            extra_attributes = order.get('extra_attributes')
            order_id = order.get('order_id')
            gift_message = order.get('gift_message')
            remarks = order.get('remarks')
            # address billing
            country_ab = order.get('address_billing').get('country')
            address3_ab = order.get('address_billing').get('address3')
            address2_ab = order.get('address_billing').get('address2')
            city_ab = order.get('address_billing').get('city')
            phone_ab = order.get('address_billing').get('phone')
            address1_ab = order.get('address_billing').get('address1')
            post_code_ab = order.get('address_billing').get('post_code')
            phone2_ab = order.get('address_billing').get('phone2')
            last_name_ab = order.get('address_billing').get('last_name')
            address5_ab = order.get('address_billing').get('address5')
            address4_ab = order.get('address_billing').get('address4')
            first_name_ab = order.get('address_billing').get('first_name')
            # address shipping
            country_as = order.get('address_shipping').get('country')
            address3_as = order.get('address_shipping').get('address3')
            address2_as = order.get('address_shipping').get('address2')
            city_as = order.get('address_shipping').get('city')
            phone_as = order.get('address_shipping').get('phone')
            address1_as = order.get('address_shipping').get('address1')
            post_code_as = order.get('address_shipping').get('post_code')
            phone2_as = order.get('address_shipping').get('phone2')
            last_name_as = order.get('address_shipping').get('last_name')
            address5_as = order.get('address_shipping').get('address5')
            address4_as = order.get('address_shipping').get('address4')
            first_name_as = order.get('address_shipping').get('first_name')

            customerName = first_name_ab+" "+last_name_ab
            street = address1_ab+", "+address2_ab+", "+address3_ab+", "+address4_ab+", "+address5_ab
            checkCustomer = customerEnv.search([('phone', '=', phone_ab)]) 
            if checkCustomer.id == True or checkCustomer.id > 0:
                partner_id = saleEnv.create({
                    'partner_id': checkCustomer.id,
                    'state': 'done',
                    'confirmation_date': datetime.now(),
                    'warehouse_id': self.warehouse.id,
                    # 'product_id': product.id,
                })
                request = lazop.LazopRequest('/order/items/get','GET')
                request.add_api_param('order_id', order_id)
                response = client.execute(request, self.API_Token)
                items = response.body["data"]
                for item in items:
                    getName = item.get('name')
                    getOrderId = item.get('order_id')
                    getOderItemId = item.get('order_item_id')
                    getItemPrice = item.get('item_price')
                    # print(getName, getOrderId, getOderItemId,getItemPrice )
                    checkItem = productEnv.search([('item_id','=',getOderItemId)])
                    if checkItem:
                        saleOrderEnv.create({
                            'product_id':checkItem.id,
                            'order_id':partner_id.id,
                            'order_partner_id':checkCustomer.id,
                        })
                    else:
                        itemId = productEnv.create({
                            'name':getName,
                            'LazadaProductName':getName,
                            'orderId':getOrderId,
                            'item_id':getOderItemId,
                            'list_price':getItemPrice,
                            'type':'product',
                            'company_id':self.company.id,
                            # 'property_stock_production':self.fromLocation.id,
                            # 'property_stock_inventory':self.fromLocation.id
                        })
                        stock = stockEnv.create({
                            'name': name + ' - ' + str(datetime.now()).split(".")[0],
                            'filter': 'product',
                            'product_id': itemId.id,
                            'state':'done',
                            'line_ids':[(0,0,{
                                'product_qty': quantity,
                                'location_id':self.fromLocation.id,
                                'product_id':itemId.id
                            })],
                            'move_ids':[(0,0,{
                                'name': _('INV:') + name,
                                'product_id': itemId.id,
                                'product_uom': 1,
                                'product_uom_qty': quantity,
                                'date': datetime.now(),
                                # 'company_id': self.company.id,
                                # # 'inventory_id': self.inventory_id.id,
                                'state': 'done',
                                # # 'restrict_partner_id': self.partner_id.id,
                                'location_id': self.fromLocation.id,
                                'location_dest_id': self.toLocation.id,
                                'move_line_ids': [(0, 0, {
                                    'product_id': itemId.id,
                                    'lot_id': self.prod_lot_id.id,
                                    'product_uom_qty': 0,  # bypass reservation here
                                    'product_uom_id': 1,
                                    'qty_done': quantity,
                                    # 'package_id': out and self.package_id.id or False,
                                    'result_package_id': self.package_id.id or False,
                                    'location_id': self.fromLocation.id,
                                    'location_dest_id': self.toLocation.id,
                                    # 'owner_id': self.partner_id.id,
                                })]
                            })]
                        })
                        saleOrderEnv.create({
                            'product_id':itemId.id,
                            'order_id':partner_id.id,
                            'order_partner_id':checkCustomer.id,
                        })
            elif checkCustomer.id == False:
                customerId = customerEnv.create({
                    'name': customerName,
                    'street': street,
                    'phone':phone_ab
                })
                partner_id = saleEnv.create({
                    'partner_id': customerId.id,
                    'state': 'done',
                    'confirmation_date': datetime.now(),
                    'warehouse_id': self.warehouse.id,
                    # 'product_id': product.id,
                })
                request = lazop.LazopRequest('/order/items/get','GET')
                request.add_api_param('order_id', order_id)
                response = client.execute(request, self.API_Token)
                items = response.body["data"]
                for item in items:
                    getName = item.get('name')
                    getOrderId = item.get('order_id')
                    getOderItemId = item.get('order_item_id')
                    getItemPrice = item.get('item_price')
                    # print(getName, getOrderId, getOderItemId,getItemPrice )
                    checkItem = productEnv.search([('item_id','=',getOderItemId)])
                    if checkItem:
                        saleOrderEnv.create({
                            'product_id':checkItem.id,
                            'order_id':partner_id.id,
                            'order_partner_id':checkCustomer.id,
                        })
                    else:
                        itemId = productEnv.create({
                            'name':getName,
                            'LazadaProductName':getName,
                            'orderId':getOrderId,
                            'item_id':getOderItemId,
                            'list_price':getItemPrice,
                            'type':'product',
                            'company_id':self.company.id,
                            # 'property_stock_production':self.fromLocation.id,
                            # 'property_stock_inventory':self.fromLocation.id
                        })
                        stock = stockEnv.create({
                            'name': name + ' - ' + str(datetime.now()).split(".")[0],
                            'filter': 'product',
                            'product_id': itemId.id,
                            'state':'done',
                            'line_ids':[(0,0,{
                                'product_qty': quantity,
                                'location_id':self.fromLocation.id,
                                'product_id':itemId.id
                            })],
                            'move_ids':[(0,0,{
                                'name': _('INV:') + name,
                                'product_id': itemId.id,
                                'product_uom': 1,
                                'product_uom_qty': quantity,
                                'date': datetime.now(),
                                # 'company_id': self.company.id,
                                # # 'inventory_id': self.inventory_id.id,
                                'state': 'done',
                                # # 'restrict_partner_id': self.partner_id.id,
                                'location_id': self.fromLocation.id,
                                'location_dest_id': self.toLocation.id,
                                'move_line_ids': [(0, 0, {
                                    'product_id': itemId.id,
                                    'lot_id': self.prod_lot_id.id,
                                    'product_uom_qty': 0,  # bypass reservation here
                                    'product_uom_id': 1,
                                    'qty_done': quantity,
                                    # 'package_id': out and self.package_id.id or False,
                                    'result_package_id': self.package_id.id or False,
                                    'location_id': self.fromLocation.id,
                                    'location_dest_id': self.toLocation.id,
                                    # 'owner_id': self.partner_id.id,
                                })]
                            })]
                        })
                        saleOrderEnv.create({
                            'product_id':itemId.id,
                            'order_id':partner_id.id,
                            'order_partner_id':checkCustomer.id,
                        })