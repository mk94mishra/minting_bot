import asyncio
from router import *
from datetime import datetime, timedelta
import time

import gc


total_call = 1000

# Define the data to be sent in the request
data = {
    "url": "/api/v3/time",
    "method": "GET"
}


# test normal call in a time
def timeout_call_one_by_one(seconds):
    end_time = datetime.now() + timedelta(minutes=(seconds//60))
    total_results = 0
    while datetime.now() < end_time:
        current_time = datetime.now()
        time_difference = end_time - current_time
        results = call_all_proxy_one_by_one(5, data)
        total_results = total_results + len(results)
        print(f"Total results one by one: {total_results} in {seconds}")
        with open('testresults.txt', 'a') as file:
            file.write(f"Total results one by one: {total_results} in {seconds}\n")
            file.close()


# test concurrent call in a time
async def timeout_call_concurrent(seconds):
    try:
        results = await asyncio.wait_for(call_all_proxy_one_by_one(total_call, data), timeout=seconds)  # 300 seconds = 5 minutes
        # Process results if the call is successful within the timeout
        if results is not None:
            total_results = len(results)
            print(f"Total results concurrent: {total_results} in {seconds}")
            with open('testresults.txt', 'a') as file:
                file.write(f"Total results one by one: {total_results} in {seconds}")
                file.close()
        else:
            print("No results due to timeout.")
    except asyncio.TimeoutError:
        # Handle timeout (function call took more than 5 minutes)
        print("Function call timed out after 5 minutes")
        return None


# with open('testresults.txt', 'a') as file:
#     file.write(f"test initated \n")
#     file.close()

# # test call in 1 minutes
# timeout_call_one_by_one(60)
# asyncio.run(timeout_call_concurrent(60))
# # test call in 5 minutes
# timeout_call_one_by_one(300)
# asyncio.run(timeout_call_concurrent(300))

# test 10,000 calls
# start_time = datetime.now()
# results = call_all_proxy_one_by_one(total_call,data)
# print(f"one by one call start time{start_time} and end time{datetime.now()} in {total_call} call")
# with open('testresults.txt', 'a') as file:
#     file.write(f"one by one call start time{start_time} and end time{datetime.now()} in {total_call} call\n")
#     file.close()

# test concurrent 10,000 calls
start_time = datetime.now()
limit_call = 100
total_call_with_limit = total_call//limit_call
all_results = []
for _ in range(total_call_with_limit):
    results = asyncio.run(call_all_proxy_concurrent(limit_call,data))
    all_results.append(results)
    
with open('testresults.txt', 'a') as file:
    file.write(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call\n")
    file.write(f'{all_results}')
    file.close()

print(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call")
gc.collect()

