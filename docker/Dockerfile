# ─────────────────────────────────────────────
# 🧠 Dockerfile para el Asistente Nicolás
# ─────────────────────────────────────────────

# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo
WORKDIR /app

# Copia los requerimientos
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto (puedes ignorar cosas en .dockerignore)
COPY . .

# Variables de entorno por defecto
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Comando por defecto (ejecuta tu main.py)
CMD ["python", "src/main.py"]
