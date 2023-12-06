import requests


# Define your API credentials
username = "signal"
password = "pa$$word"

# Create a tuple with the username and password
auth_credentials = (username, password)

def update_indexer_ledger(ledger):
    # Fetch Open Order List from Signal
    signal_open_order_response = requests.get('http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/status',auth=auth_credentials)
    signal_open_orders = signal_open_order_response.json()
    signal_open_order_ids = [order['trade_id'] for order in signal_open_orders]

    # Update ledger with new open orders
    for order in signal_open_orders:
        if order['trade_id'] not in ledger['open_orders']:
            ledger['open_orders'].append(order['trade_id'])

    # Fetch Current Trade Log from Signal
    signal_trade_log_response = requests.get('http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/trades', params={'limit': 100, 'offset': ledger['offset']},auth=auth_credentials)
    signal_trades = signal_trade_log_response.json()
    signal_trade_ids = [trade['trade_id'] for trade in signal_trades['trades']]

    # Update ledger with realized profit
    for trade in signal_trades['trades']:
        if trade['is_open'] == False:
            ledger['stake_capital'] += trade['realized_profit']

    # Update ledger with closed orders
    for order_id in ledger['open_orders']:
        if order_id not in signal_trade_ids:
            ledger['open_orders'].remove(order_id)

    # Update ledger with new open orders from trade log
    for trade in signal_trades['trades']:
        if trade['is_open'] == True and trade['trade_id'] not in ledger['open_orders']:
            ledger['open_orders'].append(trade['trade_id'])

    # Update offset
    ledger['offset'] = min(ledger['open_orders']) - 1 if len(ledger['open_orders']) > 0 else 0

    return ledger

# Initialize Indexer Ledger
ledger = {
    'trade_id': 0,
    'base_currency': 'string',
    'quote_currency': 'USDT',
    'exchange': 'binance',
    'is_open': False,
    'stake_amount': 0,
    'open_rate': 0,
    'stop_loss_abs': 0,
    'exit_reason': 'string',
    'realized_profit': 0,
    'total_trades': 100,
    'offset': 0,
    'stake_capital': 10000,
    'open_orders': [0, 0, 0]
}

# Update Indexer Ledger continuously
i=0
while i<500:
    i=i+1
    ledger = update_indexer_ledger(ledger)
print(ledger)
