from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
audio_path = 'audio_2025-11-11_10-43-31.mp3'

with open(audio_path, 'rb') as f:
    result = client.audio.transcriptions.create(
        model='whisper-1',
        file=f,
        response_format='text'
    )
print(f"hasil transcripsi: \n{result}")