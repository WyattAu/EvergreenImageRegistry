# =============================================================================
# SOVEREIGN HARDENED KNOT-RESOLVER
# Generated from template - Version: 5.8.1
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.8.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://knot-resolver.org/download/knot-resolver-5.8.1.tar.gz" -o /kresd.tar.gz && \
    tar -xzf /kresd.tar.gz -C / && rm /kresd.tar.gz && chmod +x /kresd 2>/dev/null || \
    curl -fsSL "https://knot-resolver.org/download/knot-resolver-5.8.1.tar.gz" -o /kresd && chmod +x /kresd

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/kresd /var/cache/kresd

FROM scratch
COPY --from=downloader /kresd /kresd
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/kresd /var/log/kresd
COPY --from=builder /var/cache/kresd /var/cache/kresd
USER 65534:65534
WORKDIR /app
EXPOSE 53
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kresd", "--version"]
ENTRYPOINT ["/kresd"]
LABEL org.opencontainers.image.title="knot-resolver" \
      org.opencontainers.image.version="5.8.1" \
      org.opencontainers.image.vendor="Knot DNS" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
