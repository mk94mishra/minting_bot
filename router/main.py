# Import the necessary libraries
from fastapi import FastAPI, HTTPException, HTTPException,Request
from typing import Optional, Dict, Any
from pydantic import BaseModel
import asyncio
from router import *
from datetime import datetime
import gc


# Create a FastAPI app
app = FastAPI()

# Define the CallApi model
class CallApi(BaseModel):
    data: Optional[list] = None

def arrange_data(start_time,total_call,method,data):
    limit_call = 50
    total_call_with_limit = total_call//limit_call
    all_results = []
    # print(start_time,total_call,url,method,headers)
    for i in range(total_call_with_limit):
        results = asyncio.run(call_all_proxy_concurrent(limit_call,data=data))
        all_results.append(results)
        
    with open('testresults.txt', 'a') as file:
        file.write(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call\n")
        file.write(f'{all_results}')
        file.close()

    print(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call")
    gc.collect()
    return all_results


# Define the call_api_route endpoint
@app.post("/router")
async def call_api_route(request:Request,payloads: CallApi):
    payloads = payloads.dict()
    total_call = len(payloads['data'])
    response = await call_all_proxy_concurrent(total_call,data=payloads['data'])
    print(response)
    return response
