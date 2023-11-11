import ccxt
from concurrent.futures import ThreadPoolExecutor

# Replace 'http://your-proxy-url' with the actual proxy URL you want to use
proxy_url = 'http://127.0.0.1:8000/call_api/?bin_api=binaance.api/'


api_key = 'Nw3cglPnQmqtJVCyjOp84CYfB9T0lcwT9Jm93hPbyAhEgR23mNz8gnkZuPXtfJwJ'
api_secret = 'bsl0oeBw2sxni3PnOt9PpEnPmKQ9gB3IQVPYlzITTCzeJXGrW2vWAhByQjWFtcbu'

# Define a list of user credentials (API keys and secrets)
userrrr = {"api_key": api_key, "api_secret": api_secret}
users = [userrrr]*2   
# Initialize the Binance exchange object with a proxy
def create_binance_instance(api_key, api_secret):
    binance_exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': api_secret,
    })
    return binance_exchange

# Define order parameters
symbol = 'BTC/USDT'
quantity = 0.001  # Example quantity, adjust as needed
order_type = 'limit'  # Example order type, use 'limit' or 'market'

# Place orders concurrently
with ThreadPoolExecutor(max_workers=len(users)) as executor:
    instances = list(executor.map(create_binance_instance, [user['api_key'] for user in users], [user['api_secret'] for user in users]))

    def place_order(instance, user):
        try:
            order = instance.create_order(
                symbol=symbol,
                side='buy',  # or 'sell' for sell orders
                type=order_type,
                amount=quantity  # Use 'quantity' instead of 'amount'
            )
            print(f"Order placed for user with API key: {user['api_key']}")
            print(order)

        except ccxt.ExchangeError as e:
            print(f"Error placing order for user with API key {user['api_key']}: {e}")

        except Exception as e:
            print(f"An unexpected error occurred for user with API key {user['api_key']}: {e}")

    executor.map(place_order, instances, users)
