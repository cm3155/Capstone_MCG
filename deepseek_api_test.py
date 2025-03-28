#This is just checking the API key, actual cleaner is under text processing scripts
from openai import OpenAI

client = OpenAI(api_key="sk-6cdebe6c89e944278f9f58db6a0fe608", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)