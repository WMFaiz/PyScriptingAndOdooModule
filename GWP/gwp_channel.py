from datetime import datetime, date, timedelta
import pytz
import gwp_functions as gwpf
import gwp_merchant_id as gwpmid


def lazada(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    # ENT4011 BTFL ENT334 ENT570 ENT651 ENT0665 ENT4011 ENT4311 ENT4395
    # ENT4770 ENT5050 ENT6596 ENT6676 ENT6679 ENT8023 ENT8096 ENT9555
    switch = {
        '221361685_TH-337681897': gwpmid._221361685_TH_337681897(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4011': gwpmid.ENT4011(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'BTFL': gwpmid.BTFL(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT334': gwpmid.ENT334(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT570': gwpmid.ENT570(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT651': gwpmid.ENT651(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT0665': gwpmid.ENT0665(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4311': gwpmid.ENT4311(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4395': gwpmid.ENT4395(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4770': gwpmid.ENT4770(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT5050': gwpmid.ENT5050(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT6596': gwpmid.ENT6596(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT6676': gwpmid.ENT6676(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT6679': gwpmid.ENT6679(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT8023': gwpmid.ENT8023(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT8096': gwpmid.ENT8096(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT9555': gwpmid.ENT9555(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
    }
    func = switch.get(merchant_id, 'Invalid Merchant Id')
    return func

def magento1(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    # ENT570
    switch = {
        'ENT570': gwpmid.ENT570(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
    }
    func = switch.get(merchant_id, 'Invalid Merchant Id')
    return func

def shopee(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    # ENT2192 ENT334 ENT412 ENT570 ENT621 ENT651 ENT0665 ENT753 ENT4011
    # ENT4311 ENT4395 ENT5050 ENT6676 ENT8023
    switch = {
        '221361685_TH-337681897': gwpmid._221361685_TH_337681897(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT8023': gwpmid.ENT8023(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT6676': gwpmid.ENT6676(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT5050': gwpmid.ENT5050(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4395': gwpmid.ENT4395(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4311': gwpmid.ENT4311(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT4011': gwpmid.ENT4011(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT0665': gwpmid.ENT0665(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT651': gwpmid.ENT651(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT570': gwpmid.ENT570(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT334': gwpmid.ENT334(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT2192': gwpmid.ENT2192(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT412': gwpmid.ENT412(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT621': gwpmid.ENT621(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT753': gwpmid.ENT753(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
    }
    func = switch.get(merchant_id, 'Invalid Merchant Id')
    return func

def qoo10(merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    # BTFL ENT334 ENT570
    switch = {
        'BTFL': gwpmid.BTFL(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT334': gwpmid.ENT334(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
        'ENT570': gwpmid.ENT570(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
    }
    func = switch.get(merchant_id, 'Invalid Merchant Id')
    return func

def shopify( merchant_id, timezone, function_name, gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    # ENT1716
    switch = {
        'ENT1716': gwpmid.ENT1716(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num),
    }
    func = switch.get(merchant_id, 'Invalid Merchant Id')
    return func