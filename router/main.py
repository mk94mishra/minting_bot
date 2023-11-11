# Import the necessary libraries
from fastapi import FastAPI, HTTPException, HTTPException
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
    # The URL of the API to call
    url: str
    # The HTTP method to use
    method: str
    # Optional headers to send with the request
    headers: Optional[Dict[str, str]] = None
    # Optional data to send with the request
    data: Optional[Dict[str, Any]] = None

# Define the call_api_route endpoint
@app.post("/router")
async def call_api_route(payloads: CallApi):
    # Get the request payload as a dictionary
    payload = payloads.dict()

    start_time = datetime.now()
    limit_call = 50
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
