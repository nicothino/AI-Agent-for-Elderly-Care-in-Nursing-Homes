import os, requests, tempfile
from playsound import playsound
from dotenv import load_dotenv

load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "j7XQZUnVCfhpa94EsaJS")

def eleven_tts(text):
    """Convierte texto en audio usando ElevenLabs."""
    if not ELEVEN_API_KEY:
        print("⚠️ Falta ELEVENLABS_API_KEY")
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {"text": text, "model_id": "eleven_monolingual_v1"}
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    return r.content if r.status_code == 200 else None

def play_audio(mp3_bytes):
    """Reproduce audio temporalmente."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        f.write(mp3_bytes)
        name = f.name
    playsound(name)
