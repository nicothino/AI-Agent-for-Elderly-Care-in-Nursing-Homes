"""
Vector store adapter (pgvector example placeholder)
- Este archivo contiene funciones de ejemplo para upsert + query de vectores.
- En producción adapta a pinecone/weaviate/pgvector client real.
"""
from sqlalchemy import create_engine, text
import os
import json

VECTOR_DB_URL = os.getenv("VECTOR_DB_URL")  # e.g. postgresql://user:pass@host:5432/db

def connect():
    if not VECTOR_DB_URL:
        raise RuntimeError("VECTOR_DB_URL no está configurada en env")
    engine = create_engine(VECTOR_DB_URL)
    return engine
