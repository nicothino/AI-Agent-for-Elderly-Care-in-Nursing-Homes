"""
Orquestador modular — decide qué agente manejará cada entrada.
"""
import time, uuid, asyncio
from typing import Any, Dict
from agent.base_agent import get_agent_for_intent
from orchestrator.intent_manager import detect_intent

class Orchestrator:
    def __init__(self):
        self.turns = []

    async def handle_text(self, text: str) -> str:
        start = time.perf_counter()
        intent = detect_intent(text)
        agent = get_agent_for_intent(intent)

        if not agent:
            return "No tengo un agente que pueda responder eso aún."

        try:
            response = await agent.handle(text)
        except Exception as e:
            print(f"⚠️ Error en agente {agent.name}: {e}")
            response = "Tuve un problema al procesar eso."

        self.turns.append({
            "id": str(uuid.uuid4()),
            "ts": time.time(),
            "user_text": text,
            "intent": intent,
            "agent": agent.name,
            "response": response,
            "latency_ms": int((time.perf_counter() - start) * 1000)
        })

        return response
