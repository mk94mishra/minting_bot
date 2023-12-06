import requests

def get_binance_price(symbol):
    base_url = 'https://api.binance.com/api/v3/ticker/price'
    
    # Specify the symbol for which you want to get the price
    params = {'symbol': symbol}
    
    # Make a GET request to the Binance API
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response and extract the current price
        data = response.json()
        current_price = float(data['price'])
        return current_price
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

# Specify the symbol for which you want to get the price (e.g., BTCUSDT)
symbol = 'BTCUSDT'

# Fetch the current market price
price = get_binance_price(symbol)

# Print the current price
if price is not None:
    print(f'Current {symbol} Price: {price}')
