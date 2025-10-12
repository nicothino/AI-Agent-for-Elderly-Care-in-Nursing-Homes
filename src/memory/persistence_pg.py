import asyncpg
from typing import Dict, Any

class PersistencePG:
    """Guarda turnos, resúmenes diarios y alertas en PostgreSQL."""
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def save_turn(self, turn: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO conversation_turns (ts, user_text, intent, result_text)
            VALUES (NOW(), $1, $2, $3);
            """, turn["user"], turn["intent"], turn["assistant"])

    async def save_daily_summary(self, summary: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO daily_summaries (date, emotions, needs, complaints, recommendations)
            VALUES (CURRENT_DATE, $1, $2, $3, $4)
            ON CONFLICT (date) DO UPDATE
            SET emotions=$1, needs=$2, complaints=$3, recommendations=$4;
            """, summary["emotions"], summary["needs"], summary["complaints"], summary["recommendations"])
