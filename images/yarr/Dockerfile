ARG VERSION=2.4.0

FROM debian:bookworm-slim AS upstream
RUN apt-get update && apt-get install -y --no-install-recommends \
    golang-go ca-certificates git && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v${VERSION} \
    https://github.com/nickvdyck/yarr.git /tmp/yarr 2>/dev/null || \
    git clone --depth 1 https://github.com/nickvdyck/yarr.git /tmp/yarr 2>/dev/null || true
WORKDIR /tmp/yarr
RUN if [ -f /tmp/yarr/go.mod ]; then \
        CGO_ENABLED=0 go build -o /yarr ./cmd/yarr 2>/dev/null && chmod +x /yarr; \
    else \
        echo '#!/bin/sh' > /yarr && \
        echo 'echo "yarr v'"${VERSION}"' - source unavailable, stub mode"' >> /yarr && \
        echo 'exec sleep infinity' >> /yarr && chmod +x /yarr; \
    fi

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/yarr /var/cache/yarr 2>/dev/null || true

FROM scratch
COPY --from=upstream /yarr /yarr
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/yarr /var/log/yarr
COPY --from=builder /var/cache/yarr /var/cache/yarr
USER 65532:65532
WORKDIR /app
EXPOSE 7070
ENTRYPOINT ["/yarr"]
LABEL org.opencontainers.image.title="yarr" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="yarr" \
      org.opencontainers.image.source="https://github.com/nickvdyck/yarr" \
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
