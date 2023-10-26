# Import the necessary libraries
import aiohttp
import datetime
import config as config
import requests


proxy_expire_details = []
i=0
for bin_url in config.bin_api_list:
    #[apiurl, weightage,weightage_minut,event_time,proxy_name]
    proxy_expire_details.append([bin_url,0,0,0,config.proxy_name,0])
    i=i+1

# Get the current base URL for the proxy
failed_urls = []
def current_base_url():
    # Iterate over the results and check if the proxy is expired or has low weightage

    for data in proxy_expire_details:
        if (int(datetime.datetime.now().timestamp() * 1000) - int(data[3])) > config.custom['bin_max_time'] or int(data[1]) < config.custom['bin_max_weightage'] and data[5] == 0:
            # If the proxy is expired or has low weightage, return the proxy's base URL
            current_base_url = data[0]
            return current_base_url

    # If no suitable proxy is found, return None
    return None

# Update the weightage of a proxy
def update_weightage(response, base_url):
    if response is not None:
        #[apiurl, weightage,weightage_minut,event_time,proxy_name,deactive]
        # [bin_url,0,0,0,config.proxy_name,0] 
        filtered_list = [sub_list for sub_list in proxy_expire_details if base_url in sub_list]
        filtered_list[0][1]=response['x-mbx-used-weight']
        filtered_list[0][2]=response['x-mbx-used-weight-1m']
        filtered_list[0][3]=int(datetime.datetime.now().timestamp() * 1000)
    else:
        # [bin_url,0,0,0,config.proxy_name,0] 
        filtered_list = [sub_list for sub_list in proxy_expire_details if base_url in sub_list]
        filtered_list[0][1]=0
        filtered_list[0][2]=0
        filtered_list[0][3]=int(datetime.datetime.now().timestamp() * 1000)
        filtered_list[0][5]=1
        # Return True to indicate that the update was successful
    return True

# Get all proxy details
def get_proxy_details():
    # Get the results of the query
    return proxy_expire_details

# Call an API using a proxy
def call_api(url, method, headers=None, data=None):

    for _ in range(2):
        # Get the current base URL for the proxy
        base_url = current_base_url()

        # If no suitable proxy is found, return an error message
        if base_url is None:
            return "Proxy expired", get_proxy_details()

        # Construct the full URL for the API call
        api_url = f"{base_url}{url}"
        response_json = []
        response_header = []
        
        try:
            if method == 'GET':
                response = requests.get(api_url, headers=headers)
                response_json = response.json()
                response_header = response.headers
            elif method == 'POST':
                response = requests.post(api_url, headers=headers, json=data)
                response_json = response.json()
                response_header = response.headers
            elif method == 'PUT':
                response = requests.put(api_url, headers=headers, json=data)
                response_json = response.json()
                response_header = response.headers
            elif method == 'DELETE':
                response = requests.delete(api_url, headers=headers, json=data)
                response_json = response.json()
                response_header = response.headers
            else:
                raise ValueError(f'Unsupported HTTP method: {method}')

            # Update the weightage of the proxy
            update_weightage(response_header, base_url)
            break
        except Exception as e:
            print(e)
            update_weightage(None, base_url)
            
    
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

