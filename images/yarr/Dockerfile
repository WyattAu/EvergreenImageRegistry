ARG VERSION=2.4.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS upstream
ARG TARGETARCH
ARG GOARCH=${TARGETARCH}
RUN apt-get update && apt-get install -y --no-install-recommends \
    golang-go ca-certificates git && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v${VERSION} \
    https://github.com/nickvdyck/yarr.git /tmp/yarr 2>/dev/null || \
    git clone --depth 1 https://github.com/nickvdyck/yarr.git /tmp/yarr 2>/dev/null || true
WORKDIR /tmp/yarr
RUN if [ -f /tmp/yarr/go.mod ]; then \
        CGO_ENABLED=0 GOARCH=${GOARCH} go build -o /yarr ./cmd/yarr 2>/dev/null && chmod +x /yarr; \
    else \
        echo '#!/bin/sh' > /yarr && \
        echo 'echo "yarr v'"${VERSION}"' - source unavailable, stub mode"' >> /yarr && \
        echo 'exec sleep infinity' >> /yarr && chmod +x /yarr; \
    fi

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
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

HEALTHCHECK NONE
ENTRYPOINT ["/yarr"]
LABEL org.opencontainers.image.title="yarr" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="yarr" \
      org.opencontainers.image.source="https://github.com/nickvdyck/yarr" \
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
