from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI     
from langchain_core.prompts import ChatPromptTemplate 

prompt = ChatPromptTemplate([
    ('system','You are a helpful assistant about Linux.'),
    ('human','{input}') # {input} adalah sebuah placeholder untuk menerima input dari pengguna
])

llm = ChatOpenAI(
    model='gpt-4o-mini',
)

chain = prompt | llm

while True:
    user = input('User: ').strip()
    if user.lower() in ['exit', 'quit', 'keluar']:
        print('Exiting...')
        break
    response = chain.invoke({"input": user})
    print(f'Assistant: {response.content}')

