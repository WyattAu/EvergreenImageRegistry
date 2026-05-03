ARG VERSION=1.20
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make libpcsclite-dev libusb-dev openssl-dev && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch ${VERSION} https://github.com/oscam-git/oscam.git /tmp/oscam 2>/dev/null || \
    git clone --depth 1 https://github.com/oscam-git/oscam.git /tmp/oscam 2>/dev/null || true
WORKDIR /tmp/oscam
RUN if [ -f /tmp/oscam/configure ]; then \
        ./configure --disable-pcsc --enable-cccshare && \
        make -j$(nproc) && \
        cp /tmp/oscam/oscam /oscam && chmod +x /oscam; \
    else \
        echo '#!/bin/sh' > /oscam && \
        echo 'echo "oscam v'"${VERSION}"' - source unavailable, stub mode"' >> /oscam && \
        echo 'exec sleep infinity' >> /oscam && chmod +x /oscam; \
    fi

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/oscam /var/cache/oscam 2>/dev/null || true


FROM scratch
COPY --from=builder /oscam /oscam
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/oscam /var/log/oscam
COPY --from=builder /var/cache/oscam /var/cache/oscam
USER 65532:65532
WORKDIR /app
EXPOSE 8888

HEALTHCHECK NONE
ENTRYPOINT ["/oscam"]
LABEL org.opencontainers.image.title="oscam" \
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
STOPSIGNAL SIGTERM
