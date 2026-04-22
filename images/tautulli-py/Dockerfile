ARG VERSION=2.14.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir pyopenssl certifi && \
    git clone --depth 1 --branch v2.14.5 \
    "https://github.com/Tautulli/Tautulli.git" /opt/tautulli

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/tautulli /opt/tautulli
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/tautulli /var/cache/tautulli \
    && chown -R 65534:65534 /app /var/log/tautulli /var/cache/tautulli /opt/tautulli
USER 65534:65534
WORKDIR /app
EXPOSE 8181
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8181/status"]
ENTRYPOINT ["python3", "/opt/tautulli/Tautulli.py"]
LABEL org.opencontainers.image.title="tautulli-py" \
      org.opencontainers.image.version="2.14.5" \
      org.opencontainers.image.vendor="Tautulli" \
      org.opencontainers.image.source="https://github.com/Tautulli/Tautulli" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
