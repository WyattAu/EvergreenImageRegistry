ARG TARGETARCH
FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
ARG TARGETARCH
ARG VERSION=1.22.0
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates xz || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://dl.gitea.io/gitea/${VERSION}/gitea-${VERSION}-linux-${TARGETARCH}.xz" \
    -o /tmp/gitea.xz && \
    echo "b58e02e9e863a0191f26a26fbe6ef7e24c4c9917940c21957e6713cadcc5b9fd  /tmp/gitea.xz" | sha256sum -c - && \
    xz -d /tmp/gitea.xz && \
    chmod +x /tmp/gitea && \
    strip /tmp/gitea || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=1.22.0
RUN apk add --no-cache ca-certificates git tzdata || true && \
    adduser -D -u 65532 git 2>/dev/null || true && \
    mkdir -p /app /var/lib/gitea /var/log/gitea /etc/gitea /var/cache/gitea 2>/dev/null || true
COPY --from=downloader /tmp/gitea /usr/local/bin/gitea
RUN chown -R 65532:65532 /app /var/lib/gitea /var/log/gitea /etc/gitea /var/cache/gitea 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 3000 22
ENTRYPOINT ["/usr/local/bin/gitea"]
CMD ["web", "-c", "/etc/gitea/app.ini"]
LABEL org.opencontainers.image.title="source-control" \
      org.opencontainers.image.description="Source control management - Gitea lightweight Git server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://about.gitea.com/" \
      sovereign.image.tier="2" \
      sovereign.image.category="scm" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
