from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import *

# Create a session
with Session(engine) as session:
    # Insert dummy data into the Users table
    dummy_users = [
        Users(name='Alice', email='alice@example.com', is_active=True),
        Users(name='Bob', email='bob@example.com', is_active=False),
        Users(name='Charlie', email='charlie@example.com', is_active=True),
    ]

    # Add the dummy users to the session
    session.add_all(dummy_users)
    
    # Commit the changes to the database
    session.commit()

# Now, the Users table should have the dummy data inserted.
