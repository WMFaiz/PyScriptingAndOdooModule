from datetime import datetime, date, timedelta
import urllib.request, urllib.parse, urllib.error
import gwp_functions as gwpf


def _221361685_TH_337681897(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT4011(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def BTFL(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT334(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT570(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func
def ENT651(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT0665(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT4311(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT4395(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT4770(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT5050(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT6596(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT6676(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT6679(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT8023(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT8096(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT9555(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT2192(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func


def ENT412(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT621(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT753(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func

def ENT1716(function_name,timezone,gwp_order_date, gwp_end_order_date, order_item_post, order_total, order_min, delivery_order_id, gwp_code, gwp_sku_list_to_check, gwp_sku_list_to_give, num):
    switch = {
        'addGiftPerOrder': gwpf.gwp_item_list(gwpf.addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)),
        'addNumSetsPerQualifyingItem':gwpf.gwp_item_list(gwpf.addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num)),
        'addOneGiftPerQualifyingItem': gwpf.gwp_item_list(gwpf.addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give)),
        'addNumSetsPerTwoQualifyingItem': [],
        'addNumSetsPerOneCompulsoryItem': [],
        'addNumSetsPerNQualifyingItem': [],
        'addNumSetsIfQualifyingItemFound': [],
        'addNumSetsIfTwoQualifyingItemFound': [],
        'addNumSetsIfNoExcludedSkuFound': [],
        'addOneGiftPerOrderIfQualifiedItem': []
    }
    if gwp_order_date != None and gwp_end_order_date != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif order_total != None and order_min != None:
        if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
            func = switch.get(function_name, 'Invalid Function Name')
            return func
    elif gwp_order_date != None and gwp_end_order_date != None and order_total != None and order_min != None:
        if gwpf.checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
            if gwpf.checkBaseOrderTotal(order_total, order_min, 'more_n_equalTo'):
                func = switch.get(function_name, 'Invalid Function Name')
                return func