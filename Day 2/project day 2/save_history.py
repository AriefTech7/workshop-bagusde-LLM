import json

chat_history = [
    {'role':'system','content':'you are a study assistant'}
]
# function untuk melakukan save history kedalam file json dengan jumlah yang ditentukan
def save_history(number):
    filename='history_chat.json'
    data_of_saved = chat_history[:number+1] if len(chat_history) > number else chat_history
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_of_saved, f, indent=2, ensure_ascii=False)
    
    print(f"\n[System] Chat history saved to {filename}\n")