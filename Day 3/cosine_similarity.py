from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# mendapatkan nilai embedd dari kata yang diinputkan
def get_embedd(text):
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )

    embedd = response.data[0].embedding
    return embedd

# cosine similary -> menghitung kemiripan dari 2 vector(termasuk space juga dihitung)
# function ini berfungsi untuk menghitung kemiripan dari 2 vector menggunakan rumus cosine similarity
def cosine(vector1, vector2):
    # mengubah vector embedd(list->array) 
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    dot_product = np.dot(vector1, vector2)
    normaA = np.linalg.norm(vector1)
    normaB = np.linalg.norm(vector2)

    return dot_product/(normaA*normaB)

print("Menilai kemiripan dari 2 kalimat ini:")
text1 = "i love language python"
text2 = "i love language javascript"
emb1 = get_embedd(text1)
emb2 = get_embedd(text2)
print(f"text 1: {text1}")
print(f"text 2: {text2}")
sim = cosine(emb1, emb2)
print(f"cosine similarity: {sim:.4f}")
