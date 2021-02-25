import lazop
import requests
import webbrowser
import json
import base64
import urllib
import requests
from PIL import Image
from io import BytesIO
import sched, time
import xmlrpc
from datetime import datetime, date
from dateutil.relativedelta import *
from xmlrpc import client as xmlrpclib
import urllib.request, urllib.parse, urllib.error

s = sched.scheduler(time.time, time.sleep)

# def getProductInOdoo():
    # s.enter(30, 1, getProductInOdoo, (s,))
    # s.run()

def CronJobProduct():
    # Setup
    url = "http://localhost:8069"
    db = "multichannel_test"
    username = "oa_faiz@exmple.com"
    password = "admin"
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    # test = xmlrpclib.Binary('{}/xmlrpc/2/object'.format(url))
    uid = common.authenticate(db,username,password, {})

    # Odoo Products
    products_in_odoo = models.execute_kw(db,uid,password, 'product.template', 'search_read', [], {'fields': ['item_id','SkuId','SellerSku']})

    # Lazada Product
    dateStart = datetime.now() + relativedelta(months=-1)
    dateEnd = datetime.now()
    formatFrom ="%Y-%m-%d %H:%M:%S"
    formatTo ="%Y-%m-%dT%H:%M:%S+0800"
    date_str_start = str(dateStart).split('.')[0]
    date_str_end = str(dateEnd).split('.')[0]
    date_GMT_start = datetime.strptime(date_str_start,formatFrom).strftime(formatTo)
    date_GMT_end = datetime.strptime(date_str_end,formatFrom).strftime(formatTo)

    lazadaConfig = models.execute_kw(db,uid,password,'lazada.configuration','search_read', [], {
        'fields':[               
            'URL',
            'API_Key',
            'API_Secret',
            'API_Code',
            'API_Token',
            'warehouse',
            # 'fromLocation',
            'stockLocation',
            'company',
            # 'prod_lot_id',
            # 'package_id',
        ]
    })
    stocklocation = models.execute_kw(db,uid,password,'stock.location','search_read', [[['id','=', 5]]], {'fields':['id']})
    URL = lazadaConfig[0]['URL']
    API_Key = lazadaConfig[0]['API_Key']
    API_Secret = lazadaConfig[0]['API_Secret']
    API_Code = lazadaConfig[0]['API_Code']
    API_Token = lazadaConfig[0]['API_Token']
    warehouse = lazadaConfig[0]['id']
    fromLocation = stocklocation[0]['id']
    toLocation = lazadaConfig[0]['id']
    company = lazadaConfig[0]['id']
    # prod_lot_id = lazadaConfig[0]['prod_lot_id']
    # package_id = lazadaConfig[0]['package_id']
    # print(fromLocation)

    client = lazop.LazopClient(URL, API_Key, API_Secret)
    productRequest = lazop.LazopRequest('/products/get','GET')
    productRequest.add_api_param('offset', '0')
    productRequest.add_api_param('create_after', date_GMT_start)
    productRequest.add_api_param('create_before', date_GMT_end)
    productResponse = client.execute(productRequest,API_Token)
    products_in_lazada = productResponse.body["data"]["products"]

    for product_in_lazada in products_in_lazada:
        lazada_name = product_in_lazada.get('attributes').get('name')
        lazada_brand = product_in_lazada.get('attributes').get('brand')
        lazada_short_description = product_in_lazada.get('attributes').get('short_description')
        lazada_skuid = product_in_lazada.get('skus')[0].get('SkuId')
        lazada_link = product_in_lazada.get('skus')[0].get('Images')[0]
        lazada_package_content = product_in_lazada.get('skus')[0].get('package_content')
        lazada_SalePrice = product_in_lazada.get('skus')[0].get('SalePrice')
        lazada_color_family = product_in_lazada.get('skus')[0].get('color_family')
        lazada_price = product_in_lazada.get('skus')[0].get('price')
        lazada_sellersku = product_in_lazada.get('skus')[0].get('SellerSku')
        lazada_shopsku = product_in_lazada.get('skus')[0].get('ShopSku')
        lazada_price = product_in_lazada.get('skus')[0].get('price')
        lazada_quantity = product_in_lazada.get('skus')[0].get('quantity')
        lazada_available = product_in_lazada.get('skus')[0].get('Available')
        lazada_package_length = product_in_lazada.get('skus')[0].get('package_length')
        lazada_package_weight = product_in_lazada.get('skus')[0].get('package_weight')
        lazada_package_width = product_in_lazada.get('skus')[0].get('package_width')
        lazada_package_height = product_in_lazada.get('skus')[0].get('package_height')
        lazada_primary_category = product_in_lazada.get('primary_category')
        lazada_item_id = product_in_lazada.get('item_id')
        if products_in_odoo:
            for product_in_odoo in products_in_odoo:
                odoo_item_id = product_in_odoo['item_id']
                odoo_SkuId = product_in_odoo['SkuId']
                odoo_SellerSku = product_in_odoo['SellerSku']
                if str(lazada_item_id) != str(odoo_item_id) or str(lazada_sellersku) != str(odoo_SellerSku) or str(lazada_skuid) != str(odoo_SkuId):
                    if lazada_link is None or lazada_link == "":
                        create_product_odoo = models.execute_kw(db,uid,password, 'product.template', 'create', [{
                            'name':lazada_name,
                            'LazadaProductName':lazada_name,
                            'item_id':lazada_item_id,
                            'shopsku':lazada_shopsku,
                            'SkuId':lazada_skuid,
                            'list_price': lazada_price,
                            # 'image_medium':link,
                            'PrimaryCategory':lazada_primary_category,
                            'Quantity':lazada_quantity,
                            'web_url':lazada_link,
                            'Brand': lazada_brand,
                            'Color':lazada_color_family,
                            'short_description':lazada_short_description,
                            'Package_content':lazada_package_content,
                            'SellerSku':lazada_sellersku,
                            'Package_length':lazada_package_length,
                            'Package_height':lazada_package_height,
                            'Package_weight':lazada_package_weight,
                            'Package_width':lazada_package_width,
                            'type':'product',
                            'company_id':company,
                        }])
                        print(create_product_odoo)
                        # create_stock_odoo = models.execute_kw(db,uid,password, 'stock.inventory', 'create', [{
                        #     'name': lazada_name + ' - ' + str(datetime.now()).split(".")[0],
                        #     'filter': 'product',
                        #     'product_id': create_product_odoo.id,
                        #     'state':'done',
                        #     'line_ids':[(0,0,{
                        #         'product_qty': lazada_quantity,
                        #         'location_id':fromLocation,
                        #         'product_id':create_product_odoo.id
                        #     })],
                        #     'move_ids':[(0,0,{
                        #         'name': ('INV:') + lazada_name,
                        #         'product_id': create_product_odoo.id,
                        #         'product_uom': 1,
                        #         'product_uom_qty': lazada_quantity,
                        #         'date': datetime.now(),
                        #         'state': 'done',
                        #         'location_id': fromLocation,
                        #         'location_dest_id': toLocation,
                        #         'move_line_ids': [(0, 0, {
                        #             'product_id': create_product_odoo.id,
                        #             'product_uom_qty': 0,  # bypass reservation here
                        #             'product_uom_id': 1,
                        #             'qty_done': lazada_quantity,
                        #             'location_id': fromLocation,
                        #             'location_dest_id':toLocation,
                        #         })]
                        #     })]
                        # }])
        elif not products_in_odoo:
            if lazada_link is None or lazada_link == "":
                create_product_odoo = models.execute_kw(db,uid,password, 'product.template', 'create', [{
                    'name':lazada_name,
                    'LazadaProductName':lazada_name,
                    'item_id':lazada_item_id,
                    'shopsku':lazada_shopsku,
                    'SkuId':lazada_skuid,
                    'list_price': lazada_price,
                    'PrimaryCategory':lazada_primary_category,
                    'Quantity':lazada_quantity,
                    'web_url':lazada_link,
                    'Brand': lazada_brand,
                    'Color':lazada_color_family,
                    'short_description':lazada_short_description,
                    'Package_content':lazada_package_content,
                    'SellerSku':lazada_sellersku,
                    'Package_length':lazada_package_length,
                    'Package_height':lazada_package_height,
                    'Package_weight':lazada_package_weight,
                    'Package_width':lazada_package_width,
                    'type':'product',
                    'company_id':company,
                }])
                print(create_product_odoo)
            else:
                r = requests.get(lazada_link)
                Image.open(BytesIO(r.content))
                # profile_image = base64.b64decode(urllib.request.urlopen(lazada_link).read())
                profile_image = base64.encodestring(urllib.request.urlopen(lazada_link).read())
                # print(profile_image)
                create_product_odoo = models.execute_kw(db,uid,password, 'product.template', 'create', [{
                    'name':lazada_name,
                    'LazadaProductName':lazada_name,
                    'item_id':lazada_item_id,
                    'shopsku':lazada_shopsku,
                    'SkuId':lazada_skuid,
                    'list_price': lazada_price,
                    'image_medium':profile_image,
                    'PrimaryCategory':lazada_primary_category,
                    'Quantity':lazada_quantity,
                    'web_url':lazada_link,
                    'Brand': lazada_brand,
                    'Color':lazada_color_family,
                    'short_description':lazada_short_description,
                    'Package_content':lazada_package_content,
                    'SellerSku':lazada_sellersku,
                    'Package_length':lazada_package_length,
                    'Package_height':lazada_package_height,
                    'Package_weight':lazada_package_weight,
                    'Package_width':lazada_package_width,
                    'type':'product',
                    'company_id':company,
                }])
                print(create_product_odoo.id)
            

# with open("Oodoo_product_data.txt", "w") as file:
#     file.write(str(CronJobProduct()))

CronJobProduct()


# export PATH="/root/.pyenv/bin:$PATH"
# eval "$(pyenv init -)"
# eval "$(pyenv virtualenv-init -)"
