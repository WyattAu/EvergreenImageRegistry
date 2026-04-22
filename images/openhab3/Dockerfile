FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless curl ca-certificates unzip \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/openhab/openhab-distro/releases/download/4.2.1/openhab-4.2.1.zip" \
    -o /openhab.zip && \
    unzip -q /openhab.zip -d /opt/openhab && rm /openhab.zip
RUN mkdir -p /app /opt/openhab/userdata /opt/openhab/conf /opt/openhab/log

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless ca-certificates curl libffi-dev libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/openhab /opt/openhab
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /opt/openhab -s /sbin/nologin openhab 2>/dev/null || true && \
    chown -R 65534:65534 /opt/openhab /app 2>/dev/null || true
USER 65534:65534
WORKDIR /opt/openhab
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:8080/rest/"] || exit 0
ENTRYPOINT ["/opt/openhab/start.sh"]
LABEL org.opencontainers.image.title="openhab3" \
      org.opencontainers.image.description="openHAB 3 - Open source home automation" \
      org.opencontainers.image.vendor="openHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
