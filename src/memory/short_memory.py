from collections import deque
from typing import Dict, List

class ShortMemory:
    """Guarda los últimos N turnos de conversación en RAM."""
    def __init__(self, max_turns: int = 8):
        self.buffer = deque(maxlen=max_turns)

    def add_turn(self, user_text: str, assistant_text: str, intent: str):
        self.buffer.append({
            "user": user_text,
            "assistant": assistant_text,
            "intent": intent
        })

    def get_context(self, n: int = 5) -> List[Dict]:
        """Devuelve los últimos N turnos para mantener contexto."""
        return list(self.buffer)[-n:]

    def clear(self):
        self.buffer.clear()
