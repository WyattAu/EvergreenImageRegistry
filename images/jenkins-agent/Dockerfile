ARG VERSION=2.462.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/2.462.1/remoting-2.462.1.jar" -o /agent.jar

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/jenkins-agent /var/cache/jenkins-agent /home/jenkins

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=downloader /agent.jar /app/agent.jar
COPY --from=builder /app /app
COPY --from=builder /var/log/jenkins-agent /var/log/jenkins-agent
COPY --from=builder /var/cache/jenkins-agent /var/cache/jenkins-agent
COPY --from=builder /home/jenkins /home/jenkins
RUN useradd -r -u 65534 -g '' jenkins 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV HOME=/app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["java", "-jar", "/app/agent.jar", "--version"]
ENTRYPOINT ["java", "-jar", "/app/agent.jar"]
LABEL org.opencontainers.image.title="jenkins-agent" \
      org.opencontainers.image.version="2.462.1" \
      org.opencontainers.image.vendor="Jenkins" \
      org.opencontainers.image.description="Sovereign hardened jenkins-agent - Jenkins SSH/JNLP agent" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="30s"
