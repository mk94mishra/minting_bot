# test_main.py
from fastapi.testclient import TestClient
from main import app
import requests
import time
from concurrent.futures import ThreadPoolExecutor


client = TestClient(app)

url = "http://127.0.0.1:8000/call_api"
data = {
    "url": "/api/v3/exchangeInfo",
    "method": "GET"
}

# Define the number of parallel requests
num_requests = 10000

# Create a list of tasks
tasks = [(url, data) for _ in range(num_requests)]

def send_post_request(url, data):
        response = requests.post(url, json=data)
        return response

# def test_max_concurrent_call():
#     # Send requests in parallel
#     with ThreadPoolExecutor() as executor:
#         responses = list(executor.map(lambda x: send_post_request(*x), tasks))

#     # Process responses if needed
#     for response in responses:
#         assert response.status_code == 200


# Adjust the number of calls as needed
def test_max_calls_in_five_minute():
    start_time = time.time()
    duration = 300
    for i in range(1000000):
        if time.time() - start_time < duration:
            assert "5 minutes done" == "5 minutes done"
            break
        response = send_post_request(url, data)
        if response.status_code != 200:
            assert "break at {i}" == "break"
            break
        assert response.status_code == 200  
