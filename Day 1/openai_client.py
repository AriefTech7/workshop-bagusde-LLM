# library openai berfungsi untuk berkomunikasi dengan server openai. harus ada API openainya
from openai import OpenAI 
# library dotenv berfungsi untuk memuat file .env kedalam file ini
from dotenv import load_dotenv
import os

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
    ]
)
print(f"AI: {respone.choices[0].message.content}")


# cara cek koneksi API openai
# try:
#     models = client.models.list()
#     for model in models:
#         print(model)
# except Exception as e:
#     print("tidak ada")
