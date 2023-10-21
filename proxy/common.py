# Import the necessary libraries
import aiohttp
import datetime
import config as config


proxy_expire_details = []
i=0
for bin_url in config.bin_api_list:
    #[apiurl, weightage,weightage_minut,event_time,proxy_name]
    proxy_expire_details.append([bin_url,0,0,0,config.proxy_name])
    i=i+1

# Get the current base URL for the proxy
def current_base_url():
    # Iterate over the results and check if the proxy is expired or has low weightage
    for data in proxy_expire_details:
        if (int(datetime.datetime.now().timestamp() * 1000) - int(data[3])) > config.custom['bin_max_time'] or int(data[1]) < config.custom['bin_max_weightage']:
            # If the proxy is expired or has low weightage, return the proxy's base URL
            current_base_url = data[0]
            return current_base_url

    # If no suitable proxy is found, return None
    return None

# Update the weightage of a proxy
def update_weightage(response, base_url):
    #[apiurl, weightage,weightage_minut,event_time,proxy_name]
    [bin_url,0,0,0,config.proxy_name] 
    filtered_list = [sub_list for sub_list in proxy_expire_details if base_url in sub_list]
    filtered_list[0][1]=response['x-mbx-used-weight']
    filtered_list[0][2]=response['x-mbx-used-weight-1m']
    filtered_list[0][3]=int(datetime.datetime.now().timestamp() * 1000)
    # Return True to indicate that the update was successful
    return True

# Get all proxy details
def get_proxy_details():
    # Get the results of the query
    return proxy_expire_details

# Call an API using a proxy
async def call_api(url, method, headers=None, data=None):
    # Get the current base URL for the proxy
    base_url = current_base_url()

    # If no suitable proxy is found, return an error message
    if base_url is None:
        return "Proxy expired", get_proxy_details()

    # Construct the full URL for the API call
    url = f"{base_url}{url}"

    # Create an async HTTP client session
    async with aiohttp.ClientSession() as session:
        # Make the API call using the specified HTTP method
        if method == 'GET':
            async with session.get(url, headers=headers) as response:
                response_json = await response.json()
                response_header = response.headers
        elif method == 'POST':
            async with session.post(url, headers=headers, json=data) as response:
                response_json = await response.json()
                response_header = response.headers
        elif method == 'PUT':
            async with session.put(url, headers=headers, json=data) as response:
                response_json = await response.json()
                response_header = response.headers
        elif method == 'DELETE':
            async with session.delete(url, headers=headers, json=data) as response:
                response_json = await response.json()
                response_header = response.headers
        else:
            raise ValueError(f'Unsupported HTTP method: {method}')

        try:
            # Update the weightage of the proxy
            update_weightage(response_header, base_url)
        except Exception:
            print(response_header)

        # Get the proxy details
        proxy_details = get_proxy_details()

        # Construct the final response
        final_response = {
            'data': response_json,
            'headers': response_header,
            'proxy_details': proxy_details
        }

        # Return the final response
        return final_response

