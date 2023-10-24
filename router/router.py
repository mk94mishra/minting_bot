# Import the necessary libraries
import asyncio
from aiohttp import ClientSession
import datetime
import config


# Define the data to be sent in the request
data = {
    "url": "/api/v3/exchangeInfo",
    "method": "GET"
}
proxy_details_list = config.proxy_details
proxy_details_dict = {}
# Function to select a proxy from the database
def select_proxy():
    """Selects a proxy from the database based on its expiration time and weightage.

    Returns:
        The URL of the selected proxy, or None if no suitable proxy is found.
    """
    for data in proxy_details_list:
        if (int(datetime.datetime.now().timestamp() * 1000) - int(data[3])) > config.custom['proxy_max_time'] or int(data[2]) < config.custom['proxy_max_weightage']:
            return data[4]

    return None

def update_proxy(response_proxy_details): 

    for response_data in response_proxy_details:
        url = response_data[0]
        name =  response_data[4]
        weigtage = response_data[1]
        weightage_one_minute = response_data[2]
        event_time = response_data[3]
        
        for item in proxy_details_list:
            if item[0] == url and item[4] == name:
                item[1] = weigtage
                item[2] = weightage_one_minute
                item[3] = event_time
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
        update_proxy(json_response['proxy_details'])
        with open('output.txt', 'a') as file:
            file.write(f'| {i}--{response.status}--{time.time()}\n')
            file.close()
        # header_response=response.headers
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
    
total_call = 100000
# Run the asyncio event loop and print the results
async def call_all_proxy(data):
    start_range = 0
    diff_range = total_call//len(config.proxy)
    end_range = diff_range
    results_one = await concurrent_call(start_range,diff_range,data)

    start_range = end_range
    end_range = end_range+diff_range
    results_two = await concurrent_call(start_range+1,(end_range),data)
    
    start_range = end_range
    end_range = end_range+diff_range
    results_three = await concurrent_call((start_range)+1,(end_range),data)

    start_range = end_range
    end_range = end_range+end_range
    results_four = await concurrent_call((start_range)+1,(end_range),data)

    start_range = end_range
    results_five = await concurrent_call((start_range)+1,(total_call),data)

    results = [results_one,results_two,results_three,results_four,results_five]
    return results

result = asyncio.run(call_all_proxy(data))