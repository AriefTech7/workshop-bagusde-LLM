from dotenv import load_dotenv
load_dotenv()

import subprocess
from langchain_openai import ChatOpenAI     
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver



@tool
def run_linux_command(query: str) -> str:
    """Fungsi untuk mendapatkan perintah Linux berdasarkan query pengguna."""
    hasil = subprocess.run(query, shell=True, capture_output=True, text=True)
    return f"hasil perintah '{query}':\n{hasil.stdout}\n{hasil.stderr}"

TOOLS =[run_linux_command]

llm = ChatOpenAI(
    model='gpt-4o-mini',
)

memory = MemorySaver()
# menentukan apakah agent perlukan tools atau tidak, jika diperlukan maka akan memanggil tools yang sudah didefinisikan
# workflow: prompot -> llm -> agent -> analize(use tools or no) -> execute or response


agent = create_react_agent(llm,TOOLS,checkpointer=memory)  


session = {"configurable": {"thread_id": "user1-level2"}}  # Contoh session ID, bisa diganti sesuai kebutuhan


print("🐧 Linux Agent siap. Ketik 'exit' untuk keluar.")
while True:
    user = input('User: ').strip()
    if user.lower() in ['exit', 'quit', 'keluar']:
        print('Exiting...')
        break
    response = agent.invoke({"messages":[("human",user)]},config=session)
    print(f"assistant :{response['messages'][-1].content}")
    



