from agent.base_agent import BaseAgent, register_agent
from agents import Agent, Runner

class EmpathyAgent(BaseAgent):
    name = "empathy_agent"
    description = "Charla social y apoyo emocional"

    def can_handle(self, intent: str) -> bool:
        return intent in ("empathy", "social", "default")

    async def handle(self, text: str, context=None) -> str:
        """Responde con tono empático usando OpenAI Agents SDK."""
        voice_agent = Agent(
            name="Apolo",
            instructions="Responde en español, de forma cálida, empática y breve."
        )
        result = await Runner.run(voice_agent, text)
        return result.final_output

# Registrar al cargar
register_agent(EmpathyAgent())

