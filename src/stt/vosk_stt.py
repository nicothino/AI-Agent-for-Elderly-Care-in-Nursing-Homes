import os, json, queue, time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

load_dotenv()

SAMPLE_RATE = 16000
CHANNELS = 1
q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    q.put(bytes(indata))

# ✅ Ruta absoluta del modelo VOSK
def get_model_path():
    env_path = os.getenv("VOSK_MODEL_PATH", "models/vosk-model-small-es-0.42")
    model_path = os.path.abspath(env_path)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ No se encontró el modelo VOSK en: {model_path}")
    return model_path

def recognize_once(duration=5):
    """Graba durante X segundos y devuelve texto reconocido."""
    model_path = get_model_path()
    print(f"🧠 Cargando modelo VOSK desde: {model_path}")
    model = Model(model_path)
    rec = KaldiRecognizer(model, SAMPLE_RATE)

    print("🎙️ Habla ahora...")
    with sd.RawInputStream(samplerate=SAMPLE_RATE, dtype='int16', channels=CHANNELS, callback=audio_callback):
        buffer = b""
        start_time = time.time()
        while time.time() - start_time < duration:
            buffer += q.get()

    if rec.AcceptWaveform(buffer):
        res = json.loads(rec.Result())
    else:
        res = json.loads(rec.FinalResult())

    text = res.get("text", "").strip()
    return text
