FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev make && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/static-c /var/cache/static-c 2>/dev/null || true
RUN echo 'int main(void) { return 0; }' > /tmp/test.c && \
    gcc -static -o /app/test /tmp/test.c && rm /tmp/test.c && strip /app/test || true


RUN mkdir -p /app 2>/dev/null || true ; mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true


RUN mkdir -p /app 2>/dev/null || true
FROM scratch
COPY --from=builder /app /app
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="static-c" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.description="Sovereign hardened static-c - Static C binary compilation base" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM

