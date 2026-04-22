FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        cockpit cockpit-ws cockpit-dashboard cockpit-storaged cockpit-system ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        cockpit cockpit-ws cockpit-dashboard cockpit-storaged cockpit-system ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin cockpit 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-sf", "http://localhost:9090/"] || exit 0
ENTRYPOINT ["cockpit-ws"]
CMD ["--port", "9090"]
LABEL org.opencontainers.image.title="cockpit" \
      org.opencontainers.image.description="Cockpit - Web-based server management" \
      org.opencontainers.image.vendor="Red Hat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
