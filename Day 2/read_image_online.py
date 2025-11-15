from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

image_url = 'https://blue.kumparan.com/image/upload/fl_progressive,fl_lossy,c_fill,f_auto,q_auto:best,w_640/v1634025439/01hm85yfhp8ab74ps3xmymkzmh.jpg'

respone = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        # metode untuk model memahami suatu gambar secara online
        {'role':'user', 'content':[
            {'type':'text', 'text':'bisakah kamu menjelaskan gambar ini?'},
            {'type':'image_url', 'image_url':{'url':image_url}}
            ]
        }
    ]
)

print(respone.choices[0].message.content)
