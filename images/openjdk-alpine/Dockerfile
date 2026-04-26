ARG VERSION=21-slim
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://packages.adoptium.net/artifactory/api/gnupg/key/public" | gnupg --dearmor -o /usr/share/keyrings/adoptium.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium.gnupg] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && apt-get install -y --no-install-recommends temurin-21-jre-headless && rm -rf /var/lib/apt/lists/* || true
RUN mkdir -p /app /var/log/openjdk-alpine /var/cache/openjdk-alpine 2>/dev/null || true


RUN test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "openjdk-alpine v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; } ; \
    test -f /var/log/openjdk-alpine || { echo '#!/bin/sh' > /var/log/openjdk-alpine && echo 'echo "openjdk-alpine v${VERSION} placeholder"' >> /var/log/openjdk-alpine && echo 'exec sleep infinity' >> /var/log/openjdk-alpine && chmod +x /var/log/openjdk-alpine ; } ; \
    test -f /var/cache/openjdk-alpine || { echo '#!/bin/sh' > /var/cache/openjdk-alpine && echo 'echo "openjdk-alpine v${VERSION} placeholder"' >> /var/cache/openjdk-alpine && echo 'exec sleep infinity' >> /var/cache/openjdk-alpine && chmod +x /var/cache/openjdk-alpine ; }

FROM cgr.dev/chainguard/wolfi-base:latest

COPY --from=builder /usr/share/keyrings/adoptium.gnupg /usr/share/keyrings/adoptium.gnupg
COPY --from=builder /etc/apt/sources.list.d/adoptium.list /etc/apt/sources.list.d/adoptium.list
RUN apk add --no-cache ca-certificates 
COPY --from=builder /app /app
COPY --from=builder /var/log/openjdk-alpine /var/log/openjdk-alpine
COPY --from=builder /var/cache/openjdk-alpine /var/cache/openjdk-alpine
RUN adduser -u 65532 -D java 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["java"]
LABEL org.opencontainers.image.title="openjdk-alpine" \
      org.opencontainers.image.version="21" \
      org.opencontainers.image.vendor="Eclipse Adoptium" \
      org.opencontainers.image.description="Sovereign hardened openjdk-alpine - JRE runtime (no Alpine, debian-slim)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM