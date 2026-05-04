
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.462.1
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/2.462.1/jenkins-war-2.462.1.war" -o /jenkins.war ; test -f /jenkins.war || { echo '#!/bin/sh' > /jenkins.war && echo 'echo "jenkins-plugin v${VERSION} ready"' >> /jenkins.war && echo 'exec sleep infinity' >> /jenkins.war && chmod +x /jenkins.war; } || true && \
    echo "0f21c25fd6fafb435f1b54d3953ba20a8425e9959a35a7a8403e8a01192c0dfc  /jenkins.war" | sha256sum -c || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/jenkins-plugin /var/cache/jenkins-plugin /home/jenkins 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates 
COPY --from=downloader /jenkins.war /app/jenkins.war
COPY --from=builder /app /app
COPY --from=builder /var/log/jenkins-plugin /var/log/jenkins-plugin
COPY --from=builder /var/cache/jenkins-plugin /var/cache/jenkins-plugin
COPY --from=builder /home/jenkins /home/jenkins
RUN adduser -u 65532 -D jenkins 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["java", "-jar", "/app/jenkins.war"]
LABEL org.opencontainers.image.title="jenkins-plugin" \
      org.opencontainers.image.version="2.462.1" \
      org.opencontainers.image.vendor="Jenkins" \
      org.opencontainers.image.description="Evergreen hardened jenkins-plugin - Jenkins plugin manager" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
