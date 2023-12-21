user_trade_list = []

main_list = {
    "total_trades": 0,
    "stake_capital": 0,
	"deposit_queue": 0,
    "withdraw_queue": 0,
    "open_orders": [0,0,0]
}


trade_entry = {
    "trade_id": 0,
    "base_currency": None,
    "quote_currency": None,
    "is_open": None,
    "exchange": None,
    "amount": 0,
    "stake_amount": None,
    "strategy": None,
    "open_rate": 0,
    "realized_profit": 0,
    "close_rate": 0,
    "exit_reason": None,
    "stop_loss_price": 0,
    "stoploss_order_id": 0,
    "amount_precision": 0,
    "price_precision": 0,
    "precision_mode": None,
    "contract_size": 0,
    "orders": []
}
    # orders=[
    #     {
    #         "order": "buy",
    #         "pair": "BTC/USDT",
    #         "order_id": "123",
    #         "average_price": 45000,
    #         "cost": 67500,
    #         "amount": 1.5,
    #         "is_open": False,
    #         "order_date": "2023-01-01 12:30:00",
    #         "order_timestamp": 1641069000,
    #         "fee": 1.5,
    #         "fee_currency": "USDT"
    #     }
    # ]


# Print the user ledger data
# ledger_indexr = []
# user_trade_list.append(trade_entry)
# print(user_trade_list)


# for trade in user_trade_list:
#     trade['trade_id']
#     trade['is_open']
#     for ledger in ledger_indexr:
#         trade['trade_id'] =  ledger['trade_id']
#         trade['stake_amount'] = ledger['stake_amount']
#         trade['realized_profit'] = ledger['realized_profit']
#         trade['exit_reason'] = ledger['exit_reason']

user_all_trade=[]
trades = []
def user_open_trade(user_id, indexer_data, broker_data):
    trade_entry = {
        "trade_id": indexer_data['trade_id'],
        "base_currency": indexer_data['base_currency'],
        "quote_currency": indexer_data['quote_currency'],
        "is_open": indexer_data['is_open'],
        "exchange": indexer_data['exchange'],
        "amount": indexer_data['amount'],
        "stake_amount": indexer_data['stake_amount'],
        "strategy": indexer_data['strategy'],
        "open_rate": indexer_data['open_rate'],
        "realized_profit": indexer_data['realized_profit'],
        "close_rate": indexer_data['close_rate'],
        "exit_reason": indexer_data['exit_reason'],
        "stop_loss_price": indexer_data['stop_loss_price'],
        "stoploss_order_id": indexer_data['stoploss_order_id'],
        "amount_precision": indexer_data['amount_precision'],
        "price_precision": indexer_data['price_precision'],
        "precision_mode": indexer_data['precision_mode'],
        "contract_size": indexer_data['contract_size'],
        "orders": indexer_data['orders']
    }
    user_trade = {
        user_id:[trades.append(trade_entry)]
    }

    