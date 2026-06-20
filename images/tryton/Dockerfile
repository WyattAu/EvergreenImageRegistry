ARG VERSION=7.2.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN apk add --no-cache python3 py3-pip ca-certificates curl && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir trytond==7.2.0

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

LABEL org.opencontainers.image.description="tryton container image" \
      org.opencontainers.image.title="Tryton" \
      org.opencontainers.image.source="https://github.com/tryton/tryton" \
            org.opencontainers.image.version="7.2.0"

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "python -m trytond"]
CMD ["--help"]
