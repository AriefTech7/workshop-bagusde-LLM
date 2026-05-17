from dotenv import load_dotenv 
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage, AIMessage, HumanMessage
from langgraph.graph.message import BaseMessage, add_messages

from typing import TypedDict, Annotated,List, Literal
# .agents mengambil program di direktori yang sama
from .agents import (
    PlannerAgent,CodeReviewerAgent,CoderAgent,TesterAgent,DebuggerAgent,DependencyManagerAgent,DocumentationAgent,get_agent
)
from .tools import ask_approval

class CodingState(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]
    task: str
    plan: str
    code_generated: bool
    code_result:str
    test_passed: bool
    needs_debuggin: bool
    current_step: str
    file_created: List[str]
    next_action: str


class CodingOrchestration:
    def __init__(self):
        self.planner = PlannerAgent()
        self.review = CodeReviewerAgent()
        self.coder = CoderAgent()
        self.tester = TesterAgent()
        self.debuger = DebuggerAgent()
        self.dep_manager = DependencyManagerAgent()
        self.doc_agent = DocumentationAgent()
        
    def _planner_node(self, state: CodingState)->CodingState:
        """Node untuk planning""" 
        
        print("PLANNER AGENT status: prosess") 
        plan=self.planner.run(state["task"])
        
        print("PLAN:")
        print(plan) 
        approv = ask_approval(
            "gass ga ni bro?",
            "Planner agent sudah buatkan rencana untuk coding kamu"
        )  
        if not approv:
            print("user tidak menyetujuin hal itu")
        
           
        next_action = "approved" if approv else "rejected"
        
        return {
            "next_action":next_action,
            "current_step":"planning complete",
            "messages":AIMessage(content=f"Plan: {plan}"),
            "plan":plan
        }
    
    
    def _dependencyManager_node(self, state: CodingState)->CodingState:
        """Node untuk install dependency""" 
        
        intruksi = f"""Berdasarkan plan ini: 
        {state['plan']}
        
        task: {state['task']}
        Install semua dependency yang diperlukan, dan penting.
        
        """
        
        print("DEPENDENCY AGENT status: prosess") 
        result=self.dep_manager.run(state[intruksi])
    
        print(result)
        
        return {
            "messages":AIMessage(content=f"{result}"),
            "current_step":"dependencies_installed"
        }
    
    def _coder_node(self, state: CodingState)->CodingState:
        """Node untuk code ke dalam file""" 
        
        intruksi = f"""Task: {state['task']}
        Plan yang perlu diikuti:
        {state['plan']}
        
        Buatkan sebuah file yang berisi code sesuai dengan yang dispesifikkan pada plan.
        Gunakan write_file tool untuk membuat setiap file.
        Buat code yang bersih dan terdokumentasi dengan baik.
        """
        
        print("CODER AGENT status: prosess") 
        result=self.coder.run(state[intruksi])
        
        print(result) 
        
        file_created = []
        if "created" in result.lower() or "wrote" in result.lower():
            file_created.append('copy_code.py')
        
        return {
            "messages":AIMessage(content=f"{result}"),
            "current_step":"code_generated",
            "code_generated":True,
            "file_created":state.get("file_created",[]),
            "code_result":result
        }
        
    def _reviewer_node(self, state: CodingState)->CodingState:
        """Node review hasil code yang sudah digenerate""" 
        
        intruksi = f"""
        Review code yang sudah dibuat pada node sebelumnya ini:
        {state['code_result']}        
        
        Dengan tugas: {state['task']}
        
        Berikan feedback dengan memperhatikan beberap hal ini:
        1.Code quality
        2.Best practice
        3.Potential issue
        4.Suggestion for improvement
        
        """
        
        print("REVIEW AGENT status: prosess") 
        result=self.review.run(state[intruksi])
        
        print('\nPilihan:')
        print("1. Approve and contionue to testing")
        print("2. Request revision")
        print("3. Skip tests")
        
        option = input("Pilihanmu (1/2/3): ").strip()
    
        next_action = 'approved' 
        if option == '2':
            next_action="need_revision"
        elif option == '3':
            next_action="Skip_tests"
        else:
            print('Proceding to test...')
        
        return {
            "messages":AIMessage(content=f"Review_results: {result}"),
            "current_step":"code_review",
            "next_action":next_action
        }
        
        
    def _tester_node(self, state: CodingState)->CodingState:
        """Node untuk test hasil code yang sudah direview""" 
        
        intruksi = f"""
        Buat dan jalankan sebuah test untuk:
        Task: {state['task']}
        Code Result: {state['code_result']}
        """
        
        print("REVIEW AGENT status: prosess") 
        result=self.tester.run(state[intruksi])
        
        tests_passed = 'passed' in result.lower() or 'success' in result.lower()
        
        next_action = 'passed' if tests_passed else 'failed'
        
        return {
            "messages":AIMessage(content=f"Tester_results: {result}"),
            "current_step":'test_complete',
            "next_action":next_action,
            "test_passed":tests_passed
        }
        
        
    def _debugger_node(self, state: CodingState)->CodingState:
        """Node debug error pada code.""" 
        
        intruksi = f"""
        Debug and fix code dari hasil testing:
        Task: {state['task']}
        Code: {state['code_result']}
        
        Test sebelumnya menunjukkan error, bantu untuk:
        1. Analisa bagian mana yang kurang tepat
        2. Identifikasi akar penyebab masalah
        3. Perbaiki errornya
        4. Jelaskan apa yang sudah di fix
        """
        
        print("DEBUGGER AGENT status: prosess") 
        result=self.debuger.run(state[intruksi])
        
        print("Re-running the test after fixed")
            
        return {
            "messages":AIMessage(content=f"Debug_results: {result}"),
            "current_step":'bug_fixed',
            "code_result":result
        }
        
    def _documentation_node(self, state: CodingState)->CodingState:
        """Node untuk documetation dari hasil code.""" 
        
        intruksi = f"""
        Buatkan dokumentasi dari apa yang sudah dibuat sebelumnya:
        Task: {state['task']}
        Code: {state['code_result']}
        
        """
        
        print("DOCUMENTATION AGENT status: prosess") 
        result=self.doc_agent.run(state[intruksi])
        
            
        return {
            "messages":AIMessage(content=f"Review_results: {result}"),
            "current_step":'documentation_completed'
        }
        
    
    # CONDITIONAL FUNCTIONS
    
    def _shoud_proceed_fro_plan(self, state: CodingState) -> Literal['approved',"rejected"]:
        return state.get['next_action', 'rejected']
    
    def _shoud_proceed_fro_review(self, state: CodingState) -> Literal['approved',"need_revision","Skip_tests"]:
        return state.get['next_action', 'approved']
    
    # 2:19:24
