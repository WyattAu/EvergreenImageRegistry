ARG VERSION=1.12.2
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
RUN apk add --no-cache python3 py3-pip ca-certificates curl && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir pdfarranger==1.12.2

USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL evergreen.image.tier="3"
LABEL evergreen.base.image="wolfi"
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

LABEL org.opencontainers.image.description="pdfarranger container image" \
      org.opencontainers.image.title="PDF Arranger" \
      org.opencontainers.image.source="https://github.com/pdfarranger/pdfarranger" \
            org.opencontainers.image.version="1.12.2"

ENTRYPOINT ["python", "-m", "pdfarranger"]
CMD ["--help"]
