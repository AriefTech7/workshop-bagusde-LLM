# agent yang menulis blog
"""
hal yang perlu dibuat untuk agent blog ini:
state -: yang menyimpan semua data(user input, research(output), writer(output),editor(output),final output)
jadi nilai state terakhir adalah state['final_output'] 

"""
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
 # TypedDict berfungsi untuk mendeteksi apakah key benar atau salah
from typing import TypedDict, Annotated, List
from langgraph.checkpoint.memory import MemorySaver

class AgenState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    topic: str
    research_result: str # tempat hasil research agent
    draft_article: str  # tempat hasil writer agent
    final_article: str  # tempat hasil editor agent

llm = ChatOpenAI(
    model='gpt-4o-mini',
    base_url="https://ai.dinoiki.com/v1",
    temperature=0.7 #mengatur sebarapa kreatif model kita
    
)

def research(State: AgenState) -> AgenState:
    """Melakukan riset tentang topik"""
    print('research agent sedang melakukan tugasnya...')
    prompt = f"""Kamu adalah reseach assistant.
    Riset topik berikut dan berikan 3 - 6 poin penting: {State['topic']}
    Format output:
    - poin 1
    - poin 2
    - poin 3
    - dkk ...
    """
    response= llm.invoke([SystemMessage(prompt)])
    research_response = response.content
    return {
        'messages': [SystemMessage(content=f'Research: {research_response}')],
        'research_result':research_response
    }

def writer(State: AgenState) -> AgenState:
    """Menulis draft artikel berdasarkan  hasil riset"""
    print('writer agent sedang melakukan tugasnya...')
    prompt = f"""Kamu adalah content writer.
    Topik: {State['topic']}
    Berdasarkan research berikut:
    {State['research_result']}

    Tulis artikel blog (300 - 800 kata) dengan struktur:
    - Judul  
    - Perkenalan
    - Body (4 paragraf)
    - Kesimpulan
    """
    response= llm.invoke([SystemMessage(prompt)])
    draft = response.content

    return {
        'messages': [SystemMessage(content=f'Research:{draft}')],
        'draft_article': draft
    }

def editor(State: AgenState)-> AgenState:
    """Mengedit dan memperbaiki artikel"""
    print('editor agent sedang melakukan tugasnya...')
    prompt =f"""Kamu adalah seorang artikel editor profesional.
    Draft artikel: {State['draft_article']}
    Tugasmu:
    1.Perbaiki tata bahasa dan typo
    2.Improve flow dan readability
    3.Pastikan struktur artikel jelas
    4.Output final artikel yang sudah diperbaiki
    """
    response= llm.invoke([SystemMessage(prompt)])
    final = response.content
    return {
        'messages':[SystemMessage(content=f'Editor: {final}')],
        'final_article':final
    }

def create_sequential_flow():
    workflow = StateGraph(state_schema=AgenState)

    workflow.add_node('researcher', research)
    workflow.add_node('writer', writer)
    workflow.add_node('editor', editor)

    workflow.add_edge(START, 'researcher')
    workflow.add_edge('researcher','writer')
    workflow.add_edge('writer','editor')
    workflow.add_edge('editor',END)

    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    print("sequenflow : blog artikel generator")
    app = create_sequential_flow()
    THREAD_ID = "history_id"

    user_input = input("\nYou: ").strip()
           
    initial_value = {
        'messages':[HumanMessage(user_input)],
        'topic':user_input,
        "research_result": "", # tempat hasil research agent
        "draft_article": '',  # tempat hasil writer agent
        "final_article": ''
    }

    app.invoke(initial_value, config={'configurable':{'thread_id':THREAD_ID}})

    final_state = app.get_state(config={'configurable':{'thread_id':THREAD_ID}})
    print(f"Artikel final:\n{final_state.values.get('final_article','')}")

    # chat loop
    while True:
        user_input = input("\nYou: ").strip()
        if user_input == "exit":
            print("byee")
            break
        delta = {
            'messages':[HumanMessage(user_input)],
        }

        app.invoke(delta, config={'configurable':{'thread_id':THREAD_ID}})

        current = app.get_state(config={'configurable':{'thread_id':THREAD_ID}})
        current_article = app.get_state('final_article', '')
        print(f"Artikel final:\n{current_article}")