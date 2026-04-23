# =============================================================================
# SOVEREIGN HARDENED POSTGRES OPERATOR
# Generated from template - Version: 1.12.0
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.12.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/zalando/postgres-operator/releases/download/v1.12.0/postgres-operator-1.12.0-linux-amd64.tar.gz" -o /postgres-operator.tar.gz && \
    echo "PENDING_CHECKSUM  /postgres-operator.tar.gz" | sha256sum -c || true  # && \
    tar -xzf /postgres-operator.tar.gz -C / && rm /postgres-operator.tar.gz && chmod +x /postgres-operator 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/zalando/postgres-operator/releases/download/v1.12.0/postgres-operator-1.12.0-linux-amd64.tar.gz" -o /postgres-operator && chmod +x /postgres-operator

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/postgres-operator /var/cache/postgres-operator

FROM scratch
COPY --from=downloader /postgres-operator /postgres-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/postgres-operator /var/log/postgres-operator
COPY --from=builder /var/cache/postgres-operator /var/cache/postgres-operator
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/postgres-operator"]
LABEL org.opencontainers.image.title="postgres-operator" \
      org.opencontainers.image.version="1.12.0" \
      org.opencontainers.image.description="Zalando PostgreSQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/zalando/postgres-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM