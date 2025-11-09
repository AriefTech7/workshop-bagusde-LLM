from openai import OpenAI
from dotenv import load_dotenv
import os
import json


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_API_KEY")
)


chat_history = [
    {'role':'system','content':'you are a study assistant'}
]

def save_history(filename, number):
    filename='history_chat.json'
    data_of_saved = chat_history[:number+1] if len(chat_history) > number else chat_history
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_of_saved, f, indent=2, ensure_ascii=False)
    
    print(f"\n[System] Chat history saved to {filename}\n")
    
# function untuk respon dari ai yang normal
def respone_normaly(history):
    response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=history
    )
    print(f"AI: {response.choices[0].message.content}")
    return response.choices[0].message.content

# function untuk respon dari ai yang ada animasi 
def respone_stream(history):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=history,
        stream=True
    )
    full_response = ""
    print("AI: ", end="")
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            
        print(content, end="", flush=True)
    print()
    return full_response


# stream mode
on = False
print("Welcome to My First AI Chatbot in Terminal")
print("\nCommands:\n1./exit->untuk keluar" \
"\n2./on stream->mengaktifkan mode stream" \
"\n3./off stream->menonaktifkan mode stream" \
"\n4./save->menyimpan data history")
    
while True:
    user = input("You: ").lower()
    if user == "/exit":
        break
    elif user == "/on stream":
        on = True
        print("stream mode on")
        continue
    elif user == "/off stream":
        on = False
        print("strem mode off")
        continue
    elif not user:
        print("kosong, tolong input sesuatu")
        continue
    elif user == "/save":
        count_data_save = int(input("berapa banyak history yang ingin disimpan? "))
        print("your history saved")
        save_history(chat_history, count_data_save)
        continue

    chat_history.append({'role':'user', 'content':user})
    
    if on is not True:
        ai = respone_normaly(chat_history)
    else:
        ai = respone_stream(chat_history)
    chat_history.append({'role':'assistant', 'content':ai})    

    

    