import requests

# Define the API endpoint for completions
completions_url = "http://140.119.164.212:8000/v1/completions"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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"
}

# Define the payload
payload = {
    "model": "gpt2",
    "prompt": "Once upon a time",
    "max_tokens": 50
}

try:
    # Send the POST request
    response = requests.post(completions_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    response_json = response.json()

    # Extract the generated text
    generated_text = response_json['choices'][0]['text']
    print(generated_text)

except requests.exceptions.RequestException as e:
    print(f"Failed to get a response: {e}")

