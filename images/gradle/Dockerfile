ARG VERSION=8.10.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://services.gradle.org/distributions/gradle-8.10.2-bin.zip" -o /gradle.zip && \
    unzip -q /gradle.zip -d /opt/ && rm /gradle.zip && ln -sf /opt/gradle-8.10.2/bin/gradle /usr/local/bin/gradle

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gradle /var/cache/gradle /home/gradle

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/gradle-8.10.2 /opt/gradle-8.10.2
COPY --from=downloader /usr/local/bin/gradle /usr/local/bin/gradle
COPY --from=builder /app /app
COPY --from=builder /var/log/gradle /var/log/gradle
COPY --from=builder /var/cache/gradle /var/cache/gradle
COPY --from=builder /home/gradle /home/gradle
RUN useradd -r -u 65534 -g '' gradle 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
ENV GRADLE_HOME=/opt/gradle-8.10.2
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["gradle", "--version"]
ENTRYPOINT ["gradle"]
LABEL org.opencontainers.image.title="gradle" \
      org.opencontainers.image.version="8.10.2" \
      org.opencontainers.image.vendor="Gradle" \
      org.opencontainers.image.description="Sovereign hardened gradle - Java build tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
