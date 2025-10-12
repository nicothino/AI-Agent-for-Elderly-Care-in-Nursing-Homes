import openai, os, json, asyncpg
from datetime import date
from dotenv import load_dotenv
from utils.settings import get_db_pool
from openai import AsyncOpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI()

async def run_daily_summary():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # 1️⃣ Extraer las conversaciones del día
        rows = await conn.fetch("""
        SELECT user_text, assistant, intent
        FROM conversation_turns
        WHERE DATE(ts) = CURRENT_DATE;
        """)
        if not rows:
            print("📭 No hay conversaciones hoy.")
            return

        text_log = "\n".join([f"U: {r['user_text']}\nA: {r['assistant']}" for r in rows])

        # 2️⃣ Pedir resumen al modelo
        prompt = f"""
        Analiza las siguientes conversaciones y devuelve un JSON con:
        - emotions: joy, sadness, anxiety, loneliness, valence_avg (0-1)
        - needs: lista de necesidades expresadas
        - complaints: quejas o malestares
        - recommendations: sugerencias para cuidadores
        Conversación del día:
        {text_log}
        """

        resp = await client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            response_format={"type": "json_object"}
        )
        data = json.loads(resp.output[0].content[0].text)

        # 3️⃣ Guardar resumen en daily_summaries
        await conn.execute("""
        INSERT INTO daily_summaries (date, emotions, needs, complaints, recommendations)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (date) DO UPDATE
        SET emotions=$2, needs=$3, complaints=$4, recommendations=$5;
        """, date.today(), json.dumps(data["emotions"]), json.dumps(data["needs"]),
           json.dumps(data["complaints"]), json.dumps(data["recommendations"]))

        print("✅ Resumen emocional del día guardado.")

        # 4️⃣ (opcional) Insertar en memoria larga (episódico)
        embedding_resp = await client.embeddings.create(
            model="text-embedding-3-small",
            input=json.dumps(data)
        )
        emb = embedding_resp.data[0].embedding
        await conn.execute("""
        INSERT INTO memory_chunks (kind, content, embedding, meta)
        VALUES ('episodic', $1, $2, '{"source":"daily_summary"}');
        """, json.dumps(data), emb)

        print("🧠 Episodio agregado a memoria larga.")
