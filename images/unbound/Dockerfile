ARG VERSION=1.20.0
ARG TARGETARCH

FROM debian:bookworm-slim AS builder
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libexpat1-dev libevent-dev && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://unbound.net/downloads/unbound-${VERSION}.tar.gz" \
    -o /unbound.tar.gz && \
    tar -xzf /unbound.tar.gz -C /tmp && \
    cd /tmp/unbound-${VERSION} && \
    ./configure --with-pthreads --with-libevent --enable-subnet && \
    make -j$(nproc) && \
    make install DESTDIR=/opt/unbound && \
    cp /opt/unbound/usr/sbin/unbound /unbound && chmod +x /unbound

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/unbound /var/cache/unbound 2>/dev/null || true

FROM scratch
COPY --from=builder /unbound /unbound
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/unbound /var/log/unbound
COPY --from=builder /var/cache/unbound /var/cache/unbound
USER 65532:65532
WORKDIR /app
EXPOSE 53
ENTRYPOINT ["/unbound"]
LABEL org.opencontainers.image.title="unbound" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="NLnet Labs" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
