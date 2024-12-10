import requests

# Define server URL
server_url = "http://localhost:8000/generate"

# Define request payload
payload = {
    "prompt": "Explain the basic principles of quantum mechanics."
}

# Send POST request
response = requests.post(server_url, json=payload)

# Print the response
if response.status_code == 200:
    generated_text = response.json().get("response")
    if generated_text:
        print(generated_text)
    else:
        print("No response generated.")
else:
    print("Error:", response.status_code, response.text)
