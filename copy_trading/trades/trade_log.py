from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


from trades.models import *
from db import *


def create_trade_log(trade_data):
    
    # Create a session
    with Session(engine) as session:
        existing_trade = session.query(Trade).filter(Trade.trade_id == trade_data['trade_id']).first()
        if existing_trade:
            # Update the existing trade's attributes
            existing_trade.realized_profit = trade_data['realized_profit']
            existing_trade.exit_reason = trade_data['exit_reason']
            existing_trade.is_open = trade_data['is_open']

            # Commit the changes to the database
            session.commit()
        else:
            session.add(Trade(**trade_data))
            # Commit th changes to the database
            session.commit()


def create_all_trade_log(trade_data):
    # Create a session
    with Session(engine) as session:
        existing_trade = session.query(AllTrade).filter(AllTrade.id == 1).first()
        if existing_trade:
            # Update the existing trade's attributes
            existing_trade.total_trades = trade_data['total_trades']
            existing_trade.stake_capital = trade_data['stake_capital']
            existing_trade.offset = trade_data['offset']

            # Commit the changes to the database
            session.commit()
        else:
            del trade_data['closed_orders']
            session.add(AllTrade(**trade_data))
            # Commit th changes to the database
            session.commit()

