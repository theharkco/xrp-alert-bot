FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY src/__init__.py ./src/__init__.py 2>/dev/null || true
COPY include/ ./include/ 2>/dev/null || true
COPY lib/ ./lib/ 2>/dev/null || true

EXPOSE 8000

CMD ["python3", "-c", "from src.api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"]