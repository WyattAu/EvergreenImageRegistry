ARG VERSION=2.462.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates java-17-runtime && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/2.462.1/remoting-2.462.1.jar" -o /agent.jar

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jenkins-executor /var/cache/jenkins-executor /home/jenkins

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates git
COPY --from=downloader /agent.jar /app/agent.jar
COPY --from=builder /app /app
COPY --from=builder /var/log/jenkins-executor /var/log/jenkins-executor
COPY --from=builder /var/cache/jenkins-executor /var/cache/jenkins-executor
COPY --from=builder /home/jenkins /home/jenkins
RUN useradd -r -u 65532 -g '' jenkins 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENTRYPOINT ["java", "-jar", "/app/agent.jar", "-jnlpUrl", "${JENKINS_URL}/computer/${AGENT_NAME}/slave-agent.jnlp"]
LABEL org.opencontainers.image.title="jenkins-executor" \
      org.opencontainers.image.version="2.462.1" \
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