from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


from proxy.models import *
from db import *


def proxy_log(trade_data):
    # Create a session
    with Session(engine) as session:
        session.add(ProxyLog(**trade_data))
        # Commit th changes to the database
        session.commit()


