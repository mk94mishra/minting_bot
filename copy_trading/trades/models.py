from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON,ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base

# import sys
# # Add a directory to sys.path
# new_directory = '../'
# sys.path.append(new_directory)
from db import *
Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer,unique=True)
    base_currency = Column(String)
    quote_currency = Column(String)
    is_open = Column(Boolean)
    exchange = Column(String)
    amount = Column(Float)
    stake_amount = Column(Float)
    stop_loss_abs = Column(Float)
    open_rate = Column(Float)
    realized_profit = Column(Float)
    exit_reason = Column(String)
    amount_precision = Column(Integer)
    price_precision = Column(Integer)
    precision_mode = Column(Integer)
    contract_size = Column(Integer)


class AllTrade(Base):
    __tablename__ = 'all_trade'
    id = Column(Integer, primary_key=True)
    total_trades = Column(Integer)
    stake_capital = Column(String)
    open_orders = Column(JSON)
    offset = Column(Integer)


Base.metadata.create_all(engine)

