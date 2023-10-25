import asyncio
from datetime import datetime
from router import *



total_call = 10000

# Define the data to be sent in the request
data = {
    "url": "/api/v3/exchangeInfo",
    "method": "GET"
}


# test normal call in a time
async def timeout_call_one_by_one(seconds):
    try:
        results = await asyncio.wait_for(call_all_proxy_one_by_one(total_call, data), timeout=seconds)  # 300 seconds = 5 minutes
        # Process results if the call is successful within the timeout
        if results is not None:
            total_results = len(results)
            print(f"Total results one by one: {total_results} in {seconds}")
        else:
            print("No results due to timeout.")
    except asyncio.TimeoutError:
        # Handle timeout (function call took more than 5 minutes)
        print("Function call timed out after 5 minutes")
        return None

# test concurrent call in a time
async def timeout_call_concurrent(seconds):
    try:
        results = await asyncio.wait_for(call_all_proxy_one_by_one(total_call, data), timeout=seconds)  # 300 seconds = 5 minutes
        # Process results if the call is successful within the timeout
        if results is not None:
            total_results = len(results)
            print(f"Total results concurrent: {total_results} in {seconds}")
        else:
            print("No results due to timeout.")
    except asyncio.TimeoutError:
        # Handle timeout (function call took more than 5 minutes)
        print("Function call timed out after 5 minutes")
        return None


# test call in 5 minutes
asyncio.run(timeout_call_one_by_one(300))
asyncio.run(timeout_call_concurrent(300))

# test call in 1 minutes
asyncio.run(timeout_call_one_by_one(60))
asyncio.run(timeout_call_concurrent(60))


# test 10,000 calls
start_time = datetime.now()
results = call_all_proxy_one_by_one(total_call,data)
print(f"one by one call start time{start_time} and end time{datetime.now()} in {total_call} call")
with open('testresults.txt', 'a') as file:
    file.write(f"one by one call start time{start_time} and end time{datetime.now()} in {total_call} call\n")
    file.close()

# test concurrent 10,000 calls
start_time = datetime.now()
results = asyncio.run(call_all_proxy_concurrent(total_call,data))
print(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call")
with open('testresults.txt', 'a') as file:
    file.write(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call")
    file.close()


