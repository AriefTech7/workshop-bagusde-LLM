from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


user_txt = "gue pengen bmw m4"

response = client.embeddings.create(
    model='text-embedding-3-small',
    input=user_txt
)

embedd = response.data[0].embedding
print(embedd)
