import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "nicolas_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "nicolas_db")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async def get_db_pool():
    """Crea un pool de conexiones asíncronas a PostgreSQL."""
    return await asyncpg.create_pool(DATABASE_URL)
