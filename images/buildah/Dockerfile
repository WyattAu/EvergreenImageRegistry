ARG VERSION=latest
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    buildah \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/buildah /var/cache/buildah /var/lib/containers

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    containers-common \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/bin/buildah /usr/local/bin/buildah
COPY --from=builder /app /app
COPY --from=builder /var/log/buildah /var/log/buildah
COPY --from=builder /var/cache/buildah /var/cache/buildah
RUN mkdir -p /var/lib/containers /run/containers
RUN useradd -r -u 65534 -g '' buildah 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["buildah", "--version"]
ENTRYPOINT ["buildah"]
LABEL org.opencontainers.image.title="buildah" \
      org.opencontainers.image.description="Sovereign hardened buildah - OCI image builder" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
