ARG VERSION=v1.24.0
ARG BUILD_DATE

FROM gcr.io/kaniko-project/executor:v1.24.0 AS upstream
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /kaniko /var/log/kaniko /var/cache/kaniko

FROM debian:bookworm-slim
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app /app
COPY --from=builder /kaniko /kaniko
COPY --from=builder /var/log/kaniko /var/log/kaniko
COPY --from=builder /var/cache/kaniko /var/cache/kaniko
COPY --from=upstream /kaniko/executor /kaniko/executor
COPY --from=upstream /kaniko/.docker /kaniko/.docker
COPY --from=upstream /usr/local/bin /usr/local/bin
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN ln -sf /kaniko/executor /usr/local/bin/kaniko
RUN useradd -r -u 65534 -g '' kaniko 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/kaniko/executor", "--version"]
ENTRYPOINT ["/kaniko/executor"]
LABEL org.opencontainers.image.title="kaniko" \
      org.opencontainers.image.version="1.24.0" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Sovereign hardened kaniko - container image builder" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
