import requests

# Define server URL
server_url = "http://localhost:8000/generate"

# Define request payload
payload = {
    "prompt": "Explain the basic principles of quantum mechanics.",
    "max_length": 500,
    "do_sample": True,
    "num_return_sequences": 1,
    "truncation": True
}

# Send POST request
response = requests.post(server_url, json=payload)

# Print the response
if response.status_code == 200:
    # Fetch the 'responses' from the JSON
    generated_text = response.json().get("responses")
    # Check if 'responses' is not empty and print
    if generated_text:
        print(generated_text[0])  # Directly print the generated text without any additional formatting
    else:
        print("No text generated.")
else:
    print("Error:", response.status_code, response.text)
