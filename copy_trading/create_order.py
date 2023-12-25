import requests
import hashlib
import hmac
import time
from urllib.parse import urlencode


# Replace with your Binance API key and secret
# Nw3cglPnQmqtJVCyjOp84CYfB9T0lcwT9Jm93hPbyAhEgR23mNz8gnkZuPXtfJwJ
# api_key = 'Nw3cglPnQmqtJVCyjOp84CYfB9T0lcwT9Jm93hPbyAhEgR23mNz8gnkZuPXtfJwJ'
# api_secret = 'bsl0oeBw2sxni3PnOt9PpEnPmKQ9gB3IQVPYlzITTCzeJXGrW2vWAhByQjWFtcbu'

# Replace with your actual proxy URL
proxy_url = 'http://127.0.0.1:8005/router'


# Define order parameters
# symbol = 'BTCUSDT'
# side = 'BUY'
# type_ = 'MARKET'
# quantity = 0.0005

# # Construct the query parameters
# params = {
#     'symbol': symbol,
#     'side': side,
#     'type': type_,
#     'quantity': quantity,
#     'timestamp': int(time.time() * 1000),
# }


def arrange_order(api_key,api_secret,params):
    
    # Create the query string
    query_string = '&'.join([f"{key}={params[key]}" for key in params])
    # Create the signature
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    # Include the signature in the query parameters
    params['signature'] = signature
    request_data = {
            "url":f"/api/v3/order?{urlencode(params)}",
            "headers":{"X-MBX-APIKEY": api_key},
            "method":"POST",
            "data":None
            }
    print(request_data)
    return request_data
    
# total_users = 2
def create_order(total_users):
    data = []
    for api_key,api_secret,params in total_users:
        data.append(arrange_order(api_key,api_secret,params))
    print("createdata",data)
    response = requests.post(proxy_url, json={'data':data})
    # print(response.content)
    return (response.content).decode('utf-8')

