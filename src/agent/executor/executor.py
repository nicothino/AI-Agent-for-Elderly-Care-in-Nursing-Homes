"""
Executor: ejecuta pasos generados por el planner (LLM calls, RAG, TTS, acciones externas)
- Este ejemplo muestra un loop simplificado que actúa según 'type'
"""

class Executor:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def execute(self, action, user_text, memory=None):
        if action == "chat":
            return self.chat(user_text, memory)
        elif action == "tell_joke":
            return "Aquí va un chiste malo: ¿Qué le dice un .txt a otro? ¡Te extraño!"
        elif action == "get_weather":
            return "El clima está soleado en este momento (simulado)."
        return "No entendí la instrucción."

    def chat(self, text, memory=None):
        messages = [{"role": "system", "content": "Eres un asistente cordial en español."}]
        if memory:
            messages.extend(memory)
        messages.append({"role": "user", "content": text})

        resp = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return resp.choices[0].message.content