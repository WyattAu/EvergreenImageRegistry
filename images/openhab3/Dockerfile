FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        java-17-runtime curl ca-certificates unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/openhab/openhab-distro/releases/download/4.2.1/openhab-4.2.1.zip" \
    -o /openhab.zip && \
    unzip -q /openhab.zip -d /opt/openhab && rm /openhab.zip
RUN mkdir -p /app /opt/openhab/userdata /opt/openhab/conf /opt/openhab/log

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates curl libffi-dev
COPY --from=builder /opt/openhab /opt/openhab
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /opt/openhab -s /sbin/nologin openhab 2>/dev/null || true && \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM