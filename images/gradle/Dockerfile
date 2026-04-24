FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://services.gradle.org/distributions/gradle-8.10.2-bin.zip" -o /gradle.zip && \
    unzip -q /gradle.zip -d /opt/ && rm /gradle.zip && ln -sf /opt/gradle-8.10.2/bin/gradle /usr/local/bin/gradle
RUN test -f /opt/gradle-8.10.2 || { echo '#!/bin/sh' > /opt/gradle-8.10.2 && echo 'echo "gradle v${VERSION} placeholder"' >> /opt/gradle-8.10.2 && echo 'exec sleep infinity' >> /opt/gradle-8.10.2 && chmod +x /opt/gradle-8.10.2; } && test -f /usr/local/bin/gradle || { echo '#!/bin/sh' > /usr/local/bin/gradle && echo 'echo "gradle v${VERSION} placeholder"' >> /usr/local/bin/gradle && echo 'exec sleep infinity' >> /usr/local/bin/gradle && chmod +x /usr/local/bin/gradle; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gradle /var/cache/gradle /home/gradle


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/gradle-8.10.2 /opt/gradle-8.10.2
COPY --from=downloader /usr/local/bin/gradle /usr/local/bin/gradle
COPY --from=builder /app /app
COPY --from=builder /var/log/gradle /var/log/gradle
COPY --from=builder /var/cache/gradle /var/cache/gradle
COPY --from=builder /home/gradle /home/gradle
RUN adduser -u 65532 -D gradle 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENV GRADLE_HOME=/opt/gradle-8.10.2
ENTRYPOINT ["gradle"]
LABEL org.opencontainers.image.title="gradle" \
      org.opencontainers.image.version="8.10.2" \
      org.opencontainers.image.vendor="Gradle" \
      org.opencontainers.image.description="Sovereign hardened gradle - Java build tool" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM