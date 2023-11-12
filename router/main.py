# Import the necessary libraries
from fastapi import FastAPI, HTTPException, HTTPException,Request,Body
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
    # Optional data to send with the request
    order: Optional[Dict[str, Any]] = None

def arrange_data(start_time,total_call,url,method,headers,data):
    limit_call = 50
    total_call_with_limit = total_call//limit_call
    all_results = []
    print(start_time,total_call,url,method,headers)
    for i in range(total_call_with_limit):
        results = asyncio.run(call_all_proxy_concurrent(limit_call,data={'url':url,'method':method,'headers':headers[i],'data':data[i]}))
        all_results.append(results)
        
    with open('testresults.txt', 'a') as file:
        file.write(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call\n")
        file.write(f'{all_results}')
        file.close()

    print(f"concurrent call start time{start_time} and end time{datetime.now()} in {total_call} call")
    gc.collect()
    return all_results


# Define the call_api_route endpoint
@app.get("/router")
async def call_api_route(request:Request ):
    url = str(request.url)
    url = url.split('/')
    url = "/".join(url[7:])
    print(url)
    # start_time=datetime.datetime.now()
    # arrange_data(start_time,10  ,'bin_api','POST',request.headers,None)


@app.post("/router")
async def call_api_route(request:Request ):
    start_time = datetime.now()
    print(request.url)
    url = request.url
    # url = url.decode('ascii')
    url = url.split('/')
    print(url[6:])
    # print(await request.body())
    raw_data = await request.body()
    print(raw_data)
