from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float,DateTime, func
from sqlalchemy.orm import sessionmaker

# Create an engine to connect to the database
engine = create_engine('sqlite:///users.db')

# Create a declarative base for defining models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'tbl_users'
    id=Column('id', Integer, primary_key=True, autoincrement=True),
    username=Column('username', String(50), nullable=False, unique=True),  
    email=Column('email', String(100), nullable=False, unique=True),    
    password=Column('password', String(255), nullable=False),
    mobile=Column('mobile', String(20), nullable=True, unique=True),     
    signup_type=Column('signup_type', String(20), nullable=True),


# Define the broker model
class broker(Base):
    __tablename__ = 'tbl_broker'
    id=Column('id', Integer, primary_key=True, autoincrement=True),
    user_id=Column('user_id', Integer, nullable=False), 
    api_key=Column('api_key', String(255), nullable=False, unique=True),    
    api_secret=Column('api_secret', String(255), nullable=False, unique=True),
    broker=Column('broker', String(50), nullable=True), 


# Define the ledger model
class ledger(Base):
    __tablename__ = 'tbl_ledger'
    id=Column('id', Integer, primary_key=True, autoincrement=True),
    symbol=Column('symbol', String(20), nullable=False), 
    quantity=Column('quantity', Float),
    price=Column('api_secret', Float),
    fee=Column('broker', Float), 
    net_price=Column('broker', Float),
    profit_loss=Column('broker', Float),
    total_profit_loss=Column('broker', Float),
    current_time=Column('current_time', DateTime, default=func.current_timestamp(), nullable=False)
    execute_time=Column('execute_time', String(20)),
    status=Column('status', String(20), nullable=False),



# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a new user
new_user = User(username='johndoe', email='johndoe@example.com', password='password123')

# Add the new user to the session
session.add(new_user)

# Commit the changes to the database
session.commit()

# Print the user's id
print(new_user.id)
