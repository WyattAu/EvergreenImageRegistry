ARG VERSION=1.20.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libexpat1-dev libevent-dev && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL \
    "https://unbound.net/downloads/unbound-${VERSION}.tar.gz" \
    -o /unbound.tar.gz && \
    tar -xzf /unbound.tar.gz -C /tmp && \
    cd /tmp/unbound-${VERSION} && \
    ./configure --with-pthreads --with-libevent --enable-subnet && \
    make -j$(nproc) && \
    make install DESTDIR=/opt/unbound && \
    cp /opt/unbound/usr/sbin/unbound /unbound && chmod +x /unbound
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS dirs
RUN mkdir -p /app /var/log/unbound /var/cache/unbound 2>/dev/null || true

FROM scratch
COPY --from=builder /unbound /unbound
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=dirs /app /app
COPY --from=dirs /var/log/unbound /var/log/unbound
COPY --from=dirs /var/cache/unbound /var/cache/unbound
USER 65532:65532
WORKDIR /app
EXPOSE 53

HEALTHCHECK NONE
ENTRYPOINT ["/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.description="Unbound - validating, recursive, and caching DNS resolver" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="NLnet Labs" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/NLnetLabs/unbound"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
