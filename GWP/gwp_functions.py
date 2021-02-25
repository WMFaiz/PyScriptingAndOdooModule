from datetime import datetime, date, timedelta
import urllib.request, urllib.parse, urllib.error
import pytz

# MongoDB Link
# mongodb+srv://chengjk:KmgPbdsXp1Ypl3pB@cluster0.h48nu.mongodb.net/<dbname>?retryWrites=true&w=majority

def gwp_item_list(gwp_array):
    item_list = []
    item_list.append(gwp_array)
    return item_list

def getLocationDatetime(timezone, datetime):
    getTimezone = pytz.timezone(timezone)
    getDate = getTimezone.localize(datetime)
    removeNaiveDatetime = getDate.replace(tzinfo=None)
    return removeNaiveDatetime

def buildDatetimeFromScratch(timezone, dd,mm,yy,HH,MM,SS):
    getTimezone = pytz.timezone(timezone)
    build = str(yy)+'/'+str(mm)+'/'+str(dd)+' '+str(HH)+':'+str(MM)+':'+str(SS)
    convertToDatetime = datetime.strptime(build, '%Y/%m/%d %H:%M:%S')
    getDate = getTimezone.localize(convertToDatetime)
    removeNaiveDatetime = getDate.replace(tzinfo=None)
    return removeNaiveDatetime

def buildEndDatetimeFromGivenDatetime(timezone, startDatetime, dd,mm,yy,HH,MM,SS):
    if isinstance(startDatetime, list) == True:
        output = []
        for data in startDatetime:
            getTimezone = pytz.timezone(timezone)
            targetDatetime = data.replace(day=data.day+dd, month=data.month+mm, year=data.year+yy, hour=HH, minute=MM, second=SS)
            getDate = getTimezone.localize(targetDatetime)
            removeNaiveDatetime = getDate.replace(tzinfo=None)
            output.append(removeNaiveDatetime)
        return output
    elif isinstance(startDatetime, list) == False:
        getTimezone = pytz.timezone(timezone)
        targetDatetime = startDatetime.replace(day=startDatetime.day+dd, month=startDatetime.month+mm, year=startDatetime.year+yy, hour=HH, minute=MM, second=SS)
        getDate = getTimezone.localize(targetDatetime)
        removeNaiveDatetime = getDate.replace(tzinfo=None)
        return removeNaiveDatetime

def compareDatetime(startDatetime, endDatetime):
    compareDate = endDatetime - startDatetime
    return compareDate

def checkDatetime(timezone,gwp_order_date, gwp_end_order_date):
    currDatetime = getLocationDatetime(timezone,datetime.now())
    datetimeToStart = compareDatetime(currDatetime, gwp_order_date)
    ts_days, ts_ori_seconds = datetimeToStart.days, datetimeToStart.seconds
    ts_seconds = ts_ori_seconds % 60
    ts_minutes = (ts_ori_seconds % 3600) / 60
    ts_hourse = ts_days * 24 - ts_seconds / 3600
    if ts_days <= 0 and ts_hourse <= 0 and round(ts_minutes) <= 0:
        remainingDuration = compareDatetime(currDatetime, gwp_end_order_date)
        r_days, r_ori_seconds = remainingDuration.days, remainingDuration.seconds
        r_seconds = r_ori_seconds % 60
        r_minutes = (r_ori_seconds % 3600) / 60
        r_hourse = r_days * 24 - r_seconds / 3600
        if r_days <= 0 and r_hourse <= 0 and round(r_minutes) <= 0:
            return True
        else:
            return False
    else:
        print('This GWP has expired since ' + str(gwp_order_date))
        return False

def checkDatetimeTest(timezone,gwp_order_date, gwp_end_order_date):
    remainingDuration = compareDatetime(gwp_order_date, gwp_end_order_date)
    r_days, r_ori_seconds = remainingDuration.days, remainingDuration.seconds
    r_seconds = r_ori_seconds % 60
    r_minutes = (r_ori_seconds % 3600) / 60
    r_hourse = r_days * 24 - r_seconds / 3600
    if r_days <= 0 and r_hourse <= 0 and round(r_minutes) <= 0:
        return True
    else:
        print('This GWP has expired since ' + str(gwp_order_date))
        return False

def checkQuantity(order_qty, minimum_qty, operations):
    if order_qty > minimum_qty and operations == 'more':
        return True
    elif order_qty >= minimum_qty and operations == 'more_n_equalTo':
        return True
    elif order_qty < minimum_qty and operations == 'less':
        return True
    elif order_qty <= minimum_qty and operations == 'less_n_equalTo':
        return True
    else:
        return False

def checkBaseOrderTotal(priceAmount, conditionPrice, operations):
    if priceAmount > conditionPrice and operations == 'more':
        return True
    elif priceAmount < conditionPrice and operations == 'less':
        return True
    elif priceAmount >= conditionPrice and operations == 'more_n_equalTo':
        return True
    elif priceAmount <= conditionPrice and operations == 'less_n_equalTo':
        return True
    else:
        return False

def sumSellingPriceIfInSkuList(sku_list, order_item_post):
    sum = 0;
    for order_item in order_item_post:
        for sku in sku_list:
            if order_item['Sku'] == sku:
                sum += order_item['paid_price'];
    # print("sum_selling_price: " + sum)
    return sum


def countOccurence(sku_list, order_item_post):
    count = 0
    for order_item in order_item_post:
        for sku in sku_list:
            if order_item == sku:
                count += order_item['Quantity']
    return count


# Count the total number of quantity for the order
# This is used for promotions like "Buy 2 or more" for the whole order
def countNumQuantity(order_item_post):
    count = 0
    for order_item in order_item_post:
        count += order_item['Quantity'];
    return count


def addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count):
    gwp_item_list = []
    for sku in gwp_sku_list_to_give:
        gwp_sku_json = {
            'Sku':sku,
            'Quantity': count,
            'UnitPrice': 0.0
        }
        gwp_item_list.append(gwp_sku_json)
        # print(gwp_item_list)
    return gwp_item_list


def getQualifiedOrderTotal(gwp_sku_list_to_check, order_item_post):
    qualified_order_total = 0;
    for order_item in order_item_post:
        order_item_sku = order_item['Sku'];
        for item_sku in order_item_sku:
            for sku_list_to_check in gwp_sku_list_to_check:
                if item_sku == sku_list_to_check:
                    qualified_order_total += gwp_sku_list_to_check[order_item_sku] * order_item['Quantity']
    return qualified_order_total


# Functions with name of the promotion type
def addGiftPerOrder(gwp_code, delivery_order_id, gwp_sku_list_to_give, count):
    return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count)


def addOneGiftPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give):
    addItems = addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, 1)
    return addItems


# Used for the case "For each of the SKU in this list, get $num set of GWP"
def addNumSetsPerQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num):
    count = countOccurence(gwp_sku_list_to_check, order_item_post)
    if count > 0:
        return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count * num)
    return []


# use for case with 2 set of sku check list, get multiple gift based on smaller qty total * $num
def addNumSetsPerTwoQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check_set_a, gwp_sku_list_to_check_set_b, order_item_post, gwp_sku_list_to_give, num):
    count_set_a = countOccurence(gwp_sku_list_to_check_set_a, order_item_post)
    count_set_b = countOccurence(gwp_sku_list_to_check_set_b, order_item_post)
    if count_set_a > 0 and count_set_b > 0:
        if count_set_a < count_set_b:
            count = count_set_a;
            return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count * num);
        else:
            count = count_set_b;
            return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count * num);
    return []


# use for case with 2 set of sku check list, with 1 compulsory sku check list
# get multiple gift based on smaller qty total * $num
def addNumSetsPerOneCompulsoryItem(gwp_code, delivery_order_id, gwp_sku_list_to_check_set_a, gwp_sku_list_to_check_set_b, order_item_post, gwp_sku_list_to_give, num):
    count_set_a = countOccurence(gwp_sku_list_to_check_set_a, order_item_post)
    count_set_b = countOccurence(gwp_sku_list_to_check_set_b, order_item_post)
    if count_set_a > 0:
        if count_set_b > 0:
            if count_set_a <= count_set_b:
                count = count_set_a;
                return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count * num)
            else:
                count = count_set_b;
                return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, count * num)
    return []


#Used for the case "Purchase any 2 of the SKU, get $num set of GWP"
def addNumSetsPerNQualifyingItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, n_num, num):
    count = countOccurence(gwp_sku_list_to_check, order_item_post)
    if count > 0:
        n_sets = count / n_num;
        # print("n_sets: ", n_sets)
        if n_sets > 0:
            return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, n_sets * num)
        return []
    return []


def addNumSetsIfQualifyingItemFound(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give, num):
    count = countOccurence(gwp_sku_list_to_check, order_item_post)
    if count > 0:
        return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)
    return []


# use for case with 2 set of sku check list, get as $num defined gift
def addNumSetsIfTwoQualifyingItemFound(gwp_code, delivery_order_id, gwp_sku_list_to_check_set_a, gwp_sku_list_to_check_set_b, order_item_post, gwp_sku_list_to_give, num):
    count_set_a = countOccurence(gwp_sku_list_to_check_set_a, order_item_post)
    count_set_b = countOccurence(gwp_sku_list_to_check_set_b, order_item_post)
    if count_set_a > 0 and count_set_b > 0:
        return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)
    return []


#add only when none of the SKUs in the excluded list is found in order
def addNumSetsIfNoExcludedSkuFound(gwp_code, delivery_order_id, gwp_sku_list_to_exclude, order_item_post, gwp_sku_list_to_give, num):
    count = countOccurence(gwp_sku_list_to_exclude, order_item_post)
    if count == 0:
        return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, num)
    return []


def addOneGiftPerOrderIfQualifiedItem(gwp_code, delivery_order_id, gwp_sku_list_to_check, order_item_post, gwp_sku_list_to_give):
    count = countOccurence(gwp_sku_list_to_check, order_item_post)
    if count > 0:
        return addCountForEach(gwp_code, delivery_order_id, gwp_sku_list_to_give, 1)
    return []