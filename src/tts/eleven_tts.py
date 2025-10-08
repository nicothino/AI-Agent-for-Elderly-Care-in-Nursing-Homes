"""
ElevenLabs TTS helper (template)
- Convierte texto a mp3 y guarda en cache
"""
import os, requests, tempfile
from playsound import playsound

class ElevenTTS:
    def __init__(self, api_key, voice_id="JBFqnCBsd6RMkjVDRZzb"):
        self.api_key = api_key
        self.voice_id = voice_id

    def synthesize(self, text):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        payload = {"text": text, "model_id": "eleven_monolingual_v1"}
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.content
        else:
            raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text}")

    def play(self, audio_bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            fname = f.name
        playsound(fname)
