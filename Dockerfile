# syntax=docker/dockerfile:1

# A one-shot image. It does not start a server or a worker: the server's cron
# runs it with a job name, the job runs, the container exits. Nothing is held
# open between runs.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" --uid 10001 alltech \
    && chown -R alltech:alltech /app
USER alltech

# No default job on purpose: running this image with no arguments should do
# nothing rather than guess which report to send.
ENTRYPOINT ["python", "manage.py"]
