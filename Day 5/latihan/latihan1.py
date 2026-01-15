from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm =  ChatOpenAI(
    base_url="https://ai.dinoiki.com/v1",
    model="gpt-4o-mini"
)

SYSTEM_PROMPT='you are a helpful assistant'
prompt = ChatPromptTemplate([
    ('system',SYSTEM_PROMPT),
    ('human','{input}')
])
parse_output = StrOutputParser()
chain = prompt | llm | parse_output

while True:
    user_input = input("You: ").strip()
    if user_input in {'exit', 'keluar'}:
        print("good bye")
        break
    response = chain.invoke({'input':user_input})
    print(f"AI: {response}")

# prompt = PromptTemplate(
#     input_variables=['text'],
#     template="""
#     Analisa teks berikut:

#     teks:
#     {text}

#     Berikan hasil dengan format:
#     -topik utama:
#     -ringkas:
#     """
# )


# chain =prompt | llm | parse_output

# while True:
#     user_input = input("Masukkan teks: ")
#     if user_input in {'exit', 'keluar'}:
#         print("good bye")
#         break
#     response = chain.invoke({'input',user_input})
#     print(f"AI: \n{response}")