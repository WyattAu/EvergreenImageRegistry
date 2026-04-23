
FROM debian:bookworm-slim AS downloader
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/ArcticLampyrid/stalwart/releases/download/v0.9.0/stalwart-x86_64-unknown-linux-musl" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary





FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/stalwart
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65532:65532
WORKDIR /app
EXPOSE 443
LABEL org.opencontainers.image.title="stalwart"       org.opencontainers.image.description="Stalwart Mail Server - all-in-one mail server written in Rust"       org.opencontainers.image.version="0.9.0"       org.opencontainers.image.vendor="ArcticLampyrid"       org.opencontainers.image.source="https://github.com/ArcticLampyrid/stalwart"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM