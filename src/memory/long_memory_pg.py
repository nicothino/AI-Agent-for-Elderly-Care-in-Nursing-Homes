import asyncpg
from typing import List, Dict, Any

class LongMemoryPG:
    """Memoria semántica a largo plazo (usa pgvector en Postgres)."""
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def add_chunk(self, kind: str, content: str, embedding: List[float], meta: Dict[str, Any]):
        query = """
        INSERT INTO memory_chunks (kind, content, embedding, meta)
        VALUES ($1, $2, $3, $4);
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, kind, content, embedding, meta)

    async def search_chunks(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        query = """
        SELECT id, kind, content, meta
        FROM memory_chunks
        ORDER BY embedding <-> $1
        LIMIT $2;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, query_embedding, top_k)
            return [dict(r) for r in rows]
