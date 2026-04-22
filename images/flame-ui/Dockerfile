FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/pawelmalak/flame/releases/download/v2.3.1/flame_2.3.1_linux_amd64.tar.gz" \
    -o /flame.tar.gz && \
    tar -xzf /flame.tar.gz -C / && rm /flame.tar.gz && chmod +x /flame 2>/dev/null || true
RUN strip /flame 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app/data

FROM scratch

COPY --from=downloader /flame /usr/local/bin/flame 2>/dev/null || true
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin flame 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 5005
ENTRYPOINT ["flame"]
CMD ["--ui-only"]
LABEL org.opencontainers.image.title="flame-ui" \
      org.opencontainers.image.description="Flame - UI variant" \
      org.opencontainers.image.vendor="pawelmalak" \
      org.opencontainers.image.source="https://github.com/pawelmalak/flame" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM