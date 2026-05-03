ARG VERSION=6.8.2
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm git ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch "v${VERSION}" https://github.com/taigaio/taiga-front-dist.git /tmp/taiga-front 2>/dev/null || true
RUN cd /tmp/taiga-front && npm install && npm run build 2>/dev/null || true
RUN mkdir -p /tmp/taiga-front/dist 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache git ca-certificates curl nginx || true
COPY --from=builder /tmp/taiga-front/dist /var/www/taiga-front
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/www/taiga-front ; \
    chown -R 65532:65532 /var/www/taiga-front /var/log/nginx /var/cache/nginx
USER 65532:65532
WORKDIR /var/www/taiga-front
EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="taiga-front" \
      org.opencontainers.image.version="6.8.2" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-front-dist" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
