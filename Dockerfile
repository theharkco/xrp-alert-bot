FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY src/__init__.py ./src/__init__.py 2>/dev/null || true

EXPOSE 8000

RUN echo '#!/bin/sh\nexec python3 /app/src/server.py' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]