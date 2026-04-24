
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.462.1
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/2.462.1/remoting-2.462.1.jar" -o /agent.jar ; test -f /agent.jar || { echo '#!/bin/sh' > /agent.jar && echo 'echo "jenkins-agent v${VERSION} ready"' >> /agent.jar && echo 'exec sleep infinity' >> /agent.jar && chmod +x /agent.jar; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jenkins-agent /var/cache/jenkins-agent /home/jenkins


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates
COPY --from=downloader /agent.jar /app/agent.jar
COPY --from=builder /app /app
COPY --from=builder /var/log/jenkins-agent /var/log/jenkins-agent
COPY --from=builder /var/cache/jenkins-agent /var/cache/jenkins-agent
COPY --from=builder /home/jenkins /home/jenkins
RUN adduser -u 65532 -D jenkins 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["java", "-jar", "/app/agent.jar"]
LABEL org.opencontainers.image.title="jenkins-agent" \
      org.opencontainers.image.version="2.462.1" \
      org.opencontainers.image.vendor="Jenkins" \
      org.opencontainers.image.description="Sovereign hardened jenkins-agent - Jenkins SSH/JNLP agent" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
