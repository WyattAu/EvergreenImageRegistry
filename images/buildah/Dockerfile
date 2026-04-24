ARG VERSION=latest
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    buildah \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app /var/log/buildah /var/cache/buildah /var/lib/containers


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates containers-common
COPY --from=builder /usr/bin/buildah /usr/local/bin/buildah
COPY --from=builder /app /app
COPY --from=builder /var/log/buildah /var/log/buildah
COPY --from=builder /var/cache/buildah /var/cache/buildah
RUN mkdir -p /var/lib/containers /run/containers
RUN adduser -u 65532 -D buildah 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["buildah"]
LABEL org.opencontainers.image.title="buildah" \
      org.opencontainers.image.description="Sovereign hardened buildah - OCI image builder" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM