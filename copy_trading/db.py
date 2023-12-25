from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


import sqlalchemy as sa

# Replace with your PostgreSQL credentials and database details
username = "postgres"
password = "123456"
host = "localhost"
port = 5432  # Default PostgreSQL port
database = "db_mintingbot"

# Construct the connection string
database_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(database_url)

Base = declarative_base()


from trades.models import *
from users.models import *

Base.metadata.create_all(engine)


