import requests

# Define server URL
server_url = "http://localhost:8000/generate"

# Define request payload
payload = {
    "prompt": "Explain the basic principles of quantum mechanics.",
    "max_length": 200,
    "do_sample": True,
    "num_return_sequences": 1
}

# Send POST request
response = requests.post(server_url, json=payload)

# Print the response
if response.status_code == 200:
    print("Generated Text:", response.json()["responses"])
else:
    print("Error:", response.status_code, response.text)
