import sounddevice as sd
import soundfile as sf

duration = 5  # segundos
sample_rate = 16000

print("🎙️ Grabando 5 segundos...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16', device=0)
sd.wait()  # espera a que termine
sf.write("test.wav", audio, sample_rate)
print("✅ Grabación terminada. Archivo guardado como test.wav")