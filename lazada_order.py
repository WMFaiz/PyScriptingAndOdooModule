import pyshopee
import requests
import lazop
import json
import sys
import base64
import urllib
import xml.etree.ElementTree as ET
from datetime import datetime

date_GMT_start = "2019-01-01T05:27:00+0800"
date_GMT_end = "2020-11-15T05:26:59+0800"

# Lazada Credentials
url = "https://api.lazada.co.th/rest"
key = "116869"
secret = "B5k0VSbhliemszkcwK3spfolsQrX7WHv"
token = "50000900104caBwT1046b228pBBTyIzjoBQvQsfY5ovEItERwjXhawiOywcIbW"

# GLOBAL VAR

HOST = "http://192.168.43.114:8001/"
SESSION_ID = "cacecb7f0d62856bfc1bb92eaf500cb35c1f77e6"

headers = {'Content-type': 'application/json'}

productEnv = HOST+'api/product.template/?session_id='+SESSION_ID
orderEnv = HOST+'api/order.lazada/?session_id='+SESSION_ID
customerEnv = HOST+'api/res.partner/?session_id='+SESSION_ID
saleEnv = HOST+'api/sale.order/?session_id='+SESSION_ID
saleOrderEnv = HOST+'api/sale.order.line/?session_id='+SESSION_ID
stockEnv = HOST+'api/stock.inventory/?session_id='+SESSION_ID
moveEnv = HOST+'api/stock.move/?session_id='+SESSION_ID
stockQuantEnv = HOST+'api/stock.quant/?session_id='+SESSION_ID

warehouse_id = "1"
company_id = "2"
# stockLocation = "33"

# From Location(Inventory Adjustment)
fromLocation = "5"
# ToLocation(Chic/Stock)
toLocation = "33"

# Download Lazada Products

client = lazop.LazopClient(url, key, secret)
productRequest = lazop.LazopRequest('/products/get','GET')
productRequest.add_api_param('offset', '0')
productRequest.add_api_param('create_after', date_GMT_start)
productRequest.add_api_param('create_before', date_GMT_end)
productRequest.add_api_param('update_after', date_GMT_start)
productRequest.add_api_param('update_before', date_GMT_end)
productResponse = client.execute(productRequest,token)
products = productResponse.body["data"]["products"]

# print(response.body)

# Product Looping
for product in products:
    name = product.get('attributes').get('name')
    brand = product.get('attributes').get('brand')
    short_description = product.get('attributes').get('short_description')
    skuid = product.get('skus')[0].get('SkuId')
    # link = product.get('skus')[0].get('Images')[0]
    link = None
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
    # print(item_id)

    checkItem_URL = productEnv+'&filter=[["item_id","=","'+str(item_id)+'"]]'

    params = {'query': '{id}'}

    response = requests.get(
        checkItem_URL,
        params=params
    )

    json_data = json.loads(response.text)
    # print(json_data)
    checkItem = json_data["result"]
    # print(checkItem)
    if not checkItem:
        # print("Not Found")
        print(item_id)
        if link is None or link == "":
            ProductData = {
                   "jsonrpc":"2.0",
                   "params":{
                      "data":{
                        'name':name,
                        'LazadaProductName':name,
                        'item_id':item_id,
                        'shopsku':shopsku,
                        'SkuId':skuid,
                        'list_price': price,
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
                        'company_id':company_id,
                      }
                   }
            }

            response = requests.post(
                productEnv,
                data=json.dumps(ProductData),
                headers=headers
            )

            json_data = json.loads(response.text)
            productID = json_data["result"]
            print(productID)

             # -----------------------------------

            # Update Quantity To Lazada

            checkItemQuan_URL = stockQuantEnv+'&filter=[["product_id","=",15], ["location_id","=",'+fromLocation+']]'
            params = {'query': '{quantity, reserved_quantity}'}

            response = requests.get(
                checkItemQuan_URL,
                params=params
            )

            json_data = json.loads(response.text)
            result = json_data["result"]
            # print(json_data)

            for product in result:
                quantity = product.get('quantity')
                reserved_quantity = product.get('reserved_quantity')
                newQuan = reserved_quantity - quantity
                print("NewQuantity: "+str(newQuan))

                ItemId = item_id

                Request = ET.Element('Request')
                product = ET.SubElement(Request, 'Product')
                skus = ET.SubElement(product, 'Skus')
                sku = ET.SubElement(skus, 'Sku')
                item_id = ET.SubElement(sku, 'ItemId')
                sku_id = ET.SubElement(sku, 'SkuId')
                seller_sku = ET.SubElement(sku, 'SellerSku')
                quantity = ET.SubElement(sku, 'Quantity')

                item_id.text = str(ItemId)
                sku_id.text = str(skuid)
                seller_sku.text = str(sellersku)
                quantity.text = str(newQuan)

                Request = ET.tostring(Request, encoding='unicode')
                payload = Request

                print("payload: "+str(payload))

    else:
        print("Found")

        # Update Quantity To Lazada

        # checkItemQuan_URL = stockQuantEnv+'&filter=[["product_id","=",15], ["location_id","=",'+fromLocation+']]'
        # params = {'query': '{quantity, reserved_quantity}'}
        #
        # response = requests.get(
        #     checkItemQuan_URL,
        #     params=params
        # )
        #
        # json_data = json.loads(response.text)
        # result = json_data["result"]
        # print(json_data)


        # for product in result:
        #     quantity = product.get('quantity')
        #     reserved_quantity = product.get('reserved_quantity')
        #     newQuan = reserved_quantity - quantity
        #     print("NewQuantity: "+str(newQuan))










































# Send Post Request REST API

# AUTH_URL = 'http://localhost:8001/api/sale.order/?session_id=494f79a296e19a081f362195c7977e1e9f698f4a'
#
# headers = {'Content-type': 'application/json'}
#
# data = {
#        "jsonrpc":"2.0",
#        "params":{
#           "data":{
#             "name": "AtomTest5",
#             "partner_id": 11,
#             "order_line":[
#                 [
#                     0,0,{
#                         "product_id": 28,
#                         "product_uom_qty": 2,
#                         "qty_delivered": 0,
#                         "price_unit": 2950.00
#                     }
#                 ], [
#                     0,0,{
#                         "product_id": 33,
#                         "product_uom_qty": 3,
#                         "qty_delivered": 0,
#                         "price_unit": 100.0
#                     }
#                 ]
#             ],
#             "state": "sale",
#             "confirmation_date": "2020-11-13 08:43:23",
#             "type_name": "Sales Order"
#           }
#        }
# }
#
# response = requests.post(
#     AUTH_URL,
#     data=json.dumps(data),
#     headers=headers
# )
#
# print(response)
