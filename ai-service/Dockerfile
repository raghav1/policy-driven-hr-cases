FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FASTEMBED_CACHE_PATH=/models

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bake the embedding and reranking models into the image so startup needs no download.
COPY app/__init__.py app/config.py app/models_preload.py app/
RUN python -m app.models_preload

COPY . .

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 agent && chown -R agent /srv /models
USER agent

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
