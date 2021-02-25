# -*- coding: utf-8 -*-

import lazop
import requests
import webbrowser
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# url = 'https://api.lazada.com.my/rest'
# appkey = '116869'
# appSecret = 'B5k0VSbhliemszkcwK3spfolsQrX7WHv'
# access_token = '50000601720iYFiqbtRfWggq8lVycKlR16701d88lvHusCG09urayqVrlVsqK0'

class lazada_main():
    
    def lazop_client(self, url, api_key, api_secret):
        client = lazop.LazopClient(url, api_key, api_secret)
        return client

    def lazada_get_token(self, client):
        if api_token == False:
            request = lazop.LazopRequest('/auth/token/create','GET')
            request.add_api_param('code',api_code)
            response = client.execute(request)
            convertJson = str(response.body).replace("\'", "\"")
            responseJson = json.loads(convertJson)
            if 'InvalidCode' in str(responseJson):
                webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
                return 'Need request'
            else:
                return responseJson.get('access_token')
        elif api_code == False:
            webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
            return 'Need to request'
        elif api_token == False and api_code == False:
            webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
            return 'Need to request'
        elif api_token is None and api_code is not None:
            request = lazop.LazopRequest('/auth/token/create','GET')
            request.add_api_param('code',api_code)
            response = client.execute(request)
            convertJson = str(response.body).replace("\'", "\"")
            responseJson = json.loads(convertJson)
            return responseJson.get('access_token')
        elif api_token is not None and api_code is not None:
            request = lazop.LazopRequest('/product/item/get','GET')
            response = client.execute(request, api_token)
            responseOut = str(response.body)
            if 'IllegalAccessToken' in responseOut or 'Unexpected internal' in responseOut:
                request = lazop.LazopRequest('/auth/token/refresh','GET')
                request.add_api_param('refresh_token', api_token)
                response = client.execute(request)
                convertJson = str(response.body).replace("\'", "\"")
                responseJson = json.loads(convertJson)
                return responseJson.get('refresh_token')
            else:
                print('Token:','Valid')
        elif api_token is not None and api_code is None:
            webbrowser.open('https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://dbece77471d2.ngrok.io&client_id=116869')
            return 'Need to request'

    # def lazada_config_token(self):
    #     request = lazop.LazopRequest('/product/item/get','GET')
    #     response = client.execute(request, api_token)
    #     responseOut = str(response.body)
    #     if 'IllegalAccessToken' in responseOut or 'Unexpected internal' in responseOut:
    #         request = lazop.LazopRequest('/auth/token/refresh','GET')
    #         request.add_api_param('refresh_token', api_token)
    #         response = client.execute(request)
    #         convertJson = str(response.body).replace("\'", "\"")
    #         responseJson = json.loads(convertJson)
    #         return self.API_Token 
    #     else:
    #         return self.API_Token