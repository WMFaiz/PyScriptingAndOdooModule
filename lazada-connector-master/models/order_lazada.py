import pyshopee
import requests
import lazop
import json
from datetime import datetime, date
from odoo import models, fields, api,  _
from odoo.exceptions import Warning

class Order_Lazada(models.Model):
    _name = 'order.lazada'
    # _inherit = 'sale.order'

    # general information
    dateStart = fields.Datetime(string='Create After')
    dateEnd = fields.Datetime(string='Create Before')
    voucher = fields.Char(string='Voucher')
    warehouse_code = fields.Char(string='Warehouse Code')
    order_number = fields.Char(string='Order Number')
    created_at = fields.Char(string='Created at')
    voucher_code = fields.Char(string='Voucher Code')
    gift_option = fields.Char(string='Gift Option')
    shipping_fee_discount_platform = fields.Char(string='Shipping Fee Discount Platform')
    customer_last_name = fields.Char(string='Customer Last Name')
    updated_at = fields.Char(string='Updated at')
    promised_shipping_times = fields.Char(string='Promised Shipping Times')
    price = fields.Char(string='Price')
    national_registration_number = fields.Char(string='National Registration Number')
    shipping_fee_original = fields.Char(string='Shipping Fee Original')
    payment_method = fields.Char(string='Payment Method')
    customer_first_name = fields.Char(string='Customer First Name')
    shipping_fee_discount_seller = fields.Char(string='Shipping Fee Discount Seller')
    shipping_fee = fields.Char(string='Shipping Fee')
    branch_number = fields.Char(string='Branch Number')
    tax_code = fields.Char(string='Tax Code')
    delivery_info = fields.Char(string='Delivery Info')
    statuses = fields.Char(string='Status')
    extra_attributes = fields.Char(string='Extra Attributes')
    order_id = fields.Char(string='Order ID')
    gift_message = fields.Char(string='Gift Message')
    remarks = fields.Char(string='Remarks')
    # address billing
    country_ab = fields.Char(string='Country')
    address3_ab = fields.Char(string='Address 3')
    address2_ab = fields.Char(string='Address 2')
    city_ab = fields.Char(string='City')
    phone_ab = fields.Char(string='Phone')
    address1_ab = fields.Char(string='Address 1')
    post_code_ab = fields.Char(string='Post Code')
    phone2_ab = fields.Char(string='Phone 2')
    last_name_ab = fields.Char(string='Last Name')
    address5_ab = fields.Char(string='Address 5')
    address4_ab = fields.Char(string='Address 4')
    first_name_ab = fields.Char(string='First Name')
    # address shipping
    country_as = fields.Char(string='Country')
    address3_as = fields.Char(string='Address 3')
    address2_as = fields.Char(string='Address 2')
    city_as = fields.Char(string='City')
    phone_as = fields.Char(string='Phone')
    address1_as = fields.Char(string='Address 1')
    post_code_as = fields.Char(string='Post Code')
    phone2_as = fields.Char(string='Phone 2')
    last_name_as = fields.Char(string='Last Name')
    address5_as = fields.Char(string='Address 5')
    address4_as = fields.Char(string='Address 4')
    first_name_as = fields.Char(string='First Name')

    @api.multi
    def lazada_order_product(self):
        for rec in self:
            date_rec_start = rec['dateStart']
            date_rec_end = rec['dateEnd']
            formatFrom ="%Y-%m-%d %H:%M:%S"
            formatTo ="%Y-%m-%dT%H:%M:%S+08:00"
            date_str_start = str(date_rec_start).split('.')[0]
            date_str_end = str(date_rec_end).split('.')[0]
            date_GMT_start = datetime.strptime(date_str_start,formatFrom).strftime(formatTo)
            date_GMT_end = datetime.strptime(date_str_end,formatFrom).strftime(formatTo)
            lazada_rec = self.env['lazada.configuration'].search([])
            url = lazada_rec.mapped('URL')[0]
            key = lazada_rec.mapped('API_Key')[0]
            secret = lazada_rec.mapped('API_Secret')[0]
            token = lazada_rec.mapped('API_Token')[0]
            # lazada_token = self.lazada_token(url, key, secret, token)
            client = lazop.LazopClient(url, key, secret)
            request = lazop.LazopRequest('/orders/get','GET')
            request.add_api_param('offset', '0')
            request.add_api_param('created_after', date_GMT_start)
            request.add_api_param('created_before', date_GMT_end)
            # request.add_api_param('update_after', date_GMT_start)
            request.add_api_param("status", "pending");
            response = client.execute(request,token)
            # total_products = response.body["data"]["total_products"]
            # print(response.body)
            orders = response.body["data"]["orders"]
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

                # order_id
                productEnv = self.env['product.template']
                orderEnv = self.env['order.lazada'] 
                customerEnv = self.env['res.partner']
                saleEnv = self.env['sale.order']
                saleOrderId = self.env['sale.order.line']

                customerName = first_name_ab+" "+last_name_ab
                street = address1_ab+", "+address2_ab+", "+address3_ab+", "+address4_ab+", "+address5_ab
                customerId = customerEnv.create({
                    'name': customerName,
                    'street': street,
                    'phone':phone_ab
                })

                partner_id = saleEnv.create({
                    'partner_id': customerId.id,
                    # 'state': 'sale'
                })

                request = lazop.LazopRequest('/order/items/get','GET')
                request.add_api_param('order_id', order_id)
                response = client.execute(request, token)
                items = response.body["data"]
                for item in items:
                    getName = item.get('name')
                    getOrderId = item.get('order_id')
                    itemId = productEnv.create({
                        'name':getName,
                        'orderId':getOrderId
                    })
                    saleOrderId.create({
                        'product_id':itemId.id,
                        'order_id':partner_id.id,
                        'confirmation_date': datetime.now()
                    })