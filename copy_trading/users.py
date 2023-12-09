def add_trade_to_ledger(ledger, trade_id, base_currency, quote_currency, is_open, exchange,
                        amount, stake_amount, strategy, open_rate, realized_profit,
                        close_rate, exit_reason, stop_loss_price, stoploss_order_id,
                        amount_precision, price_precision, precision_mode, contract_size,
                        orders):
    trade_entry = {
        "trade_id": trade_id,
        "base_currency": base_currency,
        "quote_currency": quote_currency,
        "is_open": is_open,
        "exchange": exchange,
        "amount": amount,
        "stake_amount": stake_amount,
        "strategy": strategy,
        "open_rate": open_rate,
        "realized_profit": realized_profit,
        "close_rate": close_rate,
        "exit_reason": exit_reason,
        "stop_loss_price": stop_loss_price,
        "stoploss_order_id": stoploss_order_id,
        "amount_precision": amount_precision,
        "price_precision": price_precision,
        "precision_mode": precision_mode,
        "contract_size": contract_size,
        "orders": orders
    }

    ledger["trades"].append(trade_entry)

def create_user_ledger(user_id):
    return {
        "user_id": user_id,
        "trades": []
    }

# Example Usage:
user_id = 1
user_ledger = create_user_ledger(user_id)

# Add a new trade entry
add_trade_to_ledger(
    user_ledger,
    trade_id=5,
    base_currency="BTC",
    quote_currency="USDT",
    is_open=False,
    exchange="binance",
    amount=1.5,
    stake_amount=5000,
    strategy="long",
    open_rate=45000,
    realized_profit=20.5,
    close_rate=46000,
    exit_reason="exit_signal",
    stop_loss_price=44500,
    stoploss_order_id=12345,
    amount_precision=8,
    price_precision=2,
    precision_mode=1,
    contract_size=1,
    orders=[
        {
            "order": "buy",
            "pair": "BTC/USDT",
            "order_id": "123",
            "average_price": 45000,
            "cost": 67500,
            "amount": 1.5,
            "is_open": False,
            "order_date": "2023-01-01 12:30:00",
            "order_timestamp": 1641069000,
            "fee": 1.5,
            "fee_currency": "USDT"
        }
    ]
)

# Print the user ledger data
print(user_ledger)
