# Import the necessary libraries
import asyncio
from aiohttp import ClientSession
import sqlite3
import datetime
import config


# Define the data to be sent in the request
data = {
    "url": "/api/v3/exchangeInfo",
    "method": "GET"
}

# Function to select a proxy from the database
def select_proxy():
    """Selects a proxy from the database based on its expiration time and weightage.

    Returns:
        The URL of the selected proxy, or None if no suitable proxy is found.
    """

    conn = sqlite3.connect(config.database['db'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_proxy")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    for data in results:
        if (int(datetime.datetime.now().timestamp() * 1000) - int(data[4])) > config.custom['proxy_max_time'] or int(data[2]) < config.custom['proxy_max_weightage']:
            return data[5]

    return None
i=0
import time
# Function to make an API call using the specified proxy
async def make_api_call(session, data):
    """Makes an API call using the specified proxy.

    Args:
        session: An aiohttp.ClientSession object.
        data: A dictionary containing the request data.

    Returns:
        The JSON response from the API, or None if the request failed.
    """

    url = select_proxy()
    if url is None:
        return "proxy end"

    url = config.proxy_url[url]
    url = f"{url}/call_api"
    global i  
    
    async with session.post(url, json=data) as response:
        json_response = await response.json()
        i=i+1
        with open('output.txt', 'a') as file:
            file.write(f'| {i}--{response.status}--{time.time()}\n')
            file.close()
        return json_response

# Function to make concurrent API calls
async def concurrent_call(start_range,end_range,data):
    """Makes concurrent API calls using the specified number of requests.

    Returns:
        A list of JSON responses from the API, or None if all requests failed.
    """
    async with ClientSession() as session:
        tasks = [make_api_call(session, data) for i in range(start_range,end_range+1)]
        return await asyncio.gather(*tasks)
    
total_call = 10000
# Run the asyncio event loop and print the results

async def call_all_proxy(data):
    start_range = 0
    end_range = total_call//len(config.proxy)
    results_one = await concurrent_call(start_range,end_range,data)
    results_two = await concurrent_call(end_range+1,(end_range*2),data)
    last_call_reminder = total_call%len(config.proxy)
    results_three = await concurrent_call((end_range*3)+1,(end_range*4)+last_call_reminder,data)
    results = await [results_one,results_two,results_three]
    return results

result = asyncio.run(call_all_proxy())