import hmac
import hashlib
import requests

def generate_signature(api_secret,**params):
    
    # Create the query string
    query_string = '&'.join([f"{key}={params[key]}" for key in params])
    # Create the signature
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return signature

page_number = [100,0]
def fetch_signal_from_freqtrade():
    
    # Define the API URL
    config_url = "http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/show_config"
    # Define the API URL
    balance_url = "http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/balance"
    # Define the API URL
    trades_url = f"http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/trades?limit={page_number[0]}&offset={page_number[1]}"

    status_url = "http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/status"

    # Define your API credentials
    username = "signal"
    password = "pa$$word"

    # Create a tuple with the username and password
    auth_credentials = (username, password)

    # Send a GET request to the API with HTTP Basic Authentication
    config_response = requests.get(config_url, auth=auth_credentials)
    balance_response = requests.get(balance_url, auth=auth_credentials)
    trades_response = requests.get(trades_url, auth=auth_credentials)
    
    status_response = requests.get(status_url, auth=auth_credentials)

    # Check if the request was successful
    if config_response.status_code == 200 and balance_response.status_code == 200 and trades_response.status_code == 200 and status_response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        config_data = config_response.json()
        balance_data = balance_response.json()
        trades_data = trades_response.json()
        status_data = status_response.json()
        
        # Create an empty list to store the data
        index_list = []
        total_bot = balance_data['total_bot']
        total_trades = trades_data['total_trades']
        offset_store = True
        for tr in trades_data['trades']:
            if tr['is_open'] == True and offset_store == True:
                page_number[1] = tr['trade_id'] - 1
                offset_store = False

            trade_dict= {
            "trade_id": tr['trade_id'],
            "base_currency": tr['base_currency'],
            "quote_currency": tr['quote_currency'],
            "is_open":tr['is_open'],
            "stake_amount": tr['stake_amount'],
            "total_bot": total_bot,
            "stake_ratio": tr['stake_amount']/total_bot, 
            "open_timestamp": tr['open_timestamp'],
            "open_rate": tr['open_rate'],
            "stop_loss_ratio": tr['stop_loss_ratio'],
            "stoploss": tr['open_rate']*(1+tr['stop_loss_ratio']), 
            "exchange": tr['exchange'],
            "exit_reason": tr['exit_reason'],
            "realized_profit":tr['realized_profit']
            }
            index_list.append(trade_dict)
        page_number[0] = total_trades - page_number[1]
        # Print the list 
        print(f"Total trades = {total_trades}, Total Bot = {total_bot}, limit = {page_number[0]}, offset = {page_number[1]}")
    else:
        print("Error fetching data from API:")

        # Iterate through list_a and list_b to update list_a
        for item_a in index_list:
            for item_b in status_data:
                if item_a["trade_id"] == item_b["trade_id"]:
                    # Check conditions for updating is_open in list_a
                    if item_a["is_open"] and not item_b["is_open"]:
                        list_a.remove(item_a)
                    elif not item_a["is_open"] and item_b["is_open"]:
                        list_a.append(item_b)

        # Remove duplicates from list_a
        list_a = [dict(t) for t in {tuple(d.items()) for d in list_a}]
        # Print the updated list_a
        print(list_a)


fetch_signal_from_freqtrade()
