import concurrent.futures
import hashlib
import hmac
import time
import http.client
from urllib.parse import urlencode

# Replace with your Binance API key and secret
api_key = 'Nw3cglPnQmqtJVCyjOp84CYfB9T0lcwT9Jm93hPbyAhEgR23mNz8gnkZuPXtfJwJ'
api_secret = 'bsl0oeBw2sxni3PnOt9PpEnPmKQ9gB3IQVPYlzITTCzeJXGrW2vWAhByQjWFtcbu'

# Define order parameters
symbol = 'BTCUSDT'
quantity = 0.001
price = 60000
side = 'BUY'  # or 'SELL'
type = 'LIMIT'  # or 'MARKET'
time_in_force = 'GTC'  # Good 'til canceled

# Binance API endpoint
endpoint = '/api/v3/order'

# Current timestamp in mi     lliseconds
timestamp = int(time.time() * 1000)

# Create the query parameters
params = {
    'symbol': symbol,
    'side': side,
    'type': type,
    'timeInForce': time_in_force,
    'quantity': quantity,
    'price': price,
    'timestamp': timestamp,
    'recvWindow': 5000  # Adjust as needed
}

# Generate the query string
query_string = urlencode(params)

# Create the signature
signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

# Include the signature in the query parameters
params['signature'] = signature

# Function to make the Binance API call
def make_binance_order(user):
    url = f'http://18.60.247.215:8000{endpoint}'

    conn = http.client.HTTPSConnection('http://18.60.247.215:8000')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-MBX-APIKEY': user['api_key'],
    }
    body={
         "url": f"{endpoint}?{urlencode(params)}",
        "method": "POST"
    }

    conn.request('POST', url, headers=headers)
    response = conn.getresponse()

    print(f"User {user['api_key']} - Status: {response.status}")
    print(f"User {user['api_key']} - Response: {response.read().decode()}")

    conn.close()

# Create a list of users
users = [
    {"api_key": api_key, "api_secret": api_secret},
    {"api_key": api_key, "api_secret": api_secret},
    # Add more user credentials here
    # ...
]

# Make concurrent API calls using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(make_binance_order, users)
