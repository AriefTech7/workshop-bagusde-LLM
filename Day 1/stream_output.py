# library openai berfungsi untuk berkomunikasi dengan server openai. harus ada API openainya
from openai import OpenAI 
# library dotenv berfungsi untuk memuat file .env kedalam file ini
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_APIKEY')
)

chat = input("You: ")
respone = client.chat.completions.create(
    # memilih model yang akan merespons
    model='gpt-4o-mini',
    # menentukan sistem prompt model AI
    messages=[
        {'role':'system', 'content':'you are study assistant.'},
        {'role':'user', 'content':chat}
    ],
    stream=True
)
full_respone = ""
for chunk in respone:
    # None
    if chunk.choices[0].delta.content is not None: 
        content = chunk.choices[0].delta.content
        # parameter flush berfungsi menampilkan teks seketika, tanpa menunggu seluruh hasil selesai diproses.
        print(content, end="", flush=True)
        time.sleep(0.1)
        content += full_respone
    
    


# cara cek koneksi API openai
# try:
#     models = client.models.list()
#     for model in models:
#         print(model)
# except Exception as e:
#     print("tidak ada")

