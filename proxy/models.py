from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON,ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base

# import sys
# # Add a directory to sys.path
# new_directory = '../'
# sys.path.append(new_directory)
from db import *
Base = declarative_base()


class ProxyLog(Base):
    __tablename__ = 'proxy_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    trade_id = Column(Integer)
    order_id = Column(Integer)
    request = Column(JSON)
    response = Column(JSON)

Base.metadata.create_all(engine)

