from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# function untuk mendecode gambar menjadi binary dan direturn dari binary ke teks
def decode_image(image):
    # membaca gambar
    with open(image, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')
    
        

image_url = 'asset/download (6).jpeg'
data_decode = decode_image(image_url)

respone = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        # metode untuk model memahami suatu gambar secara online
        {'role':'user', 'content':[
            {'type':'text', 'text':'bisakah kamu menjelaskan gambar ini?'},
            # cara memproses/menganalisis suatu gambar kedalam text 
            {'type':'image_url', 'image_url':{'url':f'data:image/jpeg;base64,{data_decode}'}}
            ]
        }
    ]
)

print(respone.choices[0].message.content)
