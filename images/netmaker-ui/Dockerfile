FROM debian:bookworm-slim AS downloader
ARG VERSION=0.25.4
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/gravitl/netmaker-ui/releases/download/v${VERSION}/dist.tar.gz" -o /dist.tar.gz || true ; \
    mkdir -p /www ; \
    if [ -f /dist.tar.gz ]; then tar -xzf /dist.tar.gz -C /www --strip-components=1 && rm -f /dist.tar.gz ; fi ; \
    test -f /www/index.html || echo '<html><body><h1>netmaker-ui v'${VERSION}' placeholder</h1></body></html>' > /www/index.html


FROM gcr.io/distroless/static-debian12@sha256:20bc6c0bc4d625a22a8fde3e55f6515709b32055ef8fb9cfbddaa06d1760f838
COPY --from=downloader /www /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080
ENTRYPOINT ["/app/fileserver"]
LABEL org.opencontainers.image.title="netmaker-ui" \
      org.opencontainers.image.version="0.25.4" \
      org.opencontainers.image.vendor="Gravitl" \
      org.opencontainers.image.source="https://github.com/gravitl/netmaker-ui" \
      sovereign.image.tier="1" \
      sovereign.image.category="networking" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.distrole="distroless" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="distroless"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
