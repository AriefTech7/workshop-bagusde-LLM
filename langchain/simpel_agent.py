from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import requests
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser

@tool('get_weather',description='return weather information for a given city', return_direct=False)
def get_weather(city:str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://ai.dinoiki.com/v1",
    temperature=0.7
)

parse_str = StrOutputParser()

agent = create_agent(
    llm,
    tools=[get_weather],
    system_prompt="you are a helpful weather assistant.",
    
)
response = agent.invoke(
    {
        'messages':[
            {'role':'user','content':'what is the weather like in pekanbaru?'}
        ]
    }
    
)

print(response['messages'][-1].content)