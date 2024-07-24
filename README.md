# LLM Serve

## Overview

This project provides Python scripts to interact with APIs from Ollama and vLLM. The script `ollama_app.py` allows you to call models such as `llama3:8b`, `gemma2:9b`, and `phi-3` from the Ollama API. The vLLM models can be hosted and accessed through Docker.

For **Ollama** and **vLLM** supports, see `ollama_app.py` and `vllm_app.py` respectively.
## Ollama API Integration

The `ollama_app.py` script allows you to generate text completions using different models provided by the Ollama API.

### Supported Models

- `llama3:8b`
- `gemma2:9b`
- `phi3-mini`
- `llama3.1:8b`

### Prerequisites

- Python 3.6+
- `requests` library

You can install the required library using pip:

```sh
pip install requests
```

### Usage

1. **Edit the Script**: Ensure that the `model_names` list contains the correct models you want to use.

2. **Run the Script**:

```python
import requests
import json

def query_ollama(prompt, model_name, temperature=0):
    url = "http://140.119.164.212:11434/api/generate"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": temperature,
        "guided_json": "TEST_SCHEMA"  # Ensure TEST_SCHEMA is a string variable
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

model_names = ["llama3:8b", "gemma2:9b", "mannix/phi3-mini-4k:latest", "llama3.1:8b"]
prompt = "Translate English to French: 'Hello, how are you?'"
response = query_ollama(prompt, model_names[2])
print(response)
```

3. **Execute the Script**:

```sh
python ollama_app.py
```

## vLLM API Integration

### Prerequisites

- Docker
- NVIDIA Docker Runtime (for GPU support)
- Hugging Face API token

### Setting Up vLLM

1. **Pull the vLLM Docker Image**:

```sh
docker pull vllm/vllm-openai:latest
```

2. **Run the Docker Container**:

Ensure you have your Hugging Face API token. Replace `YOUR_HUGGING_FACE_HUB_TOKEN` with your actual token.

```sh
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -v /path/to/your/model_dir:/root/model_config \
    --env "HUGGING_FACE_HUB_TOKEN=YOUR_HUGGING_FACE_HUB_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model /root/model_config
```

### Accessing the vLLM API

You can interact with the vLLM API using HTTP requests. Below is an example Python script for querying the vLLM API:

```python
import requests

def query_vllm(prompt, model_name, max_tokens=50):
    url = "http://localhost:8000/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_HUGGING_FACE_HUB_TOKEN"
    }
    payload = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

prompt = "Once upon a time"
model_name = "mannix/phi3-mini-4k:latestt"
response = query_vllm(prompt, model_name)
print(response)
```

## Conclusion

This project provides a straightforward way to interact with text generation models from Ollama and vLLM. Ensure you have the required dependencies installed and configured correctly to use the provided scripts effectively.

For any issues or contributions, feel free to open an issue or a pull request on the project's repository.
