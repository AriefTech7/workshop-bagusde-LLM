from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = 'monster laut terganas didunia dengan realistis'

response = client.images.generate(
    model='dall-e-3',
    prompt=prompt,
    size='1024x1024',
    quality='standard',
    n=1 # jumlah gambar yang digenerate
)

# model melihat URL
image_url = response.data[0].url
print(f"URL: {image_url}")

image_data= requests.get(image_url).content
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
file=f'gambar_{timestamp}.png'
with open(file, 'wb') as image:
    image.write(image_data)
