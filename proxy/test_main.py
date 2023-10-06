# test_main.py
from fastapi.testclient import TestClient
from main import app
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import logging


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
i=0
def send_post_request(url, data):
    global i
    i=i+1
    response = requests.post(url, json=data)
    with open('concurrent-output.txt', 'a') as file:
        file.write(f'| {i} | {response.status_code} | {time.time()}\n')
        file.close()
    return response


# Adjust the number of calls as needed
def test_max_calls_in_five_minute():
    start_time = time.time()
    duration = 300
    error_response =[]
    i=0
    while time.time() - start_time < duration:
        i=i+1
        response = send_post_request(url, data)
        with open('output.txt', 'a') as file:
            file.write(f'| {i}--{response.status_code}--{time.time()}\n')
            file.close()
        if response.status_code != 200:
             error_response.append(response.status_code)
        assert  len(error_response) == 0


def test_max_concurrent_call():
    # Send requests in parallel
    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(lambda x: send_post_request(*x), tasks))

    # Process responses if needed
    for response in responses:
        assert response.status_code == 200