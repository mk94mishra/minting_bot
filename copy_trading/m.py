import ccxt
import sys

# Replace 'YOUR_API_KEY2' and 'YOUR_SECRET_KEY2' with your actual Binance API key and secret
api_key = 'YOUR_API_KEY2'
api_secret = 'YOUR_SECRET_KEY2'

# Initialize the Binance exchange object
binance_instance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

# Get the memory usage of the instance in bytes
memory_usage = sys.getsizeof(binance_instance)
print(f"Memory usage of Binance instance: {memory_usage} bytes")


# Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual Binance API key and secret
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_SECRET_KEY'

# Initialize the Binance exchange object
binance_instance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

try:
    # Fetch a sample order (replace 'YOUR_ORDER_ID' with an actual order ID)
    order_id = 'YOUR_ORDER_ID'
    order = binance_instance.fetch_order(order_id)

    # Get the memory usage of the order data in bytes
    memory_usage = sys.getsizeof(order)
    print(f"Memory usage of order data: {memory_usage} bytes")

except ccxt.ExchangeError as e:
    print(f"Error fetching order: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
