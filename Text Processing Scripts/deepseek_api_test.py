#This is just checking the API key, actual cleaner is under text processing scripts
from openai import OpenAI

client = OpenAI(api_key="sk-17bb09d52e354980846653b153efcfb4", base_url="https://api.deepseek.com") #sk-17bb09d52e354980846653b153efcfb4, or sk-6cdebe6c89e944278f9f58db6a0fe608

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)