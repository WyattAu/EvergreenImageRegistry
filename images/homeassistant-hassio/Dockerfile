
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir homeassistant || true
RUN mkdir -p /config /data /app 2>/dev/null || true


RUN mkdir -p /opt/venv ; \
USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

ENTRYPOINT ["python", "-m", "homeassistant"]
CMD ["--help"]
