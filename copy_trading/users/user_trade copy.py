from users.models import *
from trades.models import *
from db import *
from create_order import *
import time
# # Create a session
# with Session(engine) as session:
#     # Insert dummy data into the Users table
#     dummy_users = [
#         Users(name='Alice', email='alice@example.com', is_active=True),
#         Users(name='Bob', email='bob@example.com', is_active=False),
#         Users(name='Charlie', email='charlie@example.com', is_active=True),
#     ]

#     # Add the dummy users to the session
#     session.add_all(dummy_users)
    
#     # Commit the changes to the database
#     session.commit()


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

        open_trade_ids_user_trades = session.query(UserTrade,Broker).join(UserTrade, Broker.user_id == UserTrade.user_id).group_by(UserTrade.trade_id, UserTrade.user_id).filter(Trade.trade_id.in_(trade_ids_to_close), UserTrade.is_open == True).all()
        
        final_order_list = []
        for ot, bt in open_trade_ids_user_trades:
            params = {
                'symbol': f'{ot.base_currency}{ot.quote_currency}',
                'side': 'SELL',
                'type': 'MARKET',
                # 'quantity': ot.stake_amount,
                'quantity': 0.0005,
                'timestamp': int(time.time() * 1000),
            }
            final_order_list.append([bt.api_key, bt.api_secret, params])
        print(create_order(final_order_list))
    # active_users = fetch_all_users()
    # all_users_trades = []
    
    # with Session(engine) as session:
    #     all_open_trades = session.query(Trade).filter(Trade.is_open == False).all()
    #     for open_trades in all_open_trades:
    #         for u in active_users:
    #             trades = {
    #                 'user_id' : u.id,
    #                 "trade_id": open_trades.trade_id,
    #                 "base_currency": open_trades.base_currency,
    #                 "quote_currency": open_trades.quote_currency,
    #                 "exchange": open_trades.exchange,
    #                 "is_open": open_trades.is_open,
    #                 "stake_amount": open_trades.stake_amount,
    #                 "open_rate": open_trades.open_rate,
    #                 # "stop_loss_abs": open_trades.stop_loss_abs,
    #                 "exit_reason": open_trades.exit_reason,
            
    #                 "realized_profit": open_trades.realized_profit,
    #             }
    #             all_users_trades.append(UserTrade(**trades))
    #         session.add_all(all_users_trades)
    #         all_users_trades = []
    #         # Commit the changes to the database
    #         session.commit()

        # Query open trades
        # open_trades = session.query(Trade).filter(Trade.is_open == True).all()

        # users_open_trades = session.query(UserTrade).filter(UserTrade.is_open == True).all()
        # print(users_open_trades)



def create_user_trade_log(**trade_data):

    with Session(engine) as session:
        # Query open trades
        open_trades = session.query(Trade).filter(Trade.is_open == True).all()

        users_open_trades = session.query(UserTrade).filter(UserTrade.is_open == True).all()
        print(users_open_trades)







#     all_users_trades = []
#     active_users = fetch_all_users()
#     for u in active_users:
#         trades = {
#             'user_id' : u.id,
#             "trade_id": trade_data['trade_id'],
#             "base_currency": trade_data['base_currency'],
#             "quote_currency": trade_data['quote_currency'],
#             "exchange": trade_data['exchange'],
#             "is_open": trade_data['is_open'],
#             "stake_amount": trade_data['stake_amount'],
#             "open_rate": trade_data['open_rate'],
#             "stop_loss_abs": trade_data['stop_loss_abs'],
#             "exit_reason": trade_data['exit_reason'],
#             "realized_profit": trade_data['realized_profit'],
#         }
#         all_users_trades.append(trades)
#     session.add_all(all_users_trades)
#     # Commit the changes to the database
#     session.commit()

def fetch_all_users():
    # Fetch all records from the table
    with Session(engine) as session:
        active_users = session.query(Users).filter(Users.is_active == True).all()
    return active_users

# all_users = fetch_all_users()

# for u in all_users:
#     print(u.name)