# Import the necessary libraries
import aiohttp
import sqlite3
import datetime
import config as config

# Connect to the SQLite database
conn = sqlite3.connect(config.database['db'])
cursor = conn.cursor()

# Get the current base URL for the proxy
def current_base_url():
    # Execute a SQL query to select the proxy with the specified name
    cursor.execute(f"SELECT * FROM tbl_proxy where proxy_name='{config.database['proxy_name']}'")

    # Get the results of the query
    results = cursor.fetchall()

    # Iterate over the results and check if the proxy is expired or has low weightage
    for data in results:
        if (int(datetime.datetime.now().timestamp() * 1000) - int(data[4])) > config.custom['bin_max_time'] or int(data[2]) < config.custom['bin_max_weightage']:
            # If the proxy is expired or has low weightage, return the proxy's base URL
            current_base_url = data[1]
            return current_base_url

    # If no suitable proxy is found, return None
    return None

# Update the weightage of a proxy
def update_weightage(response, base_url):
    # Execute a SQL query to update the weightage of the proxy
    cursor.execute(f"UPDATE tbl_proxy set weightage = '{response['x-mbx-used-weight']}', weightage_minute = '{response['x-mbx-used-weight-1m']}', event_time='{int(datetime.datetime.now().timestamp() * 1000)}' where proxy_url='{base_url}' and proxy_name='{config.database['proxy_name']}'")

    # Commit the changes to the database
    conn.commit()

    # Return True to indicate that the update was successful
    return True

# Get all proxy details
def get_proxy_details():
    # Execute a SQL query to select all proxies with the specified name
    cursor.execute(f"SELECT * FROM tbl_proxy where proxy_name='{config.database['proxy_name']}'")

    # Get the results of the query
    return cursor.fetchall()

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

        # Update the weightage of the proxy
        update_weightage(response_header, base_url)

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

