from dotenv import load_dotenv
from openai import OpenAI
import os
# library yang bisa dalam mengguanakn path
from pathlib import Path
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
text = "Halo, saya arif ganteng!!"
file_audio = Path(f'audio_{timestamp}.mp3')

with client.audio.speech.with_streaming_response.create(
    model='gpt-4o-mini-tts',
    voice='alloy',
    input=text
) as audio:
    audio.stream_to_file(file=file_audio)
