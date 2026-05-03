ARG VERSION=latest

FROM ghcr.io/innernet-rs/innernet:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/innernet-client /var/cache/innernet-client 2>/dev/null || true


FROM scratch
COPY --from=upstream /usr/local/bin/innernet /innernet
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/innernet-client /var/log/innernet-client
COPY --from=builder /var/cache/innernet-client /var/cache/innernet-client

WORKDIR /app

EXPOSE 51820/udp
EXPOSE 9101

LABEL org.opencontainers.image.title="innernet-client" org.opencontainers.image.version="0.16.0" org.opencontainers.image.vendor="innernet-rs" org.opencontainers.image.source="https://github.com/innernet-rs/innernet" org.opencontainers.image.description="innernet peer/client daemon (WireGuard-based)" evergreen.image.tier="1" evergreen.image.category="networking" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/innernet"]

CMD ["up", "--daemon"]
