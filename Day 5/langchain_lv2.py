from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI     
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory


prompt = ChatPromptTemplate([
    ('system','You are a helpful assistant about Linux.'),
    MessagesPlaceholder('chat_history'), # Placeholder untuk menyimpan riwayat percakapan
    ('human','{input}') # {input} adalah sebuah placeholder untuk menerima input dari pengguna
])

llm = ChatOpenAI(
    model='gpt-4o-mini',
)

chain = prompt | llm

sesson_store = {}

def get_chat_history(session_id):
    if session_id not in sesson_store:
        sesson_store[session_id] = InMemoryChatMessageHistory()
    return sesson_store[session_id]

agent = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_key='input',
    history_messages_key='chat_history'
)

session_id = 'user1-level2'  # Contoh session ID, bisa diganti sesuai kebutuhan
while True:
    user = input('User: ').strip()
    if user.lower() in ['exit', 'quit', 'keluar']:
        print('Exiting...')
        break
    response = agent.invoke({'input':user},
                            config={'configurable': 
                                    {'session_id': session_id}
                                    }
                            )
    print(f'Assistant: {response.content}')
    # print(f"\nsession_store: {sesson_store}\n")

