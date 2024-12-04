import requests
import time

# Define server URL
server_url = "http://localhost:8000/generate"

# Define request payload
payload = {
<<<<<<< HEAD
    "prompt": "Explain the basic principles of quantum mechanics.",
    "max_length": 500,
=======
    "prompt": "What is 1 plus 1?",
    "max_length": 200,
>>>>>>> 4f9629a (more correction)
    "do_sample": True,
    "num_return_sequences": 1,
    "truncation": True
}

# Measure latency for a single request
start_time = time.time()
response = requests.post(server_url, json=payload)
end_time = time.time()

# Calculate latency
latency = end_time - start_time

# Print the response
if response.status_code == 200:
    print("Generated Text:", response.json()["responses"])
else:
    print("Error:", response.status_code, response.text)
    print(f"Latency: {latency:.6f} seconds")

# Measure throughput (requests per second)
num_requests = 10  # Number of requests to send for throughput test
throughput_start_time = time.time()

for _ in range(num_requests):
    response = requests.post(server_url, json=payload)

throughput_end_time = time.time()

# Calculate throughput
total_time = throughput_end_time - throughput_start_time
throughput = num_requests / total_time

print(f"Throughput: {throughput:.2f} requests/second over {num_requests} requests")
