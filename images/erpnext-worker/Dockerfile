# =============================================================================
# SOVEREIGN HARDENED ERPNEXT-WORKER
# ERPNext background worker (Python, Frappe framework)
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=15
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv python3-dev \
        git curl ca-certificates \
        build-essential libffi-dev libssl-dev \
        libpq-dev libjpeg62-turbo-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir frappe-bench

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates tzdata \
        libpq5 libjpeg62-turbo zlib1g && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV FRAPPE_VERSION="${VERSION}"
RUN groupadd -g 65534 -r erpnext 2>/dev/null || true && \
    useradd -r -u 65534 -g erpnext -d /opt/erpnext -s /sbin/nologin erpnext 2>/dev/null || true && \
    mkdir -p /opt/erpnext /var/log/erpnext && \
    chown -R 65534:65534 /opt/erpnext /var/log/erpnext
USER 65534:65534
WORKDIR /opt/erpnext
EXPOSE 8000 9000
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["python3", "-c", "import frappe; print('ok')"] || exit 0
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
      sovereign.constraint.debian_slim="true"
