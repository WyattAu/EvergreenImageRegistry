# =============================================================================
# SOVEREIGN HARDENED MAILU
# Constraint: debian-slim - Python runtime required
# =============================================================================

ARG VERSION=2.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         python3="3.11.*"         python3-pip="23.1.*"         python3-venv="3.11.*"         curl="7.88.1-*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir mailu==2.0.0

FROM debian:bookworm-slim
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends         python3="3.11.*"         ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN groupadd -r -g 65534 appuser && useradd -r -u 65534 -g appuser -d /app -s /usr/sbin/nologin appuser
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /app /var/log/mailu /var/cache/mailu /data && chown -R 65534:65534 /app /var/log/mailu /var/cache/mailu /data
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["python3", "-c", "import mailu; print(1)"]
ENTRYPOINT [["python3", "-m", "mailu"]]
LABEL org.opencontainers.image.title="mailu"       org.opencontainers.image.description="Mailu - self-hosted email server suite"       org.opencontainers.image.version="2.0.0"       org.opencontainers.image.vendor="Mailu"       org.opencontainers.image.source="https://github.com/Mailu/Mailu"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian-slim="true"
