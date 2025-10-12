import asyncio
from stt.vosk_stt import recognize_once
from tts.eleven_tts import eleven_tts, play_audio
from orchestrator.core_orchestrator import Orchestrator
import agent.empathy_agent  # registra agentes
import agent.weather_agent

async def main():
    orch = Orchestrator()
    print("🤖 Asistente modular listo (Ctrl+C para salir).")

    while True:
        text = recognize_once(duration=5)
        if not text:
            print("… No entendí nada, intenta de nuevo.")
            continue

        print("📝 Usuario:", text)
        answer = await orch.handle_text(text)
        print("🤖 Asistente:", answer)

        mp3 = eleven_tts(answer)
        if mp3:
            play_audio(mp3)

if __name__ == "__main__":
    asyncio.run(main())
