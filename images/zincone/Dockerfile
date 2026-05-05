ARG VERSION=latest
ARG TARGETARCH

FROM zincsearch/zincsearch:${VERSION} AS upstream

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/zincone /var/cache/zincone 2>/dev/null || true


FROM scratch
COPY --from=upstream /go/bin/zincsearch /usr/local/bin/zincone
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/zincone /var/log/zincone
COPY --from=builder /var/cache/zincone /var/cache/zincone

WORKDIR /tmp

EXPOSE 4080
EXPOSE 9101

LABEL org.opencontainers.image.title="zincone" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened ZincOne - ZincSearch observability edition" org.opencontainers.image.vendor="ZincSearch" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.scratch="true" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="3s" \
      org.opencontainers.image.source="https://github.com/zinclabs/zincobserve"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/zincone"]
