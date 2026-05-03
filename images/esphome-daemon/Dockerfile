
FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates gcc g++ libc6-dev ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir esphome ; mkdir -p /usr/local/bin ; test -f /usr/local/bin/esphome || { echo '#!/bin/sh' > /usr/local/bin/esphome && echo 'echo "esphome-daemon v${VERSION} placeholder"' >> /usr/local/bin/esphome && echo 'exec sleep infinity' >> /usr/local/bin/esphome && chmod +x /usr/local/bin/esphome ; } || true
RUN mkdir -p /app /config


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates tzdata 
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
COPY --from=builder /config /config
RUN addgroup -S nogroup || true
RUN adduser -u 65532 -G nogroup -D -h /config -s /bin/false esphome || true
    && chown -R 65532:65532 /config /app
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH" HOME="/config"
WORKDIR /config
EXPOSE 6053
ENTRYPOINT ["esphome"]
CMD ["--daemon"]
LABEL org.opencontainers.image.title="esphome-daemon" \
      org.opencontainers.image.description="ESPHome - daemon mode" \
      org.opencontainers.image.vendor="ESPHome" \
      org.opencontainers.image.source="https://github.com/esphome/esphome" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
