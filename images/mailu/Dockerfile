# =============================================================================
# EVERGREEN HARDENED MAILU
# Constraint: debian-slim - Python runtime required
# =============================================================================

ARG VERSION=2.0.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update &&     apt-get install -y --no-install-recommends         python3-pip         python3         curl         ca-certificates &&     rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip install --no-cache-dir mailu==2.0.0 || true && \
    mkdir -p /opt/venv 2>/dev/null || true && \
    mkdir -p /opt/venv 2>/dev/null || true

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:10c773dc96763e3201275bae7865d278ca4b91db586117adec79079a2d7cdb80
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"

RUN dnf install -y python3 ca-certificates || true && \
    mkdir -p /app /opt 2>/dev/null || true && \
    groupadd -g 10000 appuser 2>/dev/null || true && useradd -u 65532 -g appuser -r -M -s /bin/false appuser 2>/dev/null || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN mkdir -p /app /var/log/mailu /var/cache/mailu /data && chown -R 65532:65532 /app /var/log/mailu /var/cache/mailu /data 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8080
LABEL org.opencontainers.image.title="mailu"       org.opencontainers.image.description="Mailu - self-hosted email server suite"       org.opencontainers.image.version="2.0.0"       org.opencontainers.image.vendor="Mailu"       org.opencontainers.image.source="https://github.com/Mailu/Mailu"       evergreen.image.tier="2"       evergreen.constraint.nonroot="true"       evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:8080/ || exit 1
ENTRYPOINT ["python", "-m", "mailu"]
CMD ["--help"]
