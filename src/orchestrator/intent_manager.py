"""
Clasifica la intención del usuario.
Puede ampliarse con modelos o embeddings.
"""
import re

INTENT_KEYWORDS = {
    "websearch": ["buscar", "investiga", "qué es", "quién es", "dónde queda", "información sobre", "cuándo fue"],
    "weather": ["clima", "tiempo", "va a llover", "temperatura", "frío", "calor"],
    "empathy": ["me siento", "estoy triste", "solo", "feliz", "contento"],
}


def detect_intent(text: str) -> str:
    text = text.lower()
    for intent, kws in INTENT_KEYWORDS.items():
        if any(kw in text for kw in kws):
            return intent
    return "empathy"  # fallback por defecto
