FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends         python3 python3-pip ca-certificates     && rm -rf /var/lib/apt/lists/* &&     pip install --break-system-packages --no-cache-dir zigpy 2>/dev/null || true
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin homekit 2>/dev/null || true
RUN mkdir -p /app && chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3     CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="homekit"       org.opencontainers.image.description="Placeholder - HomeKit"       sovereign.image.tier="3"       sovereign.image.status="placeholder"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
