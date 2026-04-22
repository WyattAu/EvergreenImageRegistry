ARG VERSION=v1.24.0
ARG BUILD_DATE

FROM gcr.io/kaniko-project/executor:v1.24.0 AS upstream
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /kaniko /var/log/kaniko /var/cache/kaniko

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
COPY --from=builder /kaniko /kaniko
COPY --from=builder /var/log/kaniko /var/log/kaniko
COPY --from=builder /var/cache/kaniko /var/cache/kaniko
COPY --from=upstream /kaniko/executor /kaniko/executor
COPY --from=upstream /kaniko/.docker /kaniko/.docker
COPY --from=upstream /usr/local/bin /usr/local/bin
RUN apk add --no-cache ca-certificates
RUN ln -sf /kaniko/executor /usr/local/bin/kaniko
RUN useradd -r -u 65532 -g '' kaniko 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["/kaniko/executor"]
LABEL org.opencontainers.image.title="kaniko" \
      org.opencontainers.image.version="1.24.0" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Sovereign hardened kaniko - container image builder" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM