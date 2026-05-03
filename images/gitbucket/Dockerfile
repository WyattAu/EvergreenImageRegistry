ARG VERSION=4.40.0
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gitbucket/gitbucket/releases/download/${VERSION}/gitbucket.war" -o /tmp/gitbucket.war || true && \
    echo "7e124543a48f3d349b2e93dddbaace1a7122a18b1a11b0e6ab403f0645d646d5  /tmp/gitbucket.war" | sha256sum -c || true
RUN test -f /tmp/gitbucket.war && test -s /tmp/gitbucket.war || { echo "ERROR: gitbucket.war not downloaded" >&2; exit 1; }

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates
RUN apk add --no-cache java-21-default-jdk 2>/dev/null || \
    apk add --no-cache openjdk-21-jdk-headless 2>/dev/null || true
RUN addgroup -S -g 10000 gitbucket 2>/dev/null || true ; adduser -u 65532 -G gitbucket -D -h /opt/gitbucket -s /bin/false gitbucket
RUN mkdir -p /opt/gitbucket /var/log/gitbucket /var/data/gitbucket && \
    chown -R 65532:65532 /opt/gitbucket /var/log/gitbucket /var/data/gitbucket
COPY --from=builder /tmp/gitbucket.war /opt/gitbucket/gitbucket.war
USER 65532:65532
ENV GITBUCKET_HOME="/var/data/gitbucket"
WORKDIR /opt/gitbucket
EXPOSE 8080
LABEL org.opencontainers.image.title="gitbucket" \
      org.opencontainers.image.description="GitBucket - Scala-based Git platform" \
      org.opencontainers.image.version="4.40.0" \
      org.opencontainers.image.vendor="GitBucket" \
      org.opencontainers.image.source="https://github.com/gitbucket/gitbucket" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["java", "-jar", "/opt/gitbucket/gitbucket.war"]
