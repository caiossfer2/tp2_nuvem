ARG PYTHON_VERSION=3.13.1
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY playlist_rules_generator.py .
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

RUN chmod -R a+w /app

RUN mkdir -p /app/model && chmod -R 777 /app/model

USER appuser

EXPOSE 8000

CMD ["python", "playlist_rules_generator.py"]

