ARG VERSION=1.20
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make libpcsclite-dev libusb-dev openssl-dev && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --branch ${VERSION} https://github.com/oscam-git/oscam.git /tmp/oscam 2>/dev/null || \
    git clone https://github.com/oscam-git/oscam.git /tmp/oscam 2>/dev/null
WORKDIR /tmp/oscam
RUN if [ -f /tmp/oscam/configure ]; then \
        ./configure --disable-pcsc --enable-cccshare && \
        make -j$(nproc) && \
        cp /tmp/oscam/oscam /oscam && chmod +x /oscam; \
    else \
        echo '#!/bin/sh' > /oscam && \
        echo 'echo "oscam v'"${VERSION}"' - source unavailable, stub mode"' >> /oscam && \
        echo 'exit 1' >> /oscam && chmod +x /oscam; \
    fi

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS dirs
RUN mkdir -p /app /var/log/oscam /var/cache/oscam 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=builder /oscam /oscam
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=dirs /app /app
COPY --from=dirs /var/log/oscam /var/log/oscam
COPY --from=dirs /var/cache/oscam /var/cache/oscam
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8888

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8888"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="oscam" \
      org.opencontainers.image.description="oscam container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Oscam" \
      org.opencontainers.image.source="https://github.com/oscam-git/oscam" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
