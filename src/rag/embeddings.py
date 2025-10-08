"""
Embeddings helper (OpenAI)
- Genera embedding usando text-embedding-3-small
"""
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-3-small"):
    resp = openai.Embedding.create(model=model, input=text)
    return resp["data"][0]["embedding"]
