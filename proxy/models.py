from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON,ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProxyLog(Base):
    __tablename__ = 'proxy_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    client_order_id = Column(String)
    trade_id = Column(Integer)
    trade_type = Column(String)
    order_id = Column(Integer)
    request = Column(JSON)
    response = Column(JSON)

# Base.metadata.create_all(engine)

