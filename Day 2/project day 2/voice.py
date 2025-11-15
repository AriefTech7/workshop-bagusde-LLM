import sounddevice as sd
import scipy.io.wavfile as wv
from config import client
from pathlib import Path
from playsound import playsound


# function untuk merekam suara dan menyimpannya pada sebuah file
def record_voice(seconds=5,filename='input.wav', fs=44100):
    print("Merekam user...")
    audio = sd.rec(
        int(seconds * fs), 
        samplerate=fs, 
        channels=1, 
        dtype='int16'
        )
    sd.wait()
    # Simpan file
    wv.write(filename,fs , audio)
    print("Rekaman selesai!")
    return filename

# function ini membaca binary file audio dengan model whisper dan mengembalikan nilai dengan tipe data string
def stt(audio_path):
    with open(audio_path, 'rb') as file:
        text = client.audio.transcriptions.create(
            model='whisper-1',
            file=file,
            response_format='text'
        )
    print(f"You: {text}")
    return str(text)

# function ini menerima dan menambahkan history dari chat user dan ai sehingga model ai bisa memberikan respon 
def respon_ai(chat, chat_history):
    chat_history.append({'role':'user', 'content':chat})
    ai = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=chat_history,
        temperature=0.7
    )
    ai = ai.choices[0].message.content
    print(f"AI: {chat}")

    chat_history.append({'role':'assistant', 'content':chat})
    return  ai, chat_history   

# function ini menerima respon model ai dan mengubah respon menjadi audio yang tersimpan pada file dan file audio dijalankan dengan tipe data string
def tts(text, file_out="output_audio.mp3"):
    out_audio = Path(file_out)
    with client.audio.speech.with_streaming_response.create(
        model='gpt-4o-mini-tts',
        voice='alloy',
        input=text
    ) as audio:
        audio.stream_to_file(out_audio)
    print("AI berbicara...")
    playsound(str(out_audio))

# function yang menjadi induk untuk menjalankan semua function kedalan function ini
def run_voice():
    from save_history import chat_history   
    print("Voice Chat AI")
    print("Ketik 'exit' kapan saja untuk keluar.\n")
    while True:
        audio_path = record_voice()
        user = stt(audio_path).strip().lower()

        if "exit" in user or "keluar" in user:
            print("Good Bye")
            break

        chat, chat_history = respon_ai(user, chat_history)
        tts(chat)


   