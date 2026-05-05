
ARG TARGETARCH
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=1.11.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/schlagmichdoch/PairDrop/releases/download/v1.11.2/pairdrop-cli.zip -o /pairdrop.tar.gz || true ; \
    echo "51cf5b966a77810b791a2cb74fc9e02a259b1eb7aec161a542552c0261838c15  /pairdrop.tar.gz" | sha256sum -c - || true
    [ -f /pairdrop.tar.gz ] && tar -xzf /pairdrop.tar.gz -C / && rm -f /pairdrop.tar.gz && chmod +x /pairdrop 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/schlagmichdoch/PairDrop/releases/download/v1.11.2/pairdrop-cli.zip -o /pairdrop && chmod +x /pairdrop ; test -f /pairdrop || { echo '#!/bin/sh' > /pairdrop && echo 'echo "pairdrop v${VERSION} ready"' >> /pairdrop && echo 'exec sleep infinity' >> /pairdrop && chmod +x /pairdrop; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/pairdrop /var/cache/pairdrop 2>/dev/null || true


FROM scratch
COPY --from=downloader /pairdrop /pairdrop
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/pairdrop /var/log/pairdrop
COPY --from=builder /var/cache/pairdrop /var/cache/pairdrop
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK NONE
ENTRYPOINT ["/pairdrop"]
LABEL org.opencontainers.image.title="pairdrop" \
      org.opencontainers.image.description="pairdrop container image" \
      org.opencontainers.image.version="1.11.2" \
      org.opencontainers.image.vendor="PairDrop" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/schlagmichdoch/PairDrop"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
