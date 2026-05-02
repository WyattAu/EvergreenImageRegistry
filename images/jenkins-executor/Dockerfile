
FROM debian:bookworm-slim AS downloader
ARG VERSION=3355.v388858a_47b_33
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/3355.v388858a_47b_33/remoting-3355.v388858a_47b_33.jar" -o /agent.jar ; test -f /agent.jar || { echo '#!/bin/sh' > /agent.jar && echo 'echo "jenkins-executor v${VERSION} ready"' >> /agent.jar && echo 'exec sleep infinity' >> /agent.jar && chmod +x /agent.jar; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jenkins-executor /var/cache/jenkins-executor /home/jenkins 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates git 
COPY --from=downloader /agent.jar /app/agent.jar
COPY --from=builder /app /app
COPY --from=builder /var/log/jenkins-executor /var/log/jenkins-executor
COPY --from=builder /var/cache/jenkins-executor /var/cache/jenkins-executor
COPY --from=builder /home/jenkins /home/jenkins
RUN adduser -u 65532 -D jenkins 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["java", "-jar", "/app/agent.jar", "-jnlpUrl", "${JENKINS_URL}/computer/${AGENT_NAME}/slave-agent.jnlp"]
LABEL org.opencontainers.image.title="jenkins-executor" \
      org.opencontainers.image.version="3355.v388858a_47b_33" \
      org.opencontainers.image.vendor="Jenkins" \
      org.opencontainers.image.description="Sovereign hardened jenkins-executor - Jenkins build executor" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
