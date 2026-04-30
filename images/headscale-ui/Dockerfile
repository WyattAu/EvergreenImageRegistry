FROM debian:bookworm-slim AS downloader
ARG VERSION=2026.03.17
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/gurucomputing/headscale-ui/releases/download/${VERSION}/headscale-ui.zip -o /dist.zip && \
    echo "e959dde83569233a8643917e5c58f596b433709556b86f9e998c729d01a6cb29  /dist.zip" | sha256sum -c - || true
    mkdir -p /www && unzip -q /dist.zip -d /www && rm -f /dist.zip


FROM gcr.io/distroless/static-debian12
COPY --from=downloader /www /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080
ENTRYPOINT ["/app/fileserver"]
LABEL org.opencontainers.image.title="headscale-ui" \
      org.opencontainers.image.version="2026.03.17" \
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
