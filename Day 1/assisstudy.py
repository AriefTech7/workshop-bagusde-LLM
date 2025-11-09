from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_KEY")
)

chat = input("You: ")
respone = client.chat.completions.create(
    model='tngtech/deepseek-r1t2-chimera:free',
    messages=[
        {'role':'system', 'content':'You are a study assistant.'},
        {'role':'user', 'content':chat}
    ],
    stream=True
)

full_respone = ""

for chunk in respone:
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        full_respone += content
        # print(chunk.choices[0].delta.content, end="", flush=True)
print(f"AI: {full_respone}", flush=True)
time.sleep(0.2)
print()  # New line setelah stream selesai


