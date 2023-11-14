import requests
import hashlib
import hmac
import time
from urllib.parse import urlencode

# Replace with your Binance API key and secret
api_key = 'U8Uvbf2Kh6D5GHswBxsuV504Urb1vZyuAScdqF1zEjzG1hrwXy4DqzpkFzM7P7AX'
api_secret = 'fWSGqLmbVT7aCkgfTIPPGKiafTvSZQhM9Vs1VuwOIVPWDDNchiDyIuQXcjA9kcKe'

# Replace with your actual proxy URL
proxy_url = 'http://127.0.0.1:8001/router'

# Binance API endpoint for getting open orders
api_url = 'https://api.binance.com/api/v3/openOrders'
recv_window = 60000

# Construct the query parameters
params = {
    'symbol': 'BTCUSDT',  # Replace with the trading pair you are interested in
    'timestamp': int(time.time() * 1000),
    'recvWindow': recv_window,
}

# Create the query string
query_string = '&'.join([f"{key}={params[key]}" for key in params])

def arrange_order(api_key, api_secret, params):
    # Create the signature
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    # Include the signature in the query parameters
    params['signature'] = signature

    request_data = {
        "url": f"/api/v3/openOrders?{urlencode(params)}",
        "headers": {"X-MBX-APIKEY": api_key},
        "method": "GET",
        "data": None
    }

    return request_data

total_users = 1
data = []
for _ in range(total_users):
    data.append(arrange_order(api_key, api_secret, params))
print(data)

response = requests.post(proxy_url, json={'data': data})
print(response.content)
