FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ggshield
RUN mkdir -p /app

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65534 -g nogroup -d /app -s /sbin/nologin ggshield 2>/dev/null || true && \
    chown -R 65534:65534 /app 2>/dev/null || true
USER 65534:65534
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=1 \
    CMD ["ggshield", "--version"]
ENTRYPOINT ["ggshield"]
LABEL org.opencontainers.image.title="ggshield" \
      org.opencontainers.image.description="ggshield - GitGuardian CLI" \
      org.opencontainers.image.vendor="GitGuardian" \
      org.opencontainers.image.source="https://github.com/GitGuardian/ggshield" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
