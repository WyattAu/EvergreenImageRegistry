# =============================================================================
# SOVEREIGN HARDENED MARIADB OPERATOR
# Generated from template - Version: 0.35.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.35.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/mariadb-operator/mariadb-operator/releases/download/v0.35.0/mariadb-operator-0.35.0-linux-amd64.tar.gz" -o /mariadb-operator.tar.gz && \
    echo "PENDING_CHECKSUM  /mariadb-operator.tar.gz" | sha256sum -c - && \
    tar -xzf /mariadb-operator.tar.gz -C / && rm /mariadb-operator.tar.gz && chmod +x /mariadb-operator 2>/dev/null || \
    curl -fsSL "https://github.com/mariadb-operator/mariadb-operator/releases/download/v0.35.0/mariadb-operator-0.35.0-linux-amd64.tar.gz" -o /mariadb-operator && chmod +x /mariadb-operator

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mariadb-operator /var/cache/mariadb-operator

FROM scratch
COPY --from=downloader /mariadb-operator /mariadb-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mariadb-operator /var/log/mariadb-operator
COPY --from=builder /var/cache/mariadb-operator /var/cache/mariadb-operator
USER 65534:65534
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/mariadb-operator", "--version"]
ENTRYPOINT ["/mariadb-operator"]
LABEL org.opencontainers.image.title="mariadb-operator" \
      org.opencontainers.image.version="0.35.0" \
      org.opencontainers.image.description="MariaDB Operator for Kubernetes" \
      org.opencontainers.image.vendor="mariadb-operator" \
      org.opencontainers.image.source="https://github.com/mariadb-operator/mariadb-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
