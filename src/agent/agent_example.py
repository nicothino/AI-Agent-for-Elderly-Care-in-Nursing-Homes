# src/agent/reminder_agent.py
from agent.base_agent import BaseAgent, register_agent
class ReminderAgent(BaseAgent):
    name = "reminder_agent"
    description = "Crea recordatorios simples"
    def can_handle(self, intent): return intent == "reminder"
    async def handle(self, text, context=None):
        return "Ok, crearé un recordatorio para eso."
register_agent(ReminderAgent())
