from agent.base_agent import BaseAgent, register_agent
import requests

class WeatherAgent(BaseAgent):
    name = "weather_agent"
    description = "Consulta el clima actual usando la API gratuita wttr.in"

    def can_handle(self, intent: str) -> bool:
        # Intención relacionada con el clima
        return intent in ("weather", "clima", "temperatura")

    async def handle(self, text: str, context=None) -> str:
        """Consulta el clima con la API gratuita wttr.in"""
        try:
            # Puedes extraer ciudad del texto si quieres, por ahora fijo en Cali
            city = "Cali"
            url = f"https://wttr.in/{city}?format=j1"
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                return "No pude obtener el clima ahora mismo."
            data = res.json()
            current = data["current_condition"][0]
            temp = current["temp_C"]
            desc = current["weatherDesc"][0]["value"].lower()
            return f"En {city} hay {desc} y una temperatura de {temp}°C."
        except Exception as e:
            print(f"⚠️ Error WeatherAgent: {e}")
            return "No pude consultar el clima en este momento."

# Registrar agente
register_agent(WeatherAgent())
