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


def call_llm(message_history):
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t-chimera:free",
        messages=message_history
    )
    return response.choices[0].message.content




# user_id=""

def login_user(username):
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



def save_message(user_id,role,content):
    value = (user_id,role,content)
    sql = ("insert into messages (user_id,role,content) values (%d,%s,%s)")
    cursor.execute(sql,value)
    db.commit()


def load_message_history(user_id):
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
        save_message(user_id,"user",content=typing_user)
        message_history.append({'role': 'user', 'content': typing_user})
        if typing_user.lower() == "keluar":
            return False

        ai_reply = call_llm(message_history)
        save_message(user_id,"assistant",content=ai_reply)
        message_history.append({'role': 'assistant', 'content': ai_reply})
        print(f"AI: {ai_reply}")


if __name__ == "__main__":
    main()
