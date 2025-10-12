from agent.base_agent import BaseAgent, register_agent
import requests, os
from dotenv import load_dotenv
load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherAgent(BaseAgent):
    name = "weather_agent"
    description = "Consulta el clima actual"

    def can_handle(self, intent: str) -> bool:
        return intent == "weather"

    async def handle(self, text: str, context=None) -> str:
        """Consulta OpenWeather y responde brevemente."""
        if not OPENWEATHER_KEY:
            return "No tengo configurada la API del clima."

        city = "Cali"  # Puedes extraer de perfil o NLP
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric&lang=es"
        r = requests.get(url)
        if r.status_code != 200:
            return "No pude obtener el clima ahora."
        data = r.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"En {city} hay {desc} y {temp} grados."

# Registrar agente
register_agent(WeatherAgent())
