FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://falco.org/repo/falcosecurity-packages.asc" | gpg --dearmor -o /etc/apt/trusted.gpg.d/falcosecurity.gpg && \
    echo "deb [signed-by=/etc/apt/trusted.gpg.d/falcosecurity.gpg] https://download.falco.org/packages/deb stable main" > /etc/apt/sources.list.d/falcosecurity.list && \
    apt-get update && apt-get install -y --no-install-recommends falco && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/falco /etc/falco

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates libjson-c5 libyaml-0-2 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/bin/falco /usr/local/bin/falco
COPY --from=builder /etc/falco /etc/falco
COPY --from=builder /app /app
COPY --from=builder /var/log/falco /var/log/falco
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin falco 2>/dev/null || true && \
    chown -R 65534:65534 /app /var/log/falco 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["falco", "--version"] || exit 0
ENTRYPOINT ["falco"]
LABEL org.opencontainers.image.title="falco" \
      org.opencontainers.image.description="Falco - Cloud native runtime security" \
      org.opencontainers.image.vendor="Sysdig" \
      org.opencontainers.image.source="https://github.com/falcosecurity/falco" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
