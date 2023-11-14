import requests
import hashlib
import hmac
import time
from urllib.parse import urlencode

# Replace with your Binance API key and secret
api_key = 'Nw3cglPnQmqtJVCyjOp84CYfB9T0lcwT9Jm93hPbyAhEgR23mNz8gnkZuPXtfJwJ'
api_secret = 'bsl0oeBw2sxni3PnOt9PpEnPmKQ9gB3IQVPYlzITTCzeJXGrW2vWAhByQjWFtcbu'

# Replace with your actual proxy URL
proxy_url = 'http://127.0.0.1:8001/router'

# Define order parameters
symbol = 'BTCUSDT'
side = 'SELL'
type_ = 'LIMIT'
time_in_force = 'GTC'
quantity = 0.002
price = 9500

# Construct the query parameters for creating the order
order_params = {
    'symbol': symbol,
    'side': side,
    'type': type_,
    'timeInForce': time_in_force,
    'quantity': quantity,
    'price': price,
    'timestamp': int(time.time() * 1000),
}

# Create the query string for creating the order
order_query_string = '&'.join([f"{key}={order_params[key]}" for key in order_params])

# Create the signature for creating the order
order_signature = hmac.new(api_secret.encode(), order_query_string.encode(), hashlib.sha256).hexdigest()

# Include the signature in the query parameters for creating the order
order_params['signature'] = order_signature

# Create the request data for creating the order
order_request_data = {
    "url": f"/api/v3/order?{urlencode(order_params)}",
    "headers": {"X-MBX-APIKEY": api_key},
    "method": "POST",
    "data": None
}

# Send the request to create the order
response_create_order = requests.post(proxy_url, json={'data': [order_request_data]})
print(response_create_order.content)

# Extract the order ID from the response (assuming the order was successfully created)
order_id = response_create_order.json().get('orderId')

# Construct the query parameters for canceling the order
cancel_params = {
    'symbol': symbol,
    'orderId': order_id,
    'timestamp': int(time.time() * 1000),
}

# Create the query string for canceling the order
cancel_query_string = '&'.join([f"{key}={cancel_params[key]}" for key in cancel_params])

# Create the signature for canceling the order
cancel_signature = hmac.new(api_secret.encode(), cancel_query_string.encode(), hashlib.sha256).hexdigest()

# Include the signature in the query parameters for canceling the order
cancel_params['signature'] = cancel_signature

# Create the request data for canceling the order
cancel_request_data = {
    "url": f"/api/v3/order?{urlencode(cancel_params)}",
    "headers": {"X-MBX-APIKEY": api_key},
    "method": "DELETE",
    "data": None
}

# Send the request to cancel the order
response_cancel_order = requests.post(proxy_url, json={'data': [cancel_request_data]})
print(response_cancel_order.content)
