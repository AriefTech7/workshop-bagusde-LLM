from dotenv import load_dotenv
from openai import OpenAI
import os
import mysql.connector

load_dotenv()
PASSWORD = "mintaduit"
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=PASSWORD,
    database="p_chatbot",
    port=3307,
    buffered=True
)

cursor = db.cursor()


def call_llm(message_history): # mengembalikan respon dari model 
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t-chimera:free",
        messages=message_history
    )
    return response.choices[0].message.content



def login_user(username): # sebagai pengindentifikasi apakah user sudah terdaftar atau belum
    sql = "SELECT id FROM users WHERE username = %s;"
    data = [username]
    cursor.execute(sql, data)
    query = cursor.fetchall()
    user_id = 0
    for q in query:
        user_id=q[0]

    if len(query) == 0:
        print("silahkan daftar")
        username = input("Masukkan username: ")
        sql = "INSERT INTO users (username) VALUES (%s);"
        data = [username]
        cursor.execute(sql, data)
        new_user_id = cursor.lastrowid
        user_id=new_user_id
        db.commit()
        
        
    else:
        print(f"Selamat Datang Username {username}")
        
    return user_id



def save_message(user_id,role,content): # menyimpan history chat pada database
    value = (user_id,role,content)
    sql = ("insert into messages (user_id,role,content) values (%s,%s,%s)")
    cursor.execute(sql,value)
    db.commit()


def load_message_history(user_id): # mengambil history chat dari database
    history=[]
    sql = f"select role,content from messages where user_id= %s order by created_at asc;"
    value = (user_id,)
    cursor.execute(sql,value)
    db_history=cursor.fetchall()
    history.append({'role': 'system', 'content': 'you are a study assistant'},)
    for data in db_history:
        data_dict ={}
        data_dict['role']= data[0]
        data_dict['content']=data[1]
        history.append(data_dict)  
    return history

def clear_chat_history(user_id): # menghapus semua history chat pada database
    
    sql = ("delete from messages where user_id=%s;")
    value = (user_id,)
    cursor.execute(sql,value)
    sql = ("insert into messages (user_id,role,content) values (%s,%s,%s);")
    value = (user_id,'system','you are a study assistant')
    cursor.execute(sql,value)
    db.commit()
    return "Semua history berhasil dihapus"


def multiple_chat_session(): # opsional but recommded
    pass

 
# cursor.execute("select role,content from messages where user_id=%s order by created_at asc;",(user_id,))
# hasil = cursor.fetchall()
# indexNol=""
# indexSatu=""
# for i in hasil:
#     indexNol = str(i[0])
#     indexSatu = str(i[1])
# print(f"index nol {indexNol} dan index satu {indexSatu} dalam table messages")    


def main():
    username=input("Masukkan username: ")
    user_id = login_user(username=username)
    message_history=load_message_history(user_id)
    while True:
        typing_user = input("User: ")
        
        if typing_user.startswith("/"):
            if typing_user.endswith("exit"):
                print(f"Good bye {username} 🫡")
                return False
            elif typing_user.endswith("clear"):
                print(clear_chat_history(user_id))
            elif typing_user.endswith("help"):
                print("List Commands System:"\
                "\n/exit  - Close program" \
                "\n/help  - Show list commands system" \
                "\n/clear - Delete messages history")
            else:
                print("That command not available")
        else:
            save_message(user_id,"user",content=typing_user)
            message_history.append({'role': 'user', 'content': typing_user})
            ai_reply = call_llm(message_history)
            save_message(user_id,"assistant",content=ai_reply)
            message_history.append({'role': 'assistant', 'content': ai_reply})
            print(f"AI: {ai_reply}")


if __name__ == "__main__":
    main()
