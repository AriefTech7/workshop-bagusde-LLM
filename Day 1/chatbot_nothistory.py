from openai import OpenAI
from  dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_APIKEY')
)

# this is a constant variable
SYSTEM_PROMPT= "You are a friendly assistant."

MAX_LENGTH = 12 * 2 + 1

history = [
    {'role':'system', 'content':SYSTEM_PROMPT}
]

while True:
    user = input("You: ").lower()
    if user == "/exit":
        break
    # memasukkan inputan role user ke history(list)
    history.append({"role": "user", "content": user})

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=history
    )

    if len(history) > MAX_LENGTH:
        response = client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[]# tolong summary history
                )
        new_history = history[0]
        history = new_history
    # memasukkan output dari ai ke variable(list) dengan role assistant
    history.append({'role':'assistant', 'content':response.choices[0].message.content})
    # menampilkan output dari ai ke terminal
    print(f"AI: {response.choices[0].message.content}")
    
    print(f"panjang history lama {len(history)}")
    