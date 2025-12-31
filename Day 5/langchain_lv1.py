from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI # chatopenai berfungsi untuk memanggil llm openai
from langchain_core.prompts import ChatPromptTemplate # chatprompttemplate berfungsi untuk system prompt
from langchain_core.output_parsers import StrOutputParser # mengekstrak struktur chat dan menampilkan output chat/content tanpa ada struktur

"""
flow chatbot biasa : input -> llm -> output
flow chatbot menggunakan framework langchain: history message(chatprompt)->llm(charopenai)->output
"""

SYSTEM_PROMPT = "you are a helpful assistant"
# session id = primary key pada database
prompt = ChatPromptTemplate([
    # format {role:...,content:...}
    ('system',SYSTEM_PROMPT),
    ('human', '{input}') # human(langchain) sebagai role user(openai)
])

llm = ChatOpenAI(
    model='gpt-4o-mini',
    base_url="https://ai.dinoiki.com/v1"
    # api_key= untuk api key akan otomatis mencari api key ke file .env, so tak perlu deklasi api key 
)
parse_output = StrOutputParser()

chain = prompt | llm | parse_output # history message dari prompt akan otomatis masuk ke llm

# loop chat
while True:
    user = input("You: ").strip()

    ai_message = chain.invoke({'input':user})
    print(f"AI: {ai_message}")