"""
VOSK STT helper (template)
- Captura audio del mic (sounddevice)
- Usa webrtcvad para VAD
- Usa VOSK para transcribir chunks
"""
import queue, json, sounddevice as sd
from vosk import Model, KaldiRecognizer

class VoskSTT:
    def __init__(self, model_path="models/vosk-model-es", sample_rate=16000):
        self.q = queue.Queue()
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate

    def _callback(self, indata, frames, time_info, status):
        self.q.put(bytes(indata))

    def listen_once(self, duration=5, device=None):
        with sd.RawInputStream(samplerate=self.sample_rate,
                               blocksize=8000,
                               dtype='int16',
                               channels=1,
                               callback=self._callback,
                               device=device):
            buffer = b""
            while len(buffer) < duration * self.sample_rate * 2:
                buffer += self.q.get()

        if self.rec.AcceptWaveform(buffer):
            return json.loads(self.rec.Result()).get("text", "")
        return json.loads(self.rec.FinalResult()).get("text", "")
