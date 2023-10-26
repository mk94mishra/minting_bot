# Import the necessary libraries
import asyncio
from aiohttp import ClientSession
import config
import requests

proxy_url_list = list(config.proxy_url.values())
def select_proxy(proxy_no):
    active_url = proxy_url_list[proxy_no]
    return active_url

i=0
import time
# Function to make an API call using the specified proxy
async def make_api_call_concurrent(session, data, proxy_no):
    """Makes an API call using the specified proxy.

    Args:
        session: An aiohttp.ClientSession object.
        data: A dictionary containing the request data.

    Returns:
        The JSON response from the API, or None if the request failed.
    """

    url = select_proxy(proxy_no)
    url = f"{url}/call_api"
    global i  
    async with session.post(url, json=data) as response:
        json_response = await response.json()
        i=i+1
        with open('output.txt', 'a') as file:
            file.write(f'| {i}--{response.status}--{time.time()}\n')
            file.close()
        return json_response


# Function to make an API call using the specified proxy
def make_api_call(data,proxy_no):
    """Makes an API call using the specified proxy.

    Args:
        session: An aiohttp.ClientSession object.
        data: A dictionary containing the request data.

    Returns:
        The JSON response from the API, or None if the request failed.
    """

    url = select_proxy(proxy_no)
    if url is None:
        return "proxy end"
    
    url = f"{url}/call_api"
        
    response = requests.post(url, json=data)
    with open('output.txt', 'a') as file:
        file.write(f'| {i}--{response.status_code}--{time.time()}\n')
        file.close()
    json_response = response.json()
    return json_response


# Function to make concurrent API calls
async def concurrent_call(start_range,end_range,data,proxy_no):
    """Makes concurrent API calls using the specified number of requests.

    Returns:
        A list of JSON responses from the API, or None if all requests failed.
    """
    async with ClientSession() as session:
        tasks = [make_api_call_concurrent(session, data, proxy_no) for i in range(start_range,end_range)]
        return await asyncio.gather(*tasks)
    
    
# Run the asyncio event loop and print the results
async def call_all_proxy_concurrent(total_call,data):
    all_results = []
    if total_call > 20:
        if total_call > config.proxy_call_limit:
            total_call = config.proxy_call_limit
            
        diff_call = total_call//len(config.proxy)

        tasks = [asyncio.create_task(concurrent_call(proxy_no * diff_call,(proxy_no * diff_call) + diff_call,data,proxy_no)) for proxy_no in range(0,len(config.proxy))]
        results = await asyncio.gather(*tasks)
        all_results.append(results)
    else:
        results = await concurrent_call(0,total_call,data,0)
        all_results.append(results)
    return all_results

# result = asyncio.run(call_all_proxy_concurrent(total_call,data))
# print(result)

def call_all_proxy_one_by_one(total_call,data):
    
    all_results = []
    if total_call > 20:
        if total_call > config.proxy_call_limit:
            total_call = config.proxy_call_limit

        diff_call = total_call//len(config.proxy)
        start_range = 0
        end_range = diff_call
        for proxy_no in range(0,len(config.proxy)):
            for _ in range(start_range,end_range):
                results = make_api_call(data,proxy_no)
                all_results.append(results)
            start_range = end_range
            end_range = end_range + diff_call
    else:
        for _ in range(0,total_call):
            results = make_api_call(data,0)
            all_results.append(results)
    
    return all_results

# results = call_all_proxy_one_by_one(total_call,data)
# print(results)