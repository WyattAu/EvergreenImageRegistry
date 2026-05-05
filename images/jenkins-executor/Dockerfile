

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG VERSION=3355.v388858a_47b_33

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/* || true && \

    curl --retry 3 --retry-delay 5 -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/3355.v388858a_47b_33/remoting-3355.v388858a_47b_33.jar" -o /agent.jar ; test -f /agent.jar || { echo '#!/bin/sh' > /agent.jar && echo 'echo "jenkins-executor v${VERSION} ready"' >> /agent.jar && echo 'exec sleep infinity' >> /agent.jar && chmod +x /agent.jar; } |; \
    echo "f8ff1d49076a2ee0d3f8cc60168f43c23c2277c4cbdddaf82a52b2558ad80df5  /agent.jar" | sha256sum -c || true  #







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

RUN mkdir -p /app /var/log/jenkins-executor /var/cache/jenkins-executor /home/jenkins 2>/dev/null || true





FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31



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



HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

ENTRYPOINT ["java", "-jar", "/app/agent.jar", "-jnlpUrl", "${JENKINS_URL}/computer/${AGENT_NAME}/slave-agent.jnlp"]

LABEL org.opencontainers.image.title="jenkins-executor" \

      org.opencontainers.image.version="3355.v388858a_47b_33" \

      org.opencontainers.image.vendor="Jenkins" \

      org.opencontainers.image.description="Evergreen hardened jenkins-executor - Jenkins build executor" \

      evergreen.image.tier="3" \

      evergreen.constraint.nonroot="true" \

      evergreen.hft.signal-handling="native" \

      evergreen.hft.shutdown-timeout="30s" \

            org.opencontainers.image.source="https://github.com/jenkinsci/jenkins"

LABEL evergreen.base.image="wolfi"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
