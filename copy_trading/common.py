import requests
import time

# Define your API credentials
username = "signal"
password = "pa$$word"

# Create a tuple with the username and password
auth_credentials = (username, password)

def fetch_open_order_list():
    response = requests.get("http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/status", auth=auth_credentials)
    return response.json()

def fetch_trade_log(limit, offset):
    response = requests.get(f"http://ec2-18-61-34-119.ap-south-2.compute.amazonaws.com:8080/api/v1/trades?limit={limit}&offset={offset}", auth=auth_credentials)
    return response.json()


page_number = [200,0]
open_order_ledger_one = {
        "total_trades": 0,
        "stake_capital": 10000,
        "open_orders": [],
        "closed_orders": []
    }

open_order_ledger_two = []
def make_open_order_ledger(open_order):
    for ot in open_order:
        if ot['is_open'] == True:
            ledger = {
                    "trade_id": ot['trade_id'],
                    "base_currency": ot['base_currency'],
                    "quote_currency": ot['quote_currency'],
                    "exchange": ot['exchange'],
                    "is_open": ot['is_open'],
                    "stake_amount": ot['stake_amount'],
                    "open_rate": ot['open_rate'],
                    "stop_loss_abs": ot['stop_loss_abs'],
                    "exit_reason": ot['exit_reason'],
                    "realized_profit": ot['realized_profit'],
                }
            open_order_ledger_one['open_orders'].append(ot['trade_id'])
            open_order_ledger_two.append(ledger)
        page_number[1] = min(open_order_ledger_one['open_orders']) - 1 
        open_order_ledger_one['total_trades']=ot['trade_id']


while True:
    trade_log = fetch_trade_log(page_number[0],page_number[1])
    for tl in trade_log['trades']:
        if tl['trade_id'] not in open_order_ledger_one['open_orders']:
            if tl['is_open'] == False:
                ledger = {
                        "trade_id": tl['trade_id'],
                        "base_currency": tl['base_currency'],
                        "quote_currency": tl['quote_currency'],
                        "exchange": tl['exchange'],
                        "is_open": tl['is_open'],
                        "stake_amount": tl['stake_amount'],
                        "open_rate": tl['open_rate'],
                        "stop_loss_abs": tl['stop_loss_abs'],
                        "exit_reason": tl['exit_reason'],
                        "realized_profit": tl['realized_profit'],
                    }
                open_order_ledger_two.append(ledger)
                open_order_ledger_one['stake_capital'] = open_order_ledger_one['stake_capital']+tl['realized_profit']
                open_order_ledger_one['total_trades']=tl['trade_id']
                open_order_ledger_one['closed_orders'].append(tl['trade_id'])

    open_order = fetch_open_order_list()
    status_open_order_list = []
    for ot in open_order:
        if ot['is_open'] == True:
            status_open_order_list.append(ot['trade_id'])

    open_order_ledger_one['open_orders'].sort()
    status_open_order_list.sort()
    if open_order_ledger_one['open_orders'] != status_open_order_list:
        make_open_order_ledger(open_order)
        
        for tl in trade_log['trades']:
            if tl['trade_id'] in open_order_ledger_one['open_orders']:
                for opi in open_order_ledger_two:
                    if opi['trade_id'] == tl['trade_id']:
                        opi['realized_profit'] = tl['realized_profit']
                        open_order_ledger_one['stake_capital'] = open_order_ledger_one['stake_capital']+tl['realized_profit']
                        open_order_ledger_one['exit_reason'] = tl['exit_reason']
                        
                open_order_ledger_one['open_orders'].remove(tl['trade_id'])
    
    trades = [
        {"trades":open_order_ledger_two},
        open_order_ledger_one
    ]
    print(trades)

    current_hour = time.localtime().tm_hour
    # Sleep until the next hour starts
    time_to_sleep = (60 - time.localtime().tm_min) * 60 - time.localtime().tm_sec
    time.sleep(time_to_sleep)

