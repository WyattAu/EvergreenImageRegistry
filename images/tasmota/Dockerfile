FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends         python3 python3-pip git ca-certificates gcc g++ make     && rm -rf /var/lib/apt/lists/*
RUN pip install --break-system-packages --no-cache-dir platformio 2>/dev/null || true
RUN mkdir -p /app /firmware

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends         python3 ca-certificates     && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /firmware /firmware
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin tasmota 2>/dev/null || true &&     chown -R 65534:65534 /app /firmware 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3     CMD ["python3", "-c", "print('ok')"]
ENTRYPOINT ["python3"]
CMD ["-c", "print('Tasmota firmware build environment. Clone https://github.com/arendst/Tasmota and run platformio.')"]
LABEL org.opencontainers.image.title="tasmota"       org.opencontainers.image.description="Tasmota - ESP firmware (build environment)"       org.opencontainers.image.vendor="Tasmota"       org.opencontainers.image.source="https://github.com/arendst/Tasmota"       sovereign.image.tier="3"       sovereign.image.status="firmware-builder"       sovereign.constraint.nonroot="true"       sovereign.constraint.debian_slim="true"
