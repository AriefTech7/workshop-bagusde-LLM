import os 
from openai import OpenAI
import PyPDF2
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
client_embdd = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name='text-embedding-3-small'
)

client_chromadb = chromadb.PersistentClient("./chroma_db")
