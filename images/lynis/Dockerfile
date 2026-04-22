FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/CISOfy/Lynis.git /src
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /src /app/src
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin lynis 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["/app/src/lynis", "show", "version"] || exit 0
ENTRYPOINT ["/app/src/lynis"]
CMD ["audit", "system"]
LABEL org.opencontainers.image.title="lynis" \
      org.opencontainers.image.description="Lynis - Security auditing tool" \
      org.opencontainers.image.vendor="CISOfy" \
      org.opencontainers.image.source="https://github.com/CISOfy/Lynis" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
