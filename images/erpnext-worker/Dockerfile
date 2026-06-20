# =============================================================================
# EVERGREEN HARDENED ERPNEXT-WORKER
# ERPNext background worker (Python, Frappe framework)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=15
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3-dev \
        git curl ca-certificates \
        build-base libffi-dev libssl-dev \
        postgresql-dev postgresql-dev libjpeg-turbo-dev zlib-dev && \
    rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN     pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir frappe-bench==5.29.1 ; \
    mkdir -p /usr/local/bin

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim

LABEL evergreen.base.fallback_reason="wolfi-base for musl compatibility"
ARG VERSION=15

RUN apk add --no-cache python3 ca-certificates tzdata postgresql-libs libjpeg-turbo zlib || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV FRAPPE_VERSION="${VERSION}"
RUN groupadd -g 10000 erpnext 2>/dev/null || true && \
    useradd -u 65532 -g erpnext -r -M -s /bin/false erpnext 2>/dev/null || true && \
    mkdir -p /opt/erpnext /var/log/erpnext ; \
    chown -R 65532:65532 /opt/erpnext /var/log/erpnext 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/erpnext
EXPOSE 8000 9000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8000"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "bench"]
CMD ["--", "worker", "--queue", "default"]
LABEL org.opencontainers.image.title="erpnext-worker" \
      org.opencontainers.image.description="erpnext-worker container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Frappe" \
      org.opencontainers.image.source="https://github.com/frappe/erpnext" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="erp" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
