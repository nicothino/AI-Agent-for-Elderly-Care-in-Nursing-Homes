import os
import json
import queue
import time
import requests
import tempfile
from dotenv import load_dotenv
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from playsound import playsound

# 🚀 Nuevo import de agentes
from agents import Agent, Runner

# ===================== CONFIG =====================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "j7XQZUnVCfhpa94EsaJS")
VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "models/vosk-model-es-0.42")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ Necesitas configurar OPENAI_API_KEY en .env")
if not ELEVEN_API_KEY:
    print("⚠️ No hay ELEVENLABS_API_KEY, no podrás oír la respuesta")

SAMPLE_RATE = 16000
CHANNELS = 1

# ===================== AUDIO CAPTURE =====================
q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    q.put(bytes(indata))

# ===================== STT (VOSK) =====================
print("🎙️ Cargando modelo VOSK...")
model = Model(VOSK_MODEL_PATH)
rec = KaldiRecognizer(model, SAMPLE_RATE)

def recognize_once(duration=5):
    """Graba durante X segundos y devuelve texto reconocido"""
    print("🎙️ Habla ahora...")

    def get_default_input_device():
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                return idx
        raise RuntimeError("❌ No se encontró ningún micrófono válido")

    input_device = get_default_input_device()

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype='int16',
        channels=CHANNELS,
        callback=audio_callback,
        device=input_device
    ):
        buffer = b""
        start_time = time.time()
        while True:
            frame = q.get()
            buffer += frame
            if time.time() - start_time > duration:
                break

    if rec.AcceptWaveform(buffer):
        res = json.loads(rec.Result())
    else:
        res = json.loads(rec.FinalResult())
    text = res.get("text", "").strip()
    return text

# ===================== AGENT (OpenAI-Agents) =====================
voice_agent = Agent(
    name="NicoBot",
    instructions="Eres un asistente de voz cordial que responde en español de manera breve y clara."
)

async def generate_text(prompt):
    result = await Runner.run(voice_agent, prompt)
    return result.final_output

# ===================== TTS (ElevenLabs) =====================
def eleven_tts(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {"text": text, "model_id": "eleven_monolingual_v1"}
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    if r.status_code == 200:
        return r.content
    else:
        print("❌ Error ElevenLabs:", r.text)
        return None

def play_audio(mp3_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        f.write(mp3_bytes)
        fname = f.name
    playsound(fname)

# ===================== LOOP =====================
import asyncio

async def main():
    print("🤖 Asistente de voz listo (Ctrl+C para salir).")
    while True:
        text = recognize_once(duration=5)
        if not text:
            print("… No entendí nada, intenta de nuevo.")
            continue
        print("📝 Usuario:", text)

        answer = await generate_text(text)
        print("🤖 Asistente:", answer)

        if ELEVEN_API_KEY:
            mp3 = eleven_tts(answer)
            if mp3:
                play_audio(mp3)

if __name__ == "__main__":
    asyncio.run(main())
