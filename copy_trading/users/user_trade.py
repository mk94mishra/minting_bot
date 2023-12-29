from sqlalchemy.orm import Session
from sqlalchemy import text
from db import engine
from users.models import *
from trades.models import *
import create_order as ct
import time
import config as config


def users_trade_settings():
    print("users_trade")

    with Session(engine) as session:
        # fetch open trades from user_trade tbl
        trade_ids_result = session.query(UserTrade.trade_id).group_by(UserTrade.trade_id,UserTrade.user_id).filter(UserTrade.is_open == True).all()
        trade_ids_to_filter = [result[0] for result in trade_ids_result]
        # fetch close trades from ledger, which is still open in user_trade tbl
        closed_trade_ids_result = session.query(Trade).filter(Trade.trade_id.in_(trade_ids_to_filter), Trade.is_open == False).all()

        trade_ids_to_close = []
        trade_ids_close_stop_loss = []
        trade_ids_close_exit_signal = []
        for result in closed_trade_ids_result:
            trade_ids_to_close.append(result.trade_id)
            if result.exit_reason == 'stop_loss':
                trade_ids_close_stop_loss.append(result.trade_id)
            if result.exit_reason == 'exit_signal':
                trade_ids_close_exit_signal.append(result.trade_id)

        if trade_ids_to_close != []:
            open_trade_ids_user_trades = session.query(UserTrade,Broker).join(UserTrade, Broker.user_id == UserTrade.user_id).filter(UserTrade.trade_id.in_(trade_ids_to_close), UserTrade.is_open == True, Broker.is_active == True).all()
            
            final_order_list = []
            final_sl_closed_order_list = []
            for ot, bt in open_trade_ids_user_trades:
                # Execute the query with parameters using the session
                client_order_id = f"{config.broker_id}-S-{ot.user_id}-{ot.trade_id}"
                result = session.execute(text("SELECT client_order_id, order_id FROM proxy_log WHERE client_order_id = :client_order_id and order_id is not null"), {"client_order_id": client_order_id})
                exist_trade = result.fetchall()
                print("prrrr-",result.fetchall())
                try:
                    cancelOrderId = result[0].order_id
                except:
                    cancelOrderId = 0

                if exist_trade == []:
                    if ot.trade_id in trade_ids_close_exit_signal:
                        params = {
                            'symbol': f'{ot.base_currency}{ot.quote_currency}',
                            'side': 'SELL',
                            'type': 'MARKET',
                            'quantity': ot.amount,
                            'cancelReplaceMode':'STOP_ON_FAILURE',
                            'cancelOrderId':cancelOrderId,
                            'newClientOrderId': client_order_id,
                            'timestamp': int(time.time() * 1000),
                            'recvWindow': 60000,
                        }                            
                        print(params)
                        if ot.trade_id in trade_ids_close_stop_loss:
                            result = session.execute(text("SELECT client_order_id, order_id FROM proxy_log WHERE trade_id = :trade_id and user_id = :user_id and order_id is not null and trade_type = 'SL'"), {"trade_id": ot.trade_id,'user_id':ot.user_id})
                            exist_trade = result.fetchall()
                            if exist_trade:
                                sl_params = {
                                    'symbol': f'{ot.base_currency}{ot.quote_currency}',
                                    'orderId': exist_trade[0].order_id,
                                    'timestamp': int(time.time() * 1000),
                                    'recvWindow': 60000,
                                }
                                final_sl_closed_order_list.append([bt.api_key, bt.api_secret, sl_params])
                        final_order_list.append([bt.api_key, bt.api_secret, params])
            trade_ids_close_stop_loss = []
            trade_ids_close_exit_signal = []
            # close open trades
            ct.create_order(final_order_list)
            # sl close list trades
            ct.create_order(final_sl_closed_order_list)
        session.close()

        

    # open new orders
    with Session(engine) as session:
        all_users_trades = []
        active_users = session.query(Users,Broker).join(Users, Broker.user_id == Users.id).filter(Users.is_active == True).all()
        all_open_trades = session.query(Trade).filter(Trade.is_open == True).all()

        for open_trades in all_open_trades:
            for u,b in active_users:
                trades = {
                    'user_id' : u.id,
                    'api_key' : b.api_key,
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
                # all_users_trades.append(UserTrade(**trades))
                
                session.add(UserTrade(**trades))
                try:
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print("trade exist", e)
                # Close the session
        session.close()
            # session.add_all(all_users_trades)
            # all_users_trades = []
            # Commit the changes to the database
            # session.commit()

    with Session(engine) as session:
        open_trade_ids_user_trades = session.query(UserTrade,Broker).join(UserTrade, Broker.user_id == UserTrade.user_id).filter(UserTrade.is_open == True, Broker.is_active == True).all()
        
        final_order_list = []
        for ot, bt in open_trade_ids_user_trades:
            # Execute the query with parameters using the session
            client_order_id = f"{config.broker_id}-B-{ot.user_id}-{ot.trade_id}"
            result = session.execute(text("SELECT client_order_id FROM proxy_log WHERE client_order_id = :client_order_id and order_id is not null"), {"client_order_id": client_order_id})
            exist_trade = result.fetchall()
            print("prt-",exist_trade)
            if exist_trade == []:
                params = {
                    'symbol': f'{ot.base_currency}{ot.quote_currency}',
                    'side': 'BUY',
                    'type': 'MARKET',
                    'quoteOrderQty': ot.stake_amount,
                    'newClientOrderId': client_order_id,
                    'timestamp': int(time.time() * 1000),
                    'recvWindow': 60000,
                }
                final_order_list.append([bt.api_key, bt.api_secret, params])
        print(ct.create_order(final_order_list))

        final_order_list = []
        for ot, bt in open_trade_ids_user_trades:
            # Execute the query with parameters using the session
            client_order_id = f"{config.broker_id}-SL-{ot.user_id}-{ot.trade_id}"
            result = session.execute(text("SELECT client_order_id FROM proxy_log WHERE client_order_id = :client_order_id and order_id is not null"), {"client_order_id": client_order_id})
            exist_trade = result.fetchall()
            print("prtsl-",exist_trade)
            if exist_trade == []:
                params = {
                    'symbol': f'{ot.base_currency}{ot.quote_currency}',
                    'side': 'SELL',
                    'type': 'STOP_LOSS',
                    'quantity': ot.amount,
                    'stopPrice': ot.stop_loss_abs,
                    'newClientOrderId': client_order_id,
                    'timestamp': int(time.time() * 1000),
                    'recvWindow': 60000,
                }
                final_order_list.append([bt.api_key, bt.api_secret, params])
        print(ct.create_order(final_order_list))
        session.close() 


    


