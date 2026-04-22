ARG VERSION=21-slim
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://packages.adoptium.net/artifactory/api/gpg/key/public" | gpg --dearmor -o /usr/share/keyrings/adoptium.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo $VERSION_CODENAME) main" > /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && apt-get install -y --no-install-recommends temurin-21-jre-headless && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/openjdk-alpine /var/cache/openjdk-alpine

FROM debian:bookworm-slim
COPY --from=builder /usr/share/keyrings/adoptium.gpg /usr/share/keyrings/adoptium.gpg
COPY --from=builder /etc/apt/sources.list.d/adoptium.list /etc/apt/sources.list.d/adoptium.list
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates temurin-21-jre-headless && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/openjdk-alpine /var/log/openjdk-alpine
COPY --from=builder /var/cache/openjdk-alpine /var/cache/openjdk-alpine
RUN useradd -r -u 65534 -g '' java 2>/dev/null || true
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["java", "--version"]
ENTRYPOINT ["java"]
LABEL org.opencontainers.image.title="openjdk-alpine" \
      org.opencontainers.image.version="21" \
      org.opencontainers.image.vendor="Eclipse Adoptium" \
      org.opencontainers.image.description="Sovereign hardened openjdk-alpine - JRE runtime (no Alpine, debian-slim)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
