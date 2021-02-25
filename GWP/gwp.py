from datetime import datetime, date, timedelta
import gwp_functions as gwpf
import gwp_merchant_id as gwpmid
import gwp_channel as gwpc
from pymongo import MongoClient

# get GWP
def get_gwp(channel, merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'lazada': gwpc.lazada(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'magento1': gwpc.magento1(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'shopee': gwpc.shopee(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'qoo10': gwpc.qoo10(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'shopify': gwpc.shopify(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num)
    }
    func = switch.get(channel, 'Invalid Platform Name')
    return func


def inject_gwp(timezone,merchant_id,gwp_sku_list_to_check,gwp_sku_list_to_give, yy, mm, dd, HH,MM,SS):
    connection = MongoClient('mongodb+srv://chengjk:KmgPbdsXp1Ypl3pB@cluster0.h48nu.mongodb.net/<dbname>?retryWrites=true&w=majority')
    db = connection['odoo']
    db_orders = db.orders
    _id = ''
    counter = 0
    position = 0
    item_sku_2 = ''
    json = {}
    for order in db_orders.find():
        item_sku = ''
        item_name = ''
        order_item_id = ''
        shop_sku = ''
        items = order['items'][0]
        gwp_order_date = datetime.strptime(order['created_at'].replace('-','/').split(' +')[0], '%Y/%m/%d %H:%M:%S')
        gwp_end_order_date = gwpf.buildEndDatetimeFromGivenDatetime(timezone,gwp_order_date,yy,mm,dd,HH,MM,SS)
        for item in items:
            item_sku = item.get('sku')
            item_name = item.get('name')
            order_item_id = item.get('order_item_id')
            shop_sku = item.get('shop_sku')
            if item_sku in gwp_sku_list_to_check:
                if item.get('shop_sku') == merchant_id:
                    if _id != order.get('_id'):
                        _id = order.get('_id')
                        position = order['items_count'] - 1
                        position += 1
                        counter = 0
                        print('-------------------------')
                    if _id == order.get('_id'):
                        position = order['items_count']
                        _id = order.get('_id')
                        if item_sku_2 == item_sku:
                            counter += 1
                        elif item_sku_2 != item_sku:
                            item_sku_2 = item_sku
                            if counter < 1:
                                counter += 1
                for sku_give in gwp_sku_list_to_give:
                    json = {
                        'items.0.'+str(position):{
                            'name': item_name,
                            'item_sku': item_sku,
                            'order_item_id': order_item_id,
                            'shop_sku': shop_sku,
                            'sku': sku_give,
                            'Quantity': counter,
                            'item_price': 0.0
                        }
                    }
                print(json)
                # status = db_orders.update({'_id':order['_id']},{'$set' : json})
                position = 0
        # if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_order_date):
            # print(json)
            # if _id == order.get('_id'):
            #     position = order['items_count'] - 1
            #     position += 1
            # elif _id != order.get('_id'):
            #     position = order['items_count']
            #     _id = order.get('_id')

            # for sku_give in gwp_sku_list_to_give:
            #     json = {
            #         'items.0.'+str(position):{
            #             'name': item_name,
            #             'item_sku': item_sku,
            #             'order_item_id': order_item_id,
            #             'shop_sku': shop_sku,
            #             'Sku': sku_give,
            #             'Quantity': counter,
            #             'UnitPrice': 0.0
            #         }
            #     }

                # json = {
                #     'name': item_name,
                #     'item_sku': item_sku,
                #     'order_item_id': order_item_id,
                #     'shop_sku': shop_sku,
                #     'Sku': sku_give,
                #     'Quantity': counter,
                #     'UnitPrice': 0.0
                # }

            # print(json)
            # status = db_orders.update({'_id':order['_id']},{'$set' : {'items.0.'+str(position):json}})
            # position = 0
            # status = db_orders.update({'_id':order['_id']},{'$set' : {'items.0.'+str(counter):json}})
    connection.close() 
