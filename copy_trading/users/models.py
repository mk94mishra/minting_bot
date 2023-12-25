from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base
from db import *


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    password = Column(String)
    is_active = Column(Boolean)
    extra = Column(String)


class Broker(Base):
    __tablename__ = 'broker'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    api_key = Column(String)
    api_secret = Column(String)
    is_active = Column(Boolean)
    extra = Column(String)
    

class UserTrade(Base):
    __tablename__ = 'user_trades'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    api_key = Column(String)
    trade_id = Column(Integer)
    base_currency = Column(String)
    quote_currency = Column(String)
    is_open = Column(Boolean)
    exchange = Column(String)
    amount = Column(Float)
    stake_amount = Column(Float)
    strategy = Column(String)
    open_rate = Column(Float)
    realized_profit = Column(Float)
    close_rate = Column(Float)
    exit_reason = Column(String)
    stop_loss_abs = Column(Float)
    stop_loss_price = Column(Float)
    stoploss_order_id = Column(Integer)
    amount_precision = Column(Integer)
    price_precision = Column(Integer)
    precision_mode = Column(Integer)
    contract_size = Column(Integer)
    orders = Column(JSON)
    flag_one_open = Column(Integer)
    flag_two_open = Column(Integer)
    flag_one_close = Column(Integer)
    flag_two_close = Column(Integer)

    __table_args__ = (
        UniqueConstraint('user_id', 'trade_id', name='uq_user_trade'),
    )

class UserAllTrade(Base):
    __tablename__ = 'user_all_trades'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_trades = Column(Integer)
    stake_capital = Column(String)
    deposit_queue = Column(String)
    withdraw_queue = Column(String)
    open_orders = Column(JSON)


Base.metadata.create_all(engine)