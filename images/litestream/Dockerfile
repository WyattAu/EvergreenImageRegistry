# =============================================================================
# EVERGREEN HARDENED LITESTREAM
# SQLite streaming replication for production workloads
# https://github.com/benbjohnson/litestream
# =============================================================================

ARG VERSION=0.3.14
ARG BUILD_DATE
ARG TARGETARCH

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS builder
ARG TARGETARCH
ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates curl && \
    curl -fSL "https://github.com/benbjohnson/litestream/releases/download/v${VERSION}/litestream-v${VERSION}-linux-${TARGETARCH}.tar.gz" -o /tmp/litestream.tar.gz \
    && echo "880ccafc9514650c4a2a0cc78eb1e61aaad95dd3e86e877c8694f955c9095436  /tmp/litestream.tar.gz" | sha256sum -c -
FROM scratch
ARG VERSION
ARG BUILD_DATE
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /tmp/litestream.tar.gz /tmp/litestream.tar.gz
COPY --from=builder /bin/sh /bin/sh
RUN ["/bin/sh", "-c", "cd /tmp && tar xzf litestream.tar.gz && cp litestream /litestream && rm -f litestream.tar.gz"]

USER 65532:65532
WORKDIR /data

HEALTHCHECK NONE
ENTRYPOINT ["/litestream"]
LABEL org.opencontainers.image.title="litestream" \
      org.opencontainers.image.description="SQLite streaming replication for production" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/benbjohnson/litestream" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="scratch"
LABEL evergreen.metrics.native="prometheus"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
