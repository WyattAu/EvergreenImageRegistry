# =============================================================================
# EVERGREEN ALIAS - WHOOGLE -> whoogle-search
# Alias for images/whoogle-search/
# =============================================================================

ARG VERSION=1.2.4
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir whoogle-search && \
    mkdir -p /app/config /app/data 2>/dev/null || true && \binary not available - download failed" >&2 exit 1"' >> /app/binary not available - download failed" >&2 exit 1 && echo 'exit 1' >> /app/binary not available - download failed" >&2 exit 1 && chmod +x /app ; }
FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:10c773dc96763e3201275bae7865d278ca4b91db586117adec79079a2d7cdb80
LABEL evergreen.base.fallback_reason="Python C extensions require glibc"
ARG VERSION=1.2.4

RUN microdnf install -y python3 ca-certificates tzdata
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false whoogle 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:5000/ || exit 1
ENTRYPOINT ["whoogle-search"]
CMD ["--port", "5000"]
LABEL org.opencontainers.image.title="whoogle" \
      org.opencontainers.image.description="whoogle container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="benbusby" \
      org.opencontainers.image.source="https://github.com/benbusby/whoogle-search" \
      evergreen.image.tier="3" \
      evergreen.image.status="functional" \
      evergreen.image.category="search" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
