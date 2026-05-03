ARG TARGETARCH
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS downloader
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

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=1.22.0
RUN apk add --no-cache ca-certificates git tzdata || true && \
    adduser -D -u 65532 git 2>/dev/null || true && \
    mkdir -p /app /var/lib/gitea /var/log/gitea /etc/gitea /var/cache/gitea 2>/dev/null || true
COPY --from=downloader /tmp/gitea /usr/local/bin/gitea
RUN chown -R 65532:65532 /app /var/lib/gitea /var/log/gitea /etc/gitea /var/cache/gitea 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 3000 22

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:22/ || exit 1
ENTRYPOINT ["/usr/local/bin/gitea"]
CMD ["web", "-c", "/etc/gitea/app.ini"]
LABEL org.opencontainers.image.title="source-control" \
      org.opencontainers.image.description="Source control management - Gitea lightweight Git server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Gitea" \
      org.opencontainers.image.source="https://about.gitea.com/" \
      evergreen.image.tier="2" \
      evergreen.image.category="scm" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.wolfi="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
