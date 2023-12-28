from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from urllib.parse import urlparse, parse_qs
from models import *
from db import engine


def proxy_log(trade_data):
    url = trade_data['request']['data']['url']
    try:
        order_id = trade_data['response']['data']['order_id']
    except Exception as e:
        order_id = None
    print(url)
    # Parse the URL
    parsed_url = urlparse(url)
    # Get the query parameters
    query_params = parse_qs(parsed_url.query)
    # Fetch the value of newClientOrderId
    new_client_order_id = query_params.get('newClientOrderId', [None])[0]
    new_client_order_id_list = new_client_order_id.split("-")
    trade_id = new_client_order_id_list[3]
    user_id = new_client_order_id_list[2]
    trade_type = new_client_order_id_list[1]
    trade_data = {
        'client_order_id' : new_client_order_id,
        'user_id':user_id,
        'trade_id' : trade_id,
        'trade_type' : trade_type,
        'order_id' : order_id,
        'request' : trade_data['request'],
        'response' : trade_data['response']
    }
    print(trade_data)
    # Create a session
    with Session(engine) as session:
        session.add(ProxyLog(**trade_data))
        # Commit th changes to the database
        session.commit()
        if trade_type == 'S' and order_id:
            update_query = text("UPDATE user_trades SET is_open=false WHERE user_id=:user_id and trade_id=:trade_id")
            params = {'user_id': user_id, 'trade_id':trade_id}
            session.execute(update_query, params)
            session.commit()
        session.close()


    
def proxy_log_sl(trade_data):
    url = trade_data['request']['data']['url']
    response = trade_data['response']['data']
    if 'code' not in response.keys():
        # Parse the URL
        parsed_url = urlparse(url)
        # Get the query parameters
        query_params = parse_qs(parsed_url.query)
        # Fetch the value of newClientOrderId
        order_id = query_params.get('order_id', [None])[0]
        with Session(engine) as session:
            result = session.execute(text("SELECT * FROM proxy_log WHERE order_id = :order_id "), {"order_id": order_id})
            trade_data = result.fetchall()

            update_query = text("UPDATE user_trades SET is_open=false WHERE user_id=:user_id and trade_id=:trade_id")
            params = {'user_id': trade_data[0].user_id, 'trade_id':trade_data[0].trade_id}
            session.execute(update_query, params)
            session.commit()
            session.close()
