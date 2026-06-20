# =============================================================================
# EVERGREEN HARDENED LITESTREAM
# SQLite streaming replication for production workloads
# https://github.com/benbjohnson/litestream
# =============================================================================

ARG VERSION=0.5.11
ARG BUILD_DATE
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9 AS builder
ARG TARGETARCH
ARG VERSION=0.5.11
ARG TARGETARCH
RUN apk add --no-cache ca-certificates wget && \
    case ${TARGETARCH} in \
        amd64) EXPECTED_SHA="996784c9d17b8054e4127d62ca7f0aad76b45be3d1fe1af619e8886a832be417" ;; \
        arm64) EXPECTED_SHA="be8b6c250021ef58eed1d0687efbc08009b7e0401a2b7ebb5b8975d2de0b99a6" ;; \
        *) EXPECTED_SHA="" ;; \
    esac && \
    wget -t 3 -T 10 -qO /tmp/litestream.tar.gz "https://github.com/benbjohnson/litestream/releases/download/v${VERSION}/litestream-vfs-v${VERSION}-linux-${TARGETARCH}.tar.gz" \
    && echo "${EXPECTED_SHA}  /tmp/litestream.tar.gz" | sha256sum -c
ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
ARG VERSION=0.5.11
ARG BUILD_DATE
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /tmp/litestream.tar.gz /tmp/litestream.tar.gz
COPY --from=builder /bin/sh /bin/sh
RUN ["/bin/sh", "-c", "cd /tmp && tar xzf litestream.tar.gz && cp litestream /litestream && rm -f litestream.tar.gz"]

USER 65532:65532
WORKDIR /data

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/litestream"]
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
