ARG VERSION=0.70.4

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/netbirdio/netbird/releases/download/v${VERSION}/netbird-ui-linux_${VERSION}_linux_amd64.tar.gz" \
    -o /tmp/netbird-ui.tar.gz && \
    mkdir -p /tmp/ui && tar -xzf /tmp/netbird-ui.tar.gz -C /tmp/ui && rm -f /tmp/netbird-ui.tar.gz

FROM scratch
ARG VERSION
COPY --from=builder /tmp/ui /ui
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /ui
EXPOSE 80
ENTRYPOINT ["sleep", "infinity"]
LABEL org.opencontainers.image.title="netbird-ui"       org.opencontainers.image.version="${VERSION}"       org.opencontainers.image.description="Sovereign hardened NetBird UI - static web dashboard assets"       org.opencontainers.image.vendor="NetBird"       sovereign.image.tier="1"       sovereign.image.category="networking"       sovereign.image.status="functional"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
