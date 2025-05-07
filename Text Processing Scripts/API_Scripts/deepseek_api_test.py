#This is just checking if the API key works
from openai import OpenAI

client = OpenAI(api_key="<key>", base_url="https://api.deepseek.com") 

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
