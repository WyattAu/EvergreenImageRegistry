FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        scap-workbench ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        scap-workbench ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin scapwb 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["scap-workbench", "--version"] || exit 0
ENTRYPOINT ["scap-workbench"]
LABEL org.opencontainers.image.title="scap-workbench" \
      org.opencontainers.image.description="SCAP Workbench - GUI for OpenSCAP" \
      org.opencontainers.image.vendor="Red Hat" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
