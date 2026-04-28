FROM debian:bookworm-slim AS downloader
ARG VERSION=0.9.3
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates zstd &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/foxcpp/maddy/releases/download/v${VERSION}/maddy-${VERSION}-x86_64-linux-musl.tar.zst -o /tmp/maddy.tar.zst && \
    tar --zstd -xf /tmp/maddy.tar.zst -C /tmp && \
    mv /tmp/maddy /usr/local/bin/maddy && chmod +x /usr/local/bin/maddy && strip /usr/local/bin/maddy


FROM scratch
COPY --from=downloader /usr/local/bin/maddy /usr/local/bin/maddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 587 993 143 465 25
LABEL org.opencontainers.image.title="maddy"       org.opencontainers.image.description="Maddy - all-in-one mail server written in Go"       org.opencontainers.image.version="0.9.3"       org.opencontainers.image.vendor="foxcpp"       org.opencontainers.image.source="https://github.com/foxcpp/maddy"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
