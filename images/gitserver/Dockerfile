FROM debian:bookworm-slim AS builder
ARG VERSION=1.26.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates xz-utils && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 --connect-timeout 30 --max-time 300 -fsSL "https://dl.gitea.io/gitea/${VERSION}/gitea-${VERSION}-linux-amd64.xz" -o /gitea.xz 2>/dev/null || true ; \
    mkdir -p /opt/gitserver && if [ -f /gitea.xz ]; then tar -xJf /gitea.xz -C /opt/gitserver --strip-components=1 2>/dev/null || true ; rm -f /gitea.xz 2>/dev/null || true ; fi ; \
    test -f /opt/gitserver/gitea || { curl --retry 3 --retry-delay 5 -fsSL "https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64" -o /opt/gitserver/gitea 2>/dev/null || true ; chmod +x /opt/gitserver/gitea 2>/dev/null || true ; }
FROM scratch
COPY --from=builder /opt/gitserver /opt/gitserver
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 80 22
ENTRYPOINT ["/opt/gitserver/gitea"]
LABEL org.opencontainers.image.title="gitserver" \
      org.opencontainers.image.version="1.26.1" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://github.com/go-gitea/gitea" \
      org.opencontainers.image.description="GitServer - lightweight git HTTP server" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
