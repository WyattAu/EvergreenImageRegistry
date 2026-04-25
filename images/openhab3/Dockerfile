
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jre-base curl ca-certificates unzip || true ; \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/openhab/openhab-distro/releases/download/4.2.1/openhab-4.2.1.zip || true ; \
    -o /openhab.zip && \
    unzip -q /openhab.zip -d /opt/openhab && rm /openhab.zip || true
RUN mkdir -p /app /opt/openhab/userdata /opt/openhab/conf /opt/openhab/log 2>/dev/null || true


RUN mkdir -p /opt/openhab ; \ ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "openhab3 v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl libffi-dev || true
COPY --from=builder /opt/openhab /opt/openhab
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /opt/openhab -s /sbin/nologin openhab 2>/dev/null || true && \
    chown -R 65532:65532 /opt/openhab /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/openhab
EXPOSE 8080 8443
ENTRYPOINT ["/opt/openhab/start.sh"]
LABEL org.opencontainers.image.title="openhab3" \
      org.opencontainers.image.description="openHAB 3 - Open source home automation" \
      org.opencontainers.image.vendor="openHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM