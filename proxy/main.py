# Import the necessary libraries
from fastapi import FastAPI, HTTPException, HTTPException
from typing import Optional, Dict, Any
from pydantic import BaseModel
import json
import common
from proxy_log import *

# Create a FastAPI app
app = FastAPI()

# Define the CallApi model
class CallApi(BaseModel):
    # The URL of the API to call
    url: str
    # The HTTP method to use
    method: Optional[str] = None
    # Optional headers to send with the request
    headers: Optional[Dict[str, str]] = None
    # Optional data to send with the request
    data: Optional[Dict[str, Any]] = None

# Define the call_api_route endpoint
@app.post("/call_api")
async def call_api_route(payloads: CallApi):
    # Get the request payload as a dictionary
    payload = payloads.dict()
    
    # Call the common.call_api() function to call the API
    response = await common.call_api(payload['url'], payload['method'], headers=payload['headers'], data=payload['data'])

    try:
        proxy_data = {
            'request':{'data':payload},
            'response': {'data':response['data']}
        }
        proxy_log(proxy_data)
    except Exception as e:
        print(e)
    # Check if the proxy has expired
    if 'Proxy expired' in response:
        # Raise a 422 Unprocessable Entity exception
        raise HTTPException(status_code=422, detail='Proxy expired')

    # Check if there was an error calling the API
    if response is None:
        # Raise a 500 Internal Server Error exception
        raise HTTPException(status_code=500, detail="Error calling API")
    return response

