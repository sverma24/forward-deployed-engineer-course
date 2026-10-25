# The outage desk, packaged to run on Larkfield's own server (chapter C20).
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY outage-desk/ outage-desk/
COPY client-handover/ client-handover/
WORKDIR /app/outage-desk
# Build the clean database and the policy index inside the image.
RUN uv run --no-dev python -m outage_desk.clean && uv run --no-dev python -m outage_desk.docs build
ENV MODEL_BACKEND=ollama DATA_DIR=/app/outage-desk/data
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uv", "run", "--no-dev", "uvicorn", "outage_desk.service:app", "--host", "0.0.0.0", "--port", "8000"]
