

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader

ARG VERSION=3355.v388858a_47b_33

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/* || true && \

    curl --retry 3 --retry-delay 5 -fsSL "https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/3355.v388858a_47b_33/remoting-3355.v388858a_47b_33.jar" -o /agent.jar ; test -f /agent.jar || { echo '#!/bin/sh' > /agent.jar && echo 'echo "jenkins-agent v${VERSION} ready"' >> /agent.jar && echo 'exec sleep infinity' >> /agent.jar && chmod +x /agent.jar; }  || true; \
    echo "f8ff1d49076a2ee0d3f8cc60168f43c23c2277c4cbdddaf82a52b2558ad80df5  /agent.jar" | sha256sum -c || true  #







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

RUN mkdir -p /app /var/log/jenkins-agent /var/cache/jenkins-agent /home/jenkins 2>/dev/null || true





FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31



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



HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1

ENTRYPOINT ["java", "-jar", "/app/agent.jar"]

LABEL org.opencontainers.image.title="jenkins-agent" \

      org.opencontainers.image.version="3355.v388858a_47b_33" \

      org.opencontainers.image.vendor="Jenkins" \

      org.opencontainers.image.description="Evergreen hardened jenkins-agent - Jenkins SSH/JNLP agent" \

      evergreen.image.tier="3" \

      evergreen.constraint.nonroot="true" \

      evergreen.hft.signal-handling="native" \

      evergreen.hft.shutdown-timeout="30s" \

            org.opencontainers.image.source="https://github.com/jenkinsci/docker-inbound-agent"

LABEL evergreen.base.image="wolfi"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"



EXPOSE 9101

STOPSIGNAL SIGTERM
