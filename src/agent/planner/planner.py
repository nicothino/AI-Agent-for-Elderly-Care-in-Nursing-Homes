"""
Planner: recibe un objetivo/consulta y genera pasos/subtareas.
- En este starter, el planner se limita a dividir una pregunta compleja
  en pasos y decidir si necesita RAG o una acción.
"""
class Planner:
    def __init__(self):
        pass

    def decide(self, text):
        # lógica básica → luego lo mejoras
        if "clima" in text.lower():
            return "get_weather"
        elif "chiste" in text.lower():
            return "tell_joke"
        return "chat"