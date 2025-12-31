from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI # chatopenai berfungsi untuk memanggil llm openai
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
# mengintegrasikan tool ke model ai
from langchain_core.tools import tool 
from langchain.agents import create_agent

"""Note
tidak bisa menggunakan function stroutputparser karena create_agent membutuhkan struktur khusus
"""

# Berikut adalah cara untuk membuat tool calling
@tool # ini adalah dekuretor
# setiap param harus dideklarasi tipe data dan tipe data apa yang akan dihasilkan
def multiply(a:float, b:float)-> float:
    """kalikan dua angka dan kembalikan nilainya"""
    return a * b

@tool
def add(a:int, b:int)-> int:
    """Menambahkan dua angka dan kembalikan nilainya"""
    return a + b

@tool
def to_lower(text:str)->str:
    """Mengubah semua text menjadi huruf kecil"""
    return text.lower()

TOOLS=[multiply, add, to_lower]

# prompt


"""
ChatPromptTemplate berfungsi untuk system prompt
MessagesPlaceholder berfungsi   
"""

"""
flow chatbot biasa : input -> llm -> output
flow chatbot menggunakan framework langchain: history message(chatprompt)->llm(charopenai)->output
"""

SYSTEM_PROMPT = """You are a helpful assistant.
Use tools when they help solve the user's request.
Prefer `multiply` for arithmetic like "x times y".
Keep answers short and correct.
"""
# session id = primary key pada database
prompt = ChatPromptTemplate.from_messages([
    # format {role:...,content:...}
    ('system',SYSTEM_PROMPT),
    MessagesPlaceholder('chat_history'),
    ('human', '{input}'), # human(langchain) sebagai role user(openai)
    MessagesPlaceholder('agent_tool')
])

llm = ChatOpenAI(
    model='gpt-5-nano',
    base_url="https://ai.dinoiki.com/v1"
    # api_key= untuk api key akan otomatis mencari api key ke file .env, so tak perlu deklasi api key 
)

# flownya : prompt -> LLM -> analize -> execute


save_memory = MemorySaver()
agent_with_memory = create_agent(
    llm,
    TOOLS,
    checkpointer=save_memory,
    system_prompt=SYSTEM_PROMPT
)

# loop chat
if __name__ == "__main__":
    thread_id='demo-level-3'
    config={'configurable':{'thread_id':thread_id}}
while True:
    user = input("You: ").strip()
    if user == "exit":
        print("byee")
        break
    ai_message = agent_with_memory.invoke({'messages':[('user',user)]},config=config)
    print(f"AI: {ai_message['messages'][-1].content}")