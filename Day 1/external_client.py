from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    # menggunakan model ai yang ada diopenrouter
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENROUTER_KEY')
)

chat = input("You: ")
# client.chat.completions.create -> method untuk memberikan respons menggunakan openai
respone = client.chat.completions.create(
    model="x-ai/grok-4-fast",
    messages=[
        {'role':'system', 'content':'You are a finance assistant.'},
        {'role':'user', 'content':chat}
    ]
)
print(f"AI: {respone.choices[0].message.content}")

