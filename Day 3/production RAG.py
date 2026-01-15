from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np
import chromadb
from chromadb.utils import embedding_functions

# 


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client_embdd = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_name='text-embedding-3-small'
)
# menentukan dimana data vector akan disimpan
client_chroma = chromadb.PersistentClient('./chroma_db')
"""
collect bisa menyimpan semua chunks yang otomatis diubah ke embedding menggunakan client_embdd
"""
collect = client_chroma.get_or_create_collection(
    name='knowledge_base',
    metadata={'description':'Production RAG knowledge base example'},
    embedding_function=client_embdd
)

def semantic_search(query, n_result=3):
    result = collect.query(
        query_texts=[query],
        n_results=n_result
    )
    relevant_chunk =[]
    """
    mengambil respon pertama dari dokumen pada text
    """ 
    for i in range(len(result['documents'][0])):
        relevant_chunk.append({
            'text':result['documents'][0][i],
            'source':result['metadatas'][0][i]['source'],
            'distance':result['distances'][0][i] # -> panjang dari vector/cosine similarity
        })
    return relevant_chunk    

def generate_answer(chat_history):
    respone = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=chat_history
    )   
    return respone.choices[0].message.content 

# function untuk menginputkan dokumen
def load_docum(folder_path):
    dokument = []
    # contoh isi dokument
    # dokument = [
    # {'file_name':'file name pertama', 'content':'content'},
    # {'file_name':'file name pertama', 'content':'content'},
    # {'file_name':'file name pertama', 'content':'content'},
    # ]

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r',encoding='utf-8') as f:
                content = f.read()
                dokument.append({
                    'file_name':file_name,
                    'content':content
                })

    return dokument            

# function untuk menchunking dokumen
def chunk_text(text, chunk_size=800, overlap=150):
    chunks=[]
    start_chunk = 0
    # menggunakan metode chunking slicing window
    while start_chunk <= len(text):
        end_chunk = start_chunk + chunk_size
        chunk = text[start_chunk:end_chunk]
        

        if chunk.strip():
            chunks.append(chunk)

        start_chunk += chunk_size - overlap
    return chunks


def add_dokumen_to_db(folder_path):
    documents = load_docum(folder_path)
    
    all_chunks = []
    all_ids = []
    all_metadatas = []

    chunk_counter=0
    for doc in documents:
        chunk = chunk_text(doc['content'])

        for i, chnk in  enumerate(chunk):
            all_chunks.append(chnk)
            all_ids.append(f"chunk_{chunk_counter}")
            all_metadatas.append({
                'source':doc['file_name'],
                'chunk_id':i
            })
            chunk_counter +=1
    collect.add(
        documents=all_chunks,
        ids=all_ids,
        metadatas=all_metadatas
    )
    

# mendapatkan nilai embedd dari kata yang diinputkan
def get_embedd(text):
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    embedd = response.data[0].embedding
    return embedd

"""cosine similary -> menghitung kemiripan dari 2 vector(termasuk space juga dihitung)
function ini berfungsi untuk menghitung kemiripan dari 2 vector menggunakan rumus cosine similarity"""
def cosine(vector1, vector2):
    # mengubah vector embedd(list->array) 
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    dot_product = np.dot(vector1, vector2)
    normaA = np.linalg.norm(vector1)
    normaB = np.linalg.norm(vector2)

    return dot_product/(normaA*normaB)

# print("Menilai kemiripan dari 2 kalimat ini:")
# text1 = "i love language python"
# text2 = "i love language javascript"
# emb1 = get_embedd(text1)
# emb2 = get_embedd(text2)
# print(f"text 1: {text1}")
# print(f"text 2: {text2}")
# sim = cosine(emb1, emb2)
# print(f"cosine similarity: {sim:.4f}")

if collect.count() == 0:
    print('Database kosong, manambah semua dokumen')
    add_dokumen_to_db('knowledge_base')

print('RAG CHATBOT')

history = [{
    'role': 'system', 
    'content': '''You are a professional and friendly customer service agent for this company. Answer in the language used by the user

HOW TO ANSWER:
1. Always greet with kindness and empathy.
2. Answer based on the context provided.
3. If information is not in context, politely state that you need to check further.
4. Provide clear, structured, and easy-to-understand answers.
5. Avoid using too many emojis. Only use relevant ones that convey emotion.
6. Always offer additional assistance at the end of your answer.
7. If there are numbers/dates/procedures, be specific.
8. IMPORTANT: Don't make up information. Only use what is in context.

LANGUAGE STYLE:
- Formal but friendly.
- End with a relevant follow-up question.

EXAMPLE:
"Thank you for your question! 😊
According to our company policy, [specific answer from context]...
Is there anything else I can help you with?'''
}]


while True:
    raw_query= input("You: ").strip()

    openrouter=OpenAI(
        base_url='https://openrouter.ai/api/v1',
        api_key=os.getenv('OPENROUTER_API_KEY')
        )
    prompt_enhancement = openrouter.chat.completions.create(
        model='openai/gpt-oss-20b:free',
        messages=[
            {'role':'system', 'content':'You are a user question translator. Translate user questions from any language into English and make them clearer and more detailed.'},
            {'role':'user', 'content':raw_query},
        ],
        max_tokens=150
    )
    query =  prompt_enhancement.choices[0].message.content
    

    if not query:
        continue

    # seacrh ke DB
    result = semantic_search(query, n_result=3)

    context = "\n".join([chunk['text'] for chunk in result])# list comprehension

    user_prompt = f"""Customer Question: {query}
Context from knowledge base:
{context}"""
    
    history.append({
        'role':'user',
        'content':user_prompt
    })
    
    answer = generate_answer(history)
    
    history[-1]= {'role':'user', 'content':query}
    history.append({
        'role':'assistant',
        'content':answer
    })

    print(f"AI: {answer}")
