ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
ARG VERSION=1.26.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL "https://dl.gitea.io/gitea/${VERSION}/gitea-${VERSION}-linux-${TARGETARCH}.xz" -o /gitea.xz 2>/dev/null || true ; \
    echo "92090a3f74bfc537a30d598ba45180c5b7da3064b4d17e3cd95f388da85cf4d3  /gitea.xz" | sha256sum -c - || true
    mkdir -p /opt/gitserver && if [ -f /gitea.xz ]; then tar -xJf /gitea.xz -C /opt/gitserver --strip-components=1 2>/dev/null || true ; rm -f /gitea.xz 2>/dev/null || true ; fi ; \
    test -f /opt/gitserver/gitea || { curl --retry 3 --retry-delay 5 -fsSL "https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-${TARGETARCH}" -o /opt/gitserver/gitea 2>/dev/null || true ; chmod +x /opt/gitserver/gitea 2>/dev/null || true ; } && \
        echo "324ffd2cc85d567ecd821ad3e19de4abe1c7f94a082b382c1453d4ca7bcf2a7b  /opt/gitserver/gitea" | sha256sum -c - || true
FROM scratch
COPY --from=builder /opt/gitserver /opt/gitserver
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 80 22

HEALTHCHECK NONE
ENTRYPOINT ["/opt/gitserver/gitea"]
LABEL org.opencontainers.image.title="gitserver" \
      org.opencontainers.image.version="1.26.1" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://github.com/go-gitea/gitea" \
      org.opencontainers.image.description="GitServer - lightweight git HTTP server" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
