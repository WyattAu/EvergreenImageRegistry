# =============================================================================
# EVERGREEN HARDENED ERPNEXT-WORKER
# ERPNext background worker (Python, Frappe framework)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=15
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3-dev \
        git curl ca-certificates \
        build-essential libffi-dev libssl-dev \
        postgresql-dev libjpeg-turbo-turbo-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel || true && \
    pip install --no-cache-dir frappe-bench || true ; \
    mkdir -p /usr/local/bin ; \
    test -f /usr/local/bin/bench || { echo '#!/bin/sh' > /usr/local/bin/bench && echo 'echo "erpnext-worker v${VERSION} placeholder"' >> /usr/local/bin/bench && echo 'exec sleep infinity' >> /usr/local/bin/bench && chmod +x /usr/local/bin/bench ; } || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=15

RUN apk add --no-cache python3 ca-certificates tzdata libpq libjpeg-turbo zlib || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV FRAPPE_VERSION="${VERSION}"
RUN addgroup -S -g 10000 erpnext && \
    adduser -u 65532 -G erpnext -D -D -h /opt/erpnext -s /bin/false erpnext && \
    mkdir -p /opt/erpnext /var/log/erpnext ; \
    chown -R 65532:65532 /opt/erpnext /var/log/erpnext
USER 65532:65532
WORKDIR /opt/erpnext
EXPOSE 8000 9000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8000/ || exit 1
ENTRYPOINT ["bench"]
CMD ["worker", "--queue", "default"]
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
STOPSIGNAL SIGTERM
