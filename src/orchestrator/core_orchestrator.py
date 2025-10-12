"""
Orquestador modular — decide qué agente manejará cada entrada.
"""
import asyncio, time, uuid
from typing import Dict, Any
from agent.base_agent import get_agent_for_intent
from orchestrator.intent_manager import detect_intent
from memory.short_memory import ShortMemory
from memory.long_memory_pg import LongMemoryPG
from memory.profile_memory import ProfileMemory
from memory.persistence_pg import PersistencePG

class Orchestrator:
    """
    Orquestador central del asistente Nicolás:
    - Clasifica intención
    - Enruta a agentes
    - Maneja memoria (perfil, corta, larga)
    - Persiste datos en PostgreSQL
    """
    def __init__(self, pool):
        # Componentes base
        self.short_memory = ShortMemory(max_turns=8)
        self.long_memory = LongMemoryPG(pool)
        self.persistence = PersistencePG(pool)
        self.profile_memory = ProfileMemory("data/profile.json")

    async def handle_text(self, user_text: str) -> str:
        """Procesa el texto del usuario y devuelve la respuesta del agente."""
        start = time.perf_counter()
        intent = detect_intent(user_text)
        agent = get_agent_for_intent(intent)

        if not agent:
            return "No tengo un agente que pueda responder eso aún."

        # Construir contexto para agentes sociales
        context = {
            "profile": self.profile_memory.get_profile(),
            "short_memory": self.short_memory.get_context(5)
        }

        # Ejecutar agente
        try:
            result = await agent.handle(user_text, context=context)
        except Exception as e:
            print(f"⚠️ Error en agente {agent.name}: {e}")
            result = "Tuve un problema al procesar eso."

        latency = int((time.perf_counter() - start) * 1000)

        # Actualizar memoria corta
        self.short_memory.add_turn(user_text, result, intent)

        # Guardar turno en Postgres
        await self.persistence.save_turn({
            "user": user_text,
            "assistant": result,
            "intent": intent,
            "latency": latency
        })

        return result
