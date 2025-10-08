# VOSK + OpenAI + ElevenLabs Agent (starter)

Proyecto inicial para un **agente de voz** con arquitectura _planner → executor_ + **RAG** + **memory**.
Este repo contiene una estructura de carpetas y archivos de ejemplo para arrancar desarrollo con:
- **VOSK**: STT offline (local)
- **OpenAI**: embeddings + chat (RAG)
- **ElevenLabs**: Text-to-Speech (TTS)
- Orquestador local que conecta todo
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/aa55fdb5-6029-4118-ba17-2269688b3946" />

## Arquitectura (resumida)
Device (speakerphone USB) → STT (VOSK, local) → Orquestador/Router (planner) → RAG (OpenAI embeddings + vector DB) → LLM (OpenAI Chat) → Executor (acciones, herramientas) → TTS (ElevenLabs) → Output (USB speaker).
Se añaden capas de memory (short-term summaries, long-term embeddings) y caché de TTS.

## Estructura creada
- src/stt: integración VOSK (mic capture, VAD)
- src/tts: integración ElevenLabs (sintetizar y cachear audios)
- src/orchestrator: orquestador principal, loop de turnos
- src/rag: embeddings + conectores a vector DB (pgvector/Pinecone)
- src/memory: abstracción para short/long term memory (embeddings + summaries)
- src/agent: planner y executor (planner -> genera sub-tareas, executor las ejecuta)
- scripts/: utilidades para desarrollo y pruebas
- docker/: Dockerfile de ejemplo
- tests/: tests básicos de estructura

## Cómo usar (rápido)
1. Crear un virtualenv:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Configurar variables de entorno en `.env` (usa `.env.example`):
- OPENAI_API_KEY
- ELEVENLABS_API_KEY
- VECTOR_DB_URL (opcional: postgres/pinecone)

3. Ejecutar demo local (placeholder):
```bash
python src/orchestrator/run_demo.py
```

> Este repo es un *starter*. Los módulos contienen plantillas y ejemplos mínimos; hay que completar lógica de producción, manejo de errores, y seguridad para desplegar.

