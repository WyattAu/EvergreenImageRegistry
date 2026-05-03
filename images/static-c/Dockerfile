FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev make && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/static-c /var/cache/static-c 2>/dev/null || true
RUN echo 'int main(void) { return 0; }' > /tmp/test.c && \
    gcc -static -o /app/test /tmp/test.c && rm -f /tmp/test.c && strip /app/test || true


RUN mkdir -p /app 2>/dev/null || true ; mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true


RUN mkdir -p /app 2>/dev/null || true
FROM scratch
COPY --from=builder /app /app
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="static-c" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.description="Evergreen hardened static-c - Static C binary compilation base" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
