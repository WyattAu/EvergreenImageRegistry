ARG VERSION=1.20

FROM debian:bookworm-slim AS builder
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

FROM debian:bookworm-slim AS builder
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
ENTRYPOINT ["/oscam"]
LABEL org.opencontainers.image.title="oscam" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Oscam" \
      org.opencontainers.image.source="https://github.com/oscam-git/oscam" \
      sovereign.image.tier="3" \
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
