# Dockerfile de ejemplo (no optimizado)
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
CMD ["python", "src/orchestrator/run_demo.py"]
