from agent.base_agent import BaseAgent, register_agent
from dataclasses import dataclass
from typing import Literal, Optional, Dict, Any
import requests

# ======================================================
# TOOL: WebSearchTool (búsqueda web genérica)
# ======================================================

@dataclass
class WebSearchTool:
    """
    Herramienta que realiza una búsqueda web genérica.
    Usa una API gratuita (DuckDuckGo JSON) o cualquier backend.
    """
    user_location: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    search_context_size: Literal["low", "medium", "high"] = "medium"

    def search(self, query: str) -> str:
        """
        Busca en la web y devuelve un resumen textual.
        Actualmente usa la API pública de DuckDuckGo.
        """
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json&lang=es"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return "No pude realizar la búsqueda web en este momento."
            data = r.json()
            abstract = data.get("AbstractText")
            related = data.get("RelatedTopics", [])
            if abstract:
                return abstract
            elif related:
                # Tomamos el primer resultado relacionado
                first = related[0].get("Text", "")
                return first or "No encontré un resumen claro en la web."
            else:
                return "No encontré resultados útiles en Internet."
        except Exception as e:
            print(f"⚠️ Error en WebSearchTool: {e}")
            return "Hubo un error al hacer la búsqueda."

# ======================================================
# AGENTE: WebSearchAgent
# ======================================================

class WebSearchAgent(BaseAgent):
    """
    Agente que utiliza el WebSearchTool para obtener información factual.
    """
    name = "websearch_agent"
    description = "Busca información factual o noticias recientes en la web."

    def __init__(self):
        self.tool = WebSearchTool(search_context_size="medium")

    def can_handle(self, intent: str) -> bool:
        return intent in ("websearch", "wikipedia", "info", "search")

    async def handle(self, text: str, context=None) -> str:
        """Usa el WebSearchTool para buscar información."""
        print(f"🌐 [WebSearchAgent] Buscando: {text}")
        result = self.tool.search(text)
        return result

# Registrar automáticamente
register_agent(WebSearchAgent())
