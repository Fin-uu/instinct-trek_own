import sys
import subprocess

# Ensure dependencies are installed
try:
    import openai
    import requests
except ImportError:
    print("Installing required packages: requests, openai...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "openai"])
    import openai
    import requests

from openai import OpenAI

# Configuration from the markdown file
vllm_gpt_oss_120b_1 = "http://210.61.209.139:45014/v1/"
vllm_gpt_oss_120b_2 = "http://210.61.209.139:45005/v1/"

# Select the first endpoint
base_url = vllm_gpt_oss_120b_1

print(f"Connecting to API at: {base_url}")

# Initialize OpenAI Client
client = OpenAI(
    base_url=base_url,
    api_key="dummy-key"
)

# Determine model name
try:
    print("Fetching available models...")
    models = client.models.list()
    if models.data:
        model_name = models.data[0].id
        print(f"Successfully found model: {model_name}")
    else:
        model_name = "gpt-oss-120b"
        print(f"No models found in list, using default: {model_name}")
except Exception as e:
    print(f"Warning: Could not fetch model list ({e}). Using default model name.")
    model_name = "gpt-oss-120b"

print("-" * 50)

# 1. Text Generation Example
print("1. Running Text Generation Example...")
message = "Once upon a time in a magical forest,"
try:
    response = client.completions.create(
        model=model_name,
        prompt=message,
        max_tokens=100,
        temperature=0.8
    )
    generated_text = response.choices[0].text
    print("Prompt:", message)
    print("Generated text:", generated_text)
except Exception as e:
    print(f"Error in Text Generation: {e}")

print("-" * 50)

# 2. Chat Completion Example
print("2. Running Chat Completion Example...")
try:
    chat_response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain machine learning in one paragraph."}
        ],
        temperature=0.7
    )
    response_content = chat_response.choices[0].message.content
    print("Chat response:", response_content)
except Exception as e:
    print(f"Error in Chat Completion: {e}")

print("-" * 50)

# 3. Reasoning Effort Example
print("3. Running Reasoning Effort Example...")
try:
    reasoning_response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert problem solver. Think step by step and show your reasoning process."},
            {"role": "user", "content": """
            Solve this logic puzzle step by step:
            
            Three friends - Alice, Bob, and Carol - each have a different pet (cat, dog, bird) and live in different colored houses (red, blue, green).
            
            Clues:
            1. Alice doesn't live in the red house
            2. The person with the cat lives in the blue house
            3. Bob doesn't have a bird
            4. Carol doesn't live in the green house
            5. The person in the red house has a dog
            
            Who has which pet and lives in which house?
            """}
        ],
        temperature=0.1,
        max_tokens=500
    )
    reasoning_content = reasoning_response.choices[0].message.content
    print("Reasoning Response:", reasoning_content)
except Exception as e:
    print(f"Error in Reasoning Example: {e}")

print("-" * 50)
print("Done.")
