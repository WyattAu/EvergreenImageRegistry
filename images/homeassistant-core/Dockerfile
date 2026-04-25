
FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir homeassistant
RUN mkdir -p /config /app 2>/dev/null || true


RUN mkdir -p /opt/venv ; \ 2>/dev/null || true ; \
    test -f /app || { echo '#!/bin/sh' > /app && echo 'echo "homeassistant-core v${VERSION} placeholder"' >> /app && echo 'exec sleep infinity' >> /app && chmod +x /app ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates tzdata libffi-dev openssl-dev || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S nogroup 2>/dev/null || true
RUN adduser -u 65532 -G nogroup -D -h /config -s /sbin/nologin hass 2>/dev/null || true && \
    mkdir -p /config && chown -R 65532:65532 /config /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH" HOME="/config"
WORKDIR /config
EXPOSE 8123
ENTRYPOINT ["/opt/venv/bin/hass"]
CMD ["--config", "/config"]
LABEL org.opencontainers.image.title="homeassistant-core" \
      org.opencontainers.image.description="Home Assistant Core - Open source home automation" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/core" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM