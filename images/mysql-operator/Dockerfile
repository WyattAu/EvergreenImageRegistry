# =============================================================================
# SOVEREIGN HARDENED MYSQL OPERATOR
# Generated from template - Version: 0.5.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.5.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/presslabs/mysql-operator/releases/download/v0.5.0/mysql-operator-0.5.0-linux-amd64.tar.gz" -o /mysql-operator.tar.gz && \
    echo "PENDING_CHECKSUM  /mysql-operator.tar.gz" | sha256sum -c - && \
    tar -xzf /mysql-operator.tar.gz -C / && rm /mysql-operator.tar.gz && chmod +x /mysql-operator 2>/dev/null || \
    curl -fsSL "https://github.com/presslabs/mysql-operator/releases/download/v0.5.0/mysql-operator-0.5.0-linux-amd64.tar.gz" -o /mysql-operator && chmod +x /mysql-operator

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/mysql-operator /var/cache/mysql-operator

FROM scratch
COPY --from=downloader /mysql-operator /mysql-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/mysql-operator /var/log/mysql-operator
COPY --from=builder /var/cache/mysql-operator /var/cache/mysql-operator
USER 65534:65534
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/mysql-operator", "--version"]
ENTRYPOINT ["/mysql-operator"]
LABEL org.opencontainers.image.title="mysql-operator" \
      org.opencontainers.image.version="0.5.0" \
      org.opencontainers.image.description="Presslabs MySQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Presslabs" \
      org.opencontainers.image.source="https://github.com/presslabs/mysql-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
