from datetime import datetime, date, timedelta
import pytz
import gwp as gwp
import gwp_functions as gwpf
from pymongo import MongoClient

# connection = MongoClient('mongodb+srv://chengjk:KmgPbdsXp1Ypl3pB@cluster0.h48nu.mongodb.net/<dbname>?retryWrites=true&w=majority')
# db = connection['odoo']
# db_order_items = db.order_items
# db_orders = db.orders
# order_items = db_order_items.find()
# orders = db_orders.find()

# item_sku = ''
# items_sku = []
# order_item_post = []
# gwp_order_date = ''
# gwp_end_order_date = ''
# getDatetimeNow = datetime.now()
# for order in orders:
#     order_items = order['items']
#     gwp_order_date = datetime.strptime(order['created_at'].replace('-','/').split(' +')[0], '%Y/%m/%d %H:%M:%S')
#     gwp_end_order_date = gwpf.buildEndDatetimeFromGivenDatetime('Singapore',gwp_order_date, 0,0,0,getDatetimeNow.hour,getDatetimeNow.minute,getDatetimeNow.second)
#     order_total = order['items_count']
#     for items in order_items:
#         for item in items:
#             if item_sku != item['sku']:
#                 item_sku = item['sku']
#                 order_item_json = {
#                     'Sku': item_sku,
#                     'Quantity': order_total,
#                     'UnitPrice': 0.0
#                 }
#                 order_item_post.append(order_item_json)
# connection.close()

# gwp.inject_gwp(order_item_post)
# gwp_order_date = datetime.strptime(created_at, '%Y/%m/%d %H:%M:%S')
# getDatetimeNow = datetime.now()
# gwp_end_order_date = gwpf.buildEndDatetimeFromGivenDatetime('Singapore',gwp_order_date, 0,0,0,getDatetimeNow.hour,getDatetimeNow.minute,getDatetimeNow.second)

# combine_gwp = []

# lazada_ENT4011 = gwp.get_gwp('lazada', '221361685_TH-337681897', 'Asia/Singapore', 'addNumSetsPerQualifyingItem',
#                      gwp_order_date, gwp_order_date, 
#                      order_item_post, order_total, None, 
#                      'TEST ORDER 01', 'GWP-2118-1-ENT4011', 
#                      ['POD11XX212','POD00Y212'],['PD0X011Z'], 1)
# combine_gwp.append(lazada_ENT4011)
# print(combine_gwp)


# ----------------------------------------------------------------------------------------------------------------------------------------------- #
# inject_gwp(Timezone, shop_sku, GWP_sku_list, gift_sku, yy, mm, dd, HH, MM, SS) 
# yy, mm, dd, HH, MM and SS is the end date, start date is base on created_at from mongoDB POD00Y212
current = datetime.now()
gwp.inject_gwp('Asia/Singapore','221361685_TH-337681897',['POD11XX212','POD00Y212'],['PD0X011Z'], 0,1,2,current.hour,current.minute,current.second)