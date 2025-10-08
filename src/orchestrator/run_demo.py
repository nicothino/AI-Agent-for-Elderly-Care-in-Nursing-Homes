"""
Orquestador demo: captura una frase con VOSK y ejecuta planner->executor->tts
Es un demo muy simple para validar integración local.
"""
import os, asyncio
from dotenv import load_dotenv
from src.stt.vosk_stt import VoskSTT
from src.tts.eleven_tts import ElevenTTS
from src.memory.memory import ShortTermMemory
from src.agent.planner import Planner
from src.agent.executor import Executor

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

stt = VoskSTT()
tts = ElevenTTS(ELEVEN_API_KEY)
memory = ShortTermMemory()
planner = Planner()
executor = Executor(OPENAI_API_KEY)

async def main():
    print("🎙️ Asistente modular listo. Habla...")
    while True:
        text = stt.listen_once(duration=6)
        if not text:
            continue
        print("📝 Usuario:", text)

        memory.add("user", text)
        action = planner.decide(text)
        answer = executor.execute(action, text, memory.get())
        print("🤖 Asistente:", answer)

        memory.add("assistant", answer)
        audio = tts.synthesize(answer)
        tts.play(audio)

if __name__ == "__main__":
    asyncio.run(main())
