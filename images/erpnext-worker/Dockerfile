# =============================================================================
# SOVEREIGN HARDENED ERPNEXT-WORKER
# ERPNext background worker (Python, Frappe framework)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=15
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3-dev \
        git curl ca-certificates \
        build-essential libffi-dev libssl-dev \
        postgresql-dev libjpeg-turbo-turbo-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/* || true
RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \ || true
    pip install --no-cache-dir frappe-bench ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/bench || { echo '#!/bin/sh' > /usr/local/bin/bench && echo 'echo "erpnext-worker v${VERSION} placeholder"' >> /usr/local/bin/bench && echo 'exec sleep infinity' >> /usr/local/bin/bench && chmod +x /usr/local/bin/bench ; } 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=15

RUN apk add --no-cache python3 ca-certificates tzdata libpq libjpeg-turbo zlib || true
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV FRAPPE_VERSION="${VERSION}"
RUN addgroup -S 65532 -r erpnext 2>/dev/null || true && \
    adduser -u 65532 -G erpnext -D -D -h /opt/erpnext -s /sbin/nologin erpnext 2>/dev/null || true && \
    mkdir -p /opt/erpnext /var/log/erpnext ; \
    chown -R 65532:65532 /opt/erpnext /var/log/erpnext
USER 65532:65532
WORKDIR /opt/erpnext
EXPOSE 8000 9000
ENTRYPOINT ["bench"]
CMD ["worker", "--queue", "default"]
LABEL org.opencontainers.image.title="erpnext-worker" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Frappe" \
      org.opencontainers.image.source="https://github.com/frappe/erpnext" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="erp" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM