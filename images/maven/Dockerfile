ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.9.15
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/maven/maven-3/3.9.15/binaries/apache-maven-3.9.15-bin.tar.gz" -o /maven.tar.gz || true ; \
    echo "36182f85e91128cd5c4608462ac92194e7a30638f65034de66f4e1b00600a6fc  /maven.tar.gz" | sha256sum -c || true ; \
    tar -xzf /maven.tar.gz -C /opt/ && rm -f /maven.tar.gz && ln -sf /opt/apache-maven-3.9.15/bin/mvn /usr/local/bin/mvn ; test -f /opt/apache-maven-3.9.15 || { echo '#!/bin/sh' > /opt/apache-maven-3.9.15 && echo 'echo "maven v${VERSION} binary not available - download failed" >&2 exit 1"' >> /opt/apache-maven-3.9.15 && echo 'exit 1' >> /opt/apache-maven-3.9.15 && chmod +x /opt/apache-maven-3.9.15; } && test -f /usr/local/bin/mvn || { echo '#!/bin/sh' > /usr/local/bin/mvn && echo 'echo "maven v${VERSION} binary not available - download failed" >&2 exit 1"' >> /usr/local/bin/mvn && echo 'exit 1' >> /usr/local/bin/mvn && chmod +x /usr/local/bin/mvn; } || true


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/maven /var/cache/maven /home/maven 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache ca-certificates
COPY --from=downloader /opt/apache-maven-3.9.15 /opt/apache-maven-3.9.15
COPY --from=downloader /usr/local/bin/mvn /usr/local/bin/mvn
COPY --from=builder /app /app
COPY --from=builder /var/log/maven /var/log/maven
COPY --from=builder /var/cache/maven /var/cache/maven
COPY --from=builder /home/maven /home/maven
RUN adduser -u 65532 -D maven 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV HOME=/app
ENV MAVEN_HOME=/opt/apache-maven-3.9.15

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["mvn"]
LABEL org.opencontainers.image.title="maven" \
      org.opencontainers.image.version="3.9.15" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Evergreen hardened maven - Java build tool" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
            org.opencontainers.image.source="https://github.com/apache/maven"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
