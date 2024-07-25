import requests
import json

def query_ollama(prompt, model_name, temperature=0):
    url = "http://140.119.164.212:11434/api/generate"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": temperature,
        "guided_json": "TEST_SCHEMA"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    if response.headers.get('Content-Type') == 'application/x-ndjson':
        ndjson_content = response.text.strip().split('\n')
        json_responses = [json.loads(line) for line in ndjson_content]
        complete_response = ''.join([item['response'] for item in json_responses if 'response' in item])
        return complete_response

    elif response.headers.get('Content-Type') == 'application/json':
        return response.json()

    else:
        raise Exception(f"Unexpected content type: {response.headers.get('Content-Type')}")

model_names = ["codestral:22b", "codegemma:7b", "codellama:13b", "llama3.1:8b", "gemma2:9b", "llama3:8b"]
prompt = "Translate English to French: 'Hello, how are you?'"
response = query_ollama(prompt, model_names[3])
print(response)
