# =============================================================================
# SOVEREIGN HARDENED BIND
# Generated from template - Version: 9.18.0
# Constraint: distroless/static - no shell, no package manager
# =============================================================================

ARG VERSION=9.18.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://www.isc.org/bind/" -o /named.tar.gz && \
    tar -xzf /named.tar.gz -C / && rm /named.tar.gz && chmod +x /named

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/named /var/cache/named

FROM gcr.io/distroless/static:nonroot
COPY --from=downloader /named /named
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/named /var/log/named
COPY --from=builder /var/cache/named /var/cache/named
USER 65534:65534
WORKDIR /app
EXPOSE 53 953
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD named --version 2>/dev/null || exit 1
ENTRYPOINT ["/named"]
LABEL org.opencontainers.image.title="bind" \
      org.opencontainers.image.version="9.18.0" \
      org.opencontainers.image.vendor="ISC" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distroless="true"
