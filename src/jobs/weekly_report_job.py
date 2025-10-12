import asyncpg, json
from datetime import date, timedelta
from utils.settings import get_db_pool

async def run_weekly_report():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
        SELECT emotions FROM daily_summaries
        WHERE date >= CURRENT_DATE - INTERVAL '7 days';
        """)
        if not rows:
            print("📭 No hay datos para el reporte semanal.")
            return

        # Promediar valores
        sums = {"joy":0,"sadness":0,"anxiety":0,"loneliness":0,"valence_avg":0}
        for r in rows:
            emo = json.loads(r["emotions"])
            for k in sums: sums[k] += emo.get(k, 0)
        avg = {k: round(v / len(rows), 2) for k, v in sums.items()}

        await conn.execute("""
        INSERT INTO weekly_reports (week_start, emotions_avg)
        VALUES ($1, $2)
        ON CONFLICT (week_start) DO UPDATE SET emotions_avg=$2;
        """, date.today() - timedelta(days=7), json.dumps(avg))

        print("📊 Reporte semanal actualizado:", avg)
