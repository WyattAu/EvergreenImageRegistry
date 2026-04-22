FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/falcosecurity/rules.git /rules
RUN mkdir -p /app/rules

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /rules /app/rules
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin falcorules 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["test", "-f", "/app/rules/rules.yaml"]
ENTRYPOINT ["cat"]
CMD ["/app/rules/rules.yaml"]
LABEL org.opencontainers.image.title="falco-rules" \
      org.opencontainers.image.description="Falco - rules only" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/rules" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
