import requests

# Define your API credentials
username = "signal"
password = "pa$$word"

# Create a tuple with the username and password
auth_credentials = (username, password)

def fetch_open_order_list():
    response = requests.get("http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/status",auth=auth_credentials)
    return response.json()

def fetch_trade_log(limit, offset):
    response = requests.get(f"http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/trades?limit={limit}&offset={offset}",auth=auth_credentials)
    return response.json()
ledger_one=[]
def update_ledger(ledger,ledger_two, trade_log_entry):
    ledger_two["stake_capital"] += trade_log_entry.get("realized_profit", 0)
    ledger_one.append(ledger)

def main():
    ledger = {
        "trade_id": 0,
        "base_currency": "",
        "quote_currency": "USDT",
        "exchange": "binance",
        "is_open": False,
        "stake_amount": 0,
        "open_rate": 0,
        "stop_loss_abs": 0,
        "exit_reason": "",
        "realized_profit": 0,

    }
    ledger_two={
        "total_trades": 100,
        "offset": 0,
        "stake_capital": 10000,
        "open_orders": []
    }

    while True:
        # Fetch open order list from Signal
        signal_open_orders = fetch_open_order_list()

        # Check if there are any differences in open orders
        if set(ledger_two["open_orders"]) == set([order["trade_id"] for order in signal_open_orders]):
            # No changes in open orders, continue to the next iteration
            continue

        # Fetch current trade log
        trade_log = fetch_trade_log(limit=100, offset=ledger_two["offset"])

        for order_id in ledger_two["open_orders"]:
            if order_id not in [order["trade_id"] for order in signal_open_orders]:

                # Add new orders to trade log and update ledger
                for order in signal_open_orders:
                    if order["trade_id"] not in ledger_two["open_orders"]:
                        # Add the new order to the trade log
                        trade_log_entry = {}  # Get the trade log entry from the status response
                        update_ledger(ledger_two, trade_log_entry)

        # Update offset to (min(open_orders) - 1)
        ledger_two["offset"] = min(ledger_two["open_orders"]) - 1

if __name__ == "__main__":
    main()
