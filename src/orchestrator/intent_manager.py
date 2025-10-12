"""
Clasifica la intención del usuario.
Puede ampliarse con modelos o embeddings.
"""
import re

INTENT_KEYWORDS = {
    "weather": ["clima", "tiempo", "temperatura", "va a llover"],
    "empathy": ["me siento", "estoy triste", "solo", "feliz", "emocionado"],
}

def detect_intent(text: str) -> str:
    text = text.lower()
    for intent, kws in INTENT_KEYWORDS.items():
        if any(kw in text for kw in kws):
            return intent
    return "empathy"  # fallback por defecto
