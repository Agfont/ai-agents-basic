FROM python:3.14-slim AS builder

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY tutorial-api/requirements.txt /tmp/requirements-api.txt
COPY tutorial-api/requirements-labs.txt /tmp/requirements-labs.txt

RUN python -m venv "$VIRTUAL_ENV"
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements-api.txt -r /tmp/requirements-labs.txt

FROM python:3.14-slim AS runtime

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser
RUN mkdir -p /app/techcorp-docs

COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
COPY --chown=appuser:appuser tutorial-api /app/tutorial-api
COPY --chown=appuser:appuser 1-ai-api-call /app/1-ai-api-call
COPY --chown=appuser:appuser 2-langchain /app/2-langchain
COPY --chown=appuser:appuser 3-prompt-engineering /app/3-prompt-engineering
COPY --chown=appuser:appuser 4-vector-databases /app/4-vector-databases
COPY --chown=appuser:appuser 5-rag /app/5-rag
COPY --chown=appuser:appuser 6-langgraph /app/6-langgraph
COPY --chown=appuser:appuser 7-mcp /app/7-mcp

USER appuser

EXPOSE 5050

CMD ["/opt/venv/bin/python", "tutorial-api/app.py"]
