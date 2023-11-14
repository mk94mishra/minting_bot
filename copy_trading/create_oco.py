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
quantity = 0.002
entry_price = 9500
stop_loss_price = 9400  # Adjust as needed
take_profit_price = 9600  # Adjust as needed

# Construct the query parameters for the OCO order
oco_params = {
    'symbol': symbol,
    'quantity': quantity,
    'price': entry_price,
    'stopPrice': stop_loss_price,
    'stopLimitPrice': take_profit_price,
    'stopLimitTimeInForce': 'GTC',
    'timestamp': int(time.time() * 1000),
}

# Create the query string for OCO
oco_query_string = '&'.join([f"{key}={oco_params[key]}" for key in oco_params])

# Create the signature for OCO
oco_signature = hmac.new(api_secret.encode(), oco_query_string.encode(), hashlib.sha256).hexdigest()

# Include the signature in the query parameters for OCO
oco_params['signature'] = oco_signature

# Create the request data for OCO
oco_request_data = {
    "url": f"/api/v3/order/oco?{urlencode(oco_params)}",
    "headers": {"X-MBX-APIKEY": api_key},
    "method": "POST",
    "data": None
}

# Send the OCO request
response_oco = requests.post(proxy_url, json={'data': [oco_request_data]})

# Print the response
print(response_oco.content)
