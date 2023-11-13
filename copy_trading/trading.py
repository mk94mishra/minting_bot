import requests
import hashlib
import hmac
import time
from urllib.parse import urlencode


# Replace with your Binance API key and secret
api_key = 'your_binance_api_key'
api_secret = 'your_binance_api_secret'

# Replace with your actual proxy URL
proxy_url = 'http://127.0.0.1:8001/router'


# Define order parameters
symbol = 'BTCUSDT'
side = 'SELL'
type_ = 'LIMIT'
time_in_force = 'GTC'
quantity = 0.002
price = 9500

# Construct the query parameters
params = {
    'symbol': symbol,
    'side': side,
    'type': type_,
    'timeInForce': time_in_force,
    'quantity': quantity,
    'price': price,
    'timestamp': int(time.time() * 1000),
}

# Create the query string
query_string = '&'.join([f"{key}={params[key]}" for key in params])

def arrange_order(api_key,api_secret,params):
    # Replace with your Binance API key and secret
    api_key = 'your_binance_api_key'
    api_secret = 'your_binance_api_secret'

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
    # print(request_data)
    return request_data
    
total_users = 3
data = []
for _ in range(total_users):
    data.append(arrange_order(api_key,api_secret,params))
print(data)
response = requests.post(proxy_url, json={'data':data})
print(response)
