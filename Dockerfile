FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY src/__init__.py ./src/__init__.py 2>/dev/null || true

EXPOSE 8000

# Create a simple shell script that starts uvicorn and keeps the container running
RUN echo '#!/bin/bash\npython3 -m uvicorn src.api:app --host 0.0.0.0 --port 8000' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]