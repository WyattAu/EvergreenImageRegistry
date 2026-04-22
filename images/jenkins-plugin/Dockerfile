ARG VERSION=2.462.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates java-17-runtime && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/2.462.1/jenkins-war-2.462.1.war" -o /jenkins.war

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jenkins-plugin /var/cache/jenkins-plugin /home/jenkins

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
COPY --from=downloader /jenkins.war /app/jenkins.war
COPY --from=builder /app /app
COPY --from=builder /var/log/jenkins-plugin /var/log/jenkins-plugin
COPY --from=builder /var/cache/jenkins-plugin /var/cache/jenkins-plugin
COPY --from=builder /home/jenkins /home/jenkins
RUN useradd -r -u 65532 -g '' jenkins 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/jenkins.war"]
LABEL org.opencontainers.image.title="jenkins-plugin" \
      org.opencontainers.image.version="2.462.1" \
      org.opencontainers.image.vendor="Jenkins" \
      org.opencontainers.image.description="Sovereign hardened jenkins-plugin - Jenkins plugin manager" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM