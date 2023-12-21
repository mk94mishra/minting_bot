from sqlalchemy import create_engine
import sys
# Add a directory to sys.path
new_directory = './'
sys.path.append(new_directory)

database_url = 'sqlite:///db_trade.db'
engine = create_engine(database_url)


