"""
Definición base de Agentes y registro global
Cada agente debe heredar de BaseAgent y registrar su nombre e intención.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

# ============================================================
# Base Agent
# ============================================================

class BaseAgent(ABC):
    """Clase base que todos los agentes deben heredar."""
    name: str
    description: str

    @abstractmethod
    async def handle(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Debe devolver una respuesta textual."""
        pass

    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        """Define si este agente puede manejar una intención específica."""
        pass

# ============================================================
# Registro global de agentes
# ============================================================

AGENT_REGISTRY: Dict[str, BaseAgent] = {}

def register_agent(agent: BaseAgent):
    """Registra agentes en el sistema."""
    AGENT_REGISTRY[agent.name] = agent

def get_agent_for_intent(intent: str) -> Optional[BaseAgent]:
    """Devuelve el agente que puede manejar una intención."""
    for agent in AGENT_REGISTRY.values():
        if agent.can_handle(intent):
            return agent
    return None
