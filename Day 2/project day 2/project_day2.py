# nama function tidak boleh ada yang sama sehingga tidak menimpa function lain
from response_normaly import respon_normaly
from response_stream import respon_stream
from save_history import save_history
from save_history import chat_history
from voice import run_voice


def main():
    # stream mode
    on_stream = False
    print("Welcome to My First AI Chatbot in Terminal")
    print("\nCommands:\n/exit→keluar" \
    "\n/on stream→aktifkan streaming" \
    "\n/off stream→non aktifkan streaming" \
    "\n/save→simpan history" \
    "\n/voice→voice to text and text to voice")
        
    while True:
        user = input("You: ").lower()
                    
        if user == "/exit":
            break
        elif user == "/on stream":
            on_stream = True
            print("stream mode on")
            continue
        elif user == "/off stream":
            on_stream = False
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
        elif user == "/voice":
            print("text to voice")
            run_voice()
            continue


        chat_history.append({'role':'user', 'content':user}) 

        if not on_stream:
            reply_ai = respon_normaly(chat_history)
        else:
            reply_ai = respon_stream(chat_history)
        chat_history.append({'role':'assistant', 'content':reply_ai})

if __name__ == "__main__":
    main()    

    

    