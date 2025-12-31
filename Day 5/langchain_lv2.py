from dotenv import load_dotenv
load_dotenv()

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI # chatopenai berfungsi untuk memanggil llm openai
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain_core.output_parsers import StrOutputParser

"""
ChatPromptTemplate berfungsi untuk system prompt
MessagesPlaceholder berfungsi   
"""

"""
flow chatbot biasa : input -> llm -> output
flow chatbot menggunakan framework langchain: history message(chatprompt)->llm(charopenai)->output
"""

SYSTEM_PROMPT = "you are a helpful assistant"
# session id = primary key pada database
prompt = ChatPromptTemplate.from_messages([
    # format {role:...,content:...}
    ('system',SYSTEM_PROMPT),
    MessagesPlaceholder('chat_history'),
    ('human', '{input}') # human(langchain) sebagai role user(openai)
])

llm = ChatOpenAI(
    model='gpt-5-nano',
    base_url="https://ai.dinoiki.com/v1"
    # api_key= untuk api key akan otomatis mencari api key ke file .env, so tak perlu deklasi api key 
)

# store history per session id
session_store = {}
def get_history(session_id):
    # if session_id in session_store:
    #     return session_store[session_id]
    # else:
    #     session_store[session_id] = InMemoryChatMessageHistory
    #     return session_store[session_id]

    # best practice
    if session_id not in session_store:
        session_store[session_id]=InMemoryChatMessageHistory()
    return session_store[session_id]

parse_output = StrOutputParser()
chain = prompt | llm | parse_output# history message dari prompt akan otomatis masuk ke llm

agent = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key='input',
    history_messages_key='chat_history'
)

# loop chat
session_id ='demo-level-2'
while True:
    user = input("You: ").strip()

    ai_message = agent.invoke(
        {'input':user},
        config={'configurable':
                {'session_id':session_id}
                }
                              )
    print(f"AI: {ai_message}")