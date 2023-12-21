from users.models import *
from trades.models import *
from db import *
import create_order as ct
import time
import config as config


def users_trade_settings():
    print("users_trade")

    with Session(engine) as session:

        # fetch open trades from user_trade tbl
        trade_ids_result = session.query(UserTrade.trade_id).group_by(UserTrade.trade_id).filter(UserTrade.is_open == True).all()
        trade_ids_to_filter = [result[0] for result in trade_ids_result]
        # fetch close trades from ledger, which is still open in user_trade tbl
        closed_trade_ids_result = session.query(Trade).filter(Trade.trade_id.in_(trade_ids_to_filter), Trade.is_open == False).all()

        trade_ids_to_close = []
        for result in closed_trade_ids_result:
            trade_ids_to_close.append(result.trade_id)

        open_trade_ids_user_trades = session.query(UserTrade,Broker).join(UserTrade, Broker.user_id == UserTrade.user_id).group_by(UserTrade.trade_id, UserTrade.user_id).filter(Trade.trade_id.in_(trade_ids_to_close), UserTrade.is_open == True, Broker.is_active == True).all()
        
        final_order_list = []
        for ot, bt in open_trade_ids_user_trades:
            params = {
                'symbol': f'{ot.base_currency}{ot.quote_currency}',
                'side': 'SELL',
                'type': 'MARKET',
                'quantity': ot.amount,
                'timestamp': int(time.time() * 1000),
            }
            print(params)
            final_order_list.append([bt.api_key, bt.api_secret, params])

        print(ct.create_order(final_order_list))


    # open new orders
    with Session(engine) as session:
        all_users_trades = []
        active_users = session.query(Users).filter(Users.is_active == True).all()
        all_open_trades = session.query(Trade).filter(Trade.is_open == True).all()
        for open_trades in all_open_trades:
            for u in active_users:
                trades = {
                    'user_id' : u.id,
                    "trade_id": open_trades.trade_id,
                    "base_currency": open_trades.base_currency,
                    "quote_currency": open_trades.quote_currency,
                    "exchange": open_trades.exchange,
                    "is_open": open_trades.is_open,
                    "stake_amount": open_trades.stake_amount,
                    "amount": open_trades.amount,
                    "open_rate": open_trades.open_rate,
                    "stop_loss_abs": open_trades.stop_loss_abs,
                    "exit_reason": open_trades.exit_reason,
                    "realized_profit": open_trades.realized_profit,
                    "amount_precision":open_trades.amount_precision,
                    "price_precision":open_trades.price_precision,
                    "precision_mode":open_trades.precision_mode,
                    "contract_size":open_trades.contract_size,
                }
                all_users_trades.append(UserTrade(**trades))
                session.add_all(all_users_trades)
            all_users_trades = []
            # Commit the changes to the database
            session.commit()


        open_trade_ids_user_trades = session.query(UserTrade,Broker).join(UserTrade, Broker.user_id == UserTrade.user_id).group_by(UserTrade.trade_id, UserTrade.user_id).filter(UserTrade.is_open == True).all()
        
        final_order_list = []
        for ot, bt in open_trade_ids_user_trades:
            params = {
                'symbol': f'{ot.base_currency}{ot.quote_currency}',
                'side': 'BUY',
                'type': 'MARKET',
                'quoteOrderQty': ot.stake_amount,
                'timestamp': int(time.time() * 1000),
            }
            final_order_list.append([bt.api_key, bt.api_secret, params])
        print(ct.create_order(final_order_list))
            

    


