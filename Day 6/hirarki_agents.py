# Customer Support System
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from typing import TypedDict, Annotated, Literal, List

# 1.definisi State -> untuk menyimpan data yang dihasilkan oleh tiap node
class SupportState(TypedDict):
    message: Annotated[List[BaseMessage],add_messages]
    customer_query: str
    query_type: str # example "technical", "billing"
    worker_response: str
    final_response: str

# 2.inisialisasi llm
llm = ChatOpenAI(model="gpt-5-nano",temperature=0.7)

# 3.definisi manager agent 
"""
state: SupportState adalah type hint yang berfungsi memberitahu parameter state 
harus bertipe SupportState
"""
def manager_agent(state: SupportState): 
    """manager: Klasifikasi query dan route ke worker yang tepat"""
    print("\nMANAGER AGENT: Menganalisa customer query...")
    
    query=state["customer_query"]
    
    prompt=f"""kamu adalah customer support manager.
    Customer query: "{query}"
    
    Klasifikasikan query ke salah satu kategori:
    - "faq": Pertanyaan umum (pricing,features, account)
    - "technical": Masalah teknis (error,bug,performance)
    - "billing": Masalah pembayaran (invoice,refund,subscription)
    
    jawab HANYA dengan satu kata: faq, technical atau billing
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    query_type = response.content.strip().lower()
    
    # validate query
    if query_type not in ["faq","technical","billing"]:
        query_type="faq" #default
    
    return {
        "messages":[HumanMessage(content=f"Manager: Routing to {query_type}")],
        "query_type":query_type
    }
    
    # 4. definisi worker agents
    # definisi worker agents spesialis untuk menjawab pertanyaan faq 
def faq_worker(state: SupportState)->SupportState:
    """FAQ Worker: Handle pertanyaan umum"""
    print("\nFAQ WORKER: Menjawab pertanyaan umum...")
    query = state['customer_query']
    
    prompt=f"""kamu adalah FAQ Support agents.
    Customer bertanya: "{query}"
    
    Jawab dengan ramah dan informatif (2-3 kalimat).
    Referensikan documentation atau help page jika perlu.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    answer=response.content
    
    return {
        "messages":[HumanMessage(content=f"FAQ: {answer}")],
        "worker_response":answer
    }
    
    # definisi worker agents spesialis untuk menjawab pertanyaan technical
def technical_worker(state:SupportState)->SupportState:
    """Technical Worker: Handle pertanyaan teknis"""
    print("\nTECHNICAL WORKER: menjawab pertanyaan teknis...")
    query = state['customer_query']
    prompt = f"""Kamu adalah Technical Support engineer.
    Customer melaporkan: "{query}"
    
    Berikan:
    1. Diagnosis masalah
    2. Troubleshooting steps (3-4 langkah)
    3. Kapan harus escalate ke senior engineer
    """   
    
    response = llm.invoke([SystemMessage(content=prompt)])
    answer=response.content
    
    return {
        "messages":[HumanMessage(content=f"Technical: {answer}")],
        "worker_response":answer
    }
     
    # definisi worker agents spesialis untuk menjawab pertanyaan billing 
def billing_worker(state:SupportState)->SupportState:
    """Billing Worker: Handle pertanyaan masalah pembayaran"""
    print("\nBILLING WORKER: Mengatasi masalah billing...")
    
    query = state["customer_query"]
    
    prompt=f"""Kamu adalah billing support specialist.
    Customer menanyakan: "{query}"
    
    Berikan:
    1. Penjelasan tentang billing issue
    2. Langkah-langkah resolusi
    3. Timeline pengelesaian
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    answer=response.content
    
    return {
        "messages":[HumanMessage(content=f"Billing: {answer}")],
        "worker_response":answer
    }
    
    
def quality_checker(state:SupportState)->SupportState:
    """Final QC: Manager review response sebelum dikirim ke customer"""
    print("\nQUALITY CHECKER: Manager review response...")
    
    worker_answer=state['worker_response']
    
    prompt =f"""Kamu adalah QA manager.
    Review response berikut dan polish jika perlu:
    
    {worker_answer}
    
    Pastikan:
    - Professional dan empathetic
    - Clear dan actionable
    - Grammar correct
    
    Output response final yang siap dikirim ke customer.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    final=response.content
    
    
    return {
        "messages":[HumanMessage(content=f"Final: {final}")],
        "final_response":final
    }
    

    # 5. Router Function (untuk conditional edges)
def route_to_worker(state: SupportState)->Literal["faq_worker","technical_worker","billing_worker"]:
    """Routing logic berdasarkan query_type"""
    query_type = state['query_type']
    
    if query_type=="faq":
        return "faq_worker"
    elif query_type=="technical":
        return "technical_worker"
    else:
        return "billing_worker"
    
    
    # 6. Bangun graph - Hierarchical Flow
def create_hierarchical_workflow():
    workflow=StateGraph(SupportState)
    
    # add node
    workflow.add_node("manager",manager_agent)
    workflow.add_node("faq_worker",faq_worker)
    workflow.add_node("technical_worker",technical_worker)
    workflow.add_node("billing_worker",billing_worker)
    workflow.add_node("quality_checker",quality_checker)
    
    # define edges
    workflow.add_edge(START,"manager")
    
    # conditional edges: Manager router to worker yang sesuai
    workflow.add_conditional_edges(
        "manager",
        route_to_worker,
        {
            "faq_worker":"faq_worker",
            "technical_worker":"technical_worker",
            "billing_worker":"billing_worker"
        }
    )
    
    # all worker to quality checker
    workflow.add_edge("faq_worker","quality_checker")
    workflow.add_edge("technical_worker","quality_checker")
    workflow.add_edge("billing_worker","quality_checker")
    
    # Quality checker to END
    workflow.add_edge("quality_checker",END)
    
    return workflow.compile()

if __name__ == "__main__":
    print("HIERARCHICAL FLOW: Customer Support System (Manager-Worker)")

    app = create_hierarchical_workflow()
    
    test_queries = [
        "berapa harga paket premium?",
        "Aplikasi saya crash setiap kali login?",
        "Saya belum menerima invoice untuk bulan ini"
    ]
    
    for idx, query in enumerate(test_queries,1):
        print(f"\n{'='*70}")
        print(f"TEST CASE #{idx}")
        print(f"{'='*70}")
        
        initial_state = {
            "messages":[],
            "customer_query":query,
            "query_type":"",
            "worker_response":"",
            "final_response":""
        }
        
        final_state=app.invoke(initial_state)
        print(f"FINAL RESPONSE TO CUSTOMER:")
        print(final_state["final_response"])
