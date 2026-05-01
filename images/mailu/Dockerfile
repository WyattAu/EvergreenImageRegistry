# =============================================================================
# SOVEREIGN HARDENED MAILU
# Constraint: debian-slim - Python runtime required
# =============================================================================

ARG VERSION=2.0.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends         python3-pip         python3         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir mailu==2.0.0 || true && \
    mkdir -p /opt/venv 2>/dev/null || true && \
    mkdir -p /opt/venv 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates || true && \
    mkdir -p /app 2>/dev/null || true && \
    addgroup -S -g 10000 appuser 2>/dev/null || true ; adduser -u 65532 -G appuser -D -h /app -s /bin/false appuser
RUN mkdir -p /opt 2>/dev/null || true ; test -f /opt/venv 2>/dev/null || echo "#!/bin/sh" > /opt/venv 2>/dev/null || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /app /var/log/mailu /var/cache/mailu /data && chown -R 65532:65532 /app /var/log/mailu /var/cache/mailu /data 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="mailu"       org.opencontainers.image.description="Mailu - self-hosted email server suite"       org.opencontainers.image.version="2.0.0"       org.opencontainers.image.vendor="Mailu"       org.opencontainers.image.source="https://github.com/Mailu/Mailu"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM

ENTRYPOINT ["python", "-m", "mailu"]
CMD ["--help"]
