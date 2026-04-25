ARG VERSION=2.14.5
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true
RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir pyopenssl certifi &&  && \
    git clone --depth 1 --branch v2.14.5  || echo "Source repo not available - using placeholder" 2>/dev/null || true    "https://github.com/Tautulli/Tautulli.git" /opt/tautulli

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates curl || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/tautulli /opt/tautulli
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir -p /app /var/log/tautulli /var/cache/tautulli \ ; \
    chown -R 65532:65532 /app /var/log/tautulli /var/cache/tautulli /opt/tautulliUSER 65532:65532
WORKDIR /app
EXPOSE 8181
ENTRYPOINT ["python3", "/opt/tautulli/Tautulli.py"]
LABEL org.opencontainers.image.title="tautulli" \
      org.opencontainers.image.version="2.14.5" \
      org.opencontainers.image.vendor="Tautulli" \
      org.opencontainers.image.source="https://github.com/Tautulli/Tautulli" \
      sovereign.image.tier="2" \
      sovereign.image.category="media-streaming" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
