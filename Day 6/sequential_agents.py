# agent untuk menulis blog
"""
State -> menyimpan semua data (user_input, output research, output writer, output editor dan final article)
untuk mendapatkan ai response = State['final article'].
Berarti semua ai agent ada didalam State
"""
"""
flow agent blog:
input -> research -> writer -> editor -> final_output(final artikel)
"""
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
"""
TypeDict berfungsi memperlihatkan errer pada variabel bertipe Dict
"""


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]
    topic: str
    research_result: str
    draft_article: str # tempat hasil writer agent
    final_article: str # tempat hasil editor agent
    
llm =ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.1 # semakin mendekatin 1 semakin kreatif, semakin jauh dari satu semakin tidak kreatif modelnya
)

def research_agent(State: AgentState) -> AgentState:
    """Melakukan riset tentang topik"""
    print('Resarch Agent sedang melakukan tugasnya...')
    prompt = f"""
    kamu adalah research assistant.
    Riset topik berikut dan berikan 3-5 poin penting: {State['messages']}
    
    format output:
    -poin 1
    -poin 2
    -poin 3
    -dst...
    """
    
    response = llm.invoke([SystemMessage(prompt)])
    research = response.content 
    
    return {
        'messages':[SystemMessage(content=f'Research: {research}')],
        'research_result':research
    }
    
    
def writer_agent(State: AgentState) -> AgentState:
    """Menulis draft artikel berdasarkan hasil riset"""
    print('Writer Agent sedang melakukan tugasnya...')
    prompt = f"""
    kamu adalah content writer.
    Topik: {State['topic']}
    
    Berdasarkan research berikut:
    {State['research_result']}
    
    Tulis artikel blog (300-400 kata) dengan struktur:
    - judul menarik
    - intro
    - body (3 paragraf)
    - kesimpulan
    """
    
    response = llm.invoke([SystemMessage(prompt)])
    draft = response.content 
    
    return {
        'messages':[SystemMessage(content=f'Research: {draft}')],
        'draft_article':draft
    }
    
def editor_agent(State: AgentState) -> AgentState:
    """Mengedit dan memperbaiki artikel"""
    print('Editor Agent sedang melakukan tugasnya...')
    prompt = f"""
    kamu adalah seorang artikel editor profesional.
    Draft artikel: 
    {State['draft_article']}
    
    tugasmu :
    1. perbaiki grammar dan typo
    2. improve flow dan readability
    3. pastikan struktur jelas
    4. output final artike sudah dipoles
    
    """
    
    response = llm.invoke([SystemMessage(prompt)])
    final = response.content 
    
    return {
        'messages':[SystemMessage(content=f'Research: {final}')],
        'final_article':final
    }
    

def create_sequential_flow():
    # StateGraph ini adalah graph
    workflow = StateGraph(AgentState)
    
    # bangun flownya
    
    # 1) register nodenya
    workflow.add_node('researcher',research_agent)
    workflow.add_node('writer',writer_agent)
    workflow.add_node('editor',editor_agent)
    
    # 2) menghubungkan nodenya
    workflow.add_edge(START, 'researcher')   
    workflow.add_edge('researcher','writer')   
    workflow.add_edge('writer', 'editor')   
    workflow.add_edge('editor',END)   
    
    # 3) menambahkan memory 
    checkpointer = MemorySaver()
    
    # 4) mengembalikan nilai
    return workflow.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    print("sequential flow: blog artikel generator")
    app = create_sequential_flow()
    
    id= 1
    THREAD_ID = 'gue-1'
    
    user_input = input("\nYou: ").strip()
    
    initial_value = {
        'messages':[HumanMessage(user_input)],
        'topic':user_input,
        'research_result': '',
        'draft_article': '',
        'final_article': ''
    }
    
    app.invoke(initial_value, config={'configurable':{'thread_id':THREAD_ID}})
    
    final_state = app.get_state(config={'configurable':{'thread_id':THREAD_ID}})
    print('Artikel final: ')
    print(f"{final_state.values.get('final_article')}")
    
    while True:
        user_input = input("\nYou: ").strip()
        id+=1
        CURRENT_THREAD = f'gue-{id}'
        
        
        human = {
            'messages':[HumanMessage(content=user_input)],
            'topic':user_input,
            'research_result': '',
            'draft_article': '',
            'final_article': ''
        }
        
        
        app.invoke(human,config={'configurable':{'thread_id':CURRENT_THREAD}})
        current_state = app.get_state(config={'configurable':{'thread_id':CURRENT_THREAD}})
        result_state = current_state.values.get('final_article')
        print('artikel terbaru: ')
        print(f"{result_state}")
        