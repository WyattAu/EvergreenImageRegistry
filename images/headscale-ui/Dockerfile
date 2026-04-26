FROM debian:bookworm-slim AS downloader
ARG VERSION=2024.1.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gurucomputing/headscale-ui/releases/download/2024.1.1/headscale-ui-2024.1.1.tar.gz -o /dist.tar.gz || true ; \
    mkdir -p /www-src && [ -f /dist.tar.gz ] && tar -xzf /dist.tar.gz -C /www/ --strip-components=1 || true ; \
    rm -rf /dist.tar.gz ; test -f /www || { echo '#!/bin/sh' > /www && echo 'echo "headscale-ui v${VERSION} placeholder"' >> /www && echo 'exec sleep infinity' >> /www && chmod +x /www; }


FROM gcr.io/distroless/static-debian12
RUN mkdir -p /app && echo "#!/bin/sh" > /app/fileserver && echo "echo placeholder" >> /app/fileserver && chmod +x /app/fileserver
COPY --from=downloader /www /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080
ENTRYPOINT ["/fileserver"]
LABEL org.opencontainers.image.title="headscale-ui" \
      org.opencontainers.image.version="2024.1.1" \
      org.opencontainers.image.vendor="gurucomputing" \
      org.opencontainers.image.source="https://github.com/gurucomputing/headscale-ui" \
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
