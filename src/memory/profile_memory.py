
import json, os

class ProfileMemory:
    """Carga el perfil del usuario (edad, gustos, condiciones, etc.)."""
    def __init__(self, path="data/profile.json"):
        if not os.path.exists(path):
            raise FileNotFoundError("❌ No se encontró el archivo de perfil del residente.")
        with open(path, "r", encoding="utf-8") as f:
            self.profile = json.load(f)

    def get_profile(self):
        return self.profile
