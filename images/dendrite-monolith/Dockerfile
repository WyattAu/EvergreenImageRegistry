FROM debian:bookworm-slim AS downloader
ARG VERSION=0.13.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/element-hq/dendrite/releases/download/v${VERSION}/dendrite-monolith-linux-amd64" \
    -o /tmp/dendrite && \
    chmod +x /tmp/dendrite && \
    strip /tmp/dendrite

FROM scratch
COPY --from=downloader /tmp/dendrite /usr/local/bin/dendrite
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8008
ENTRYPOINT ["/usr/local/bin/dendrite"]
LABEL org.opencontainers.image.title="dendrite-monolith" \
      org.opencontainers.image.description="Dendrite Monolith - Dendrite Matrix homeserver in monolith mode" \
      org.opencontainers.image.version="0.13.1" \
      org.opencontainers.image.vendor="Element" \
      org.opencontainers.image.source="https://github.com/element-hq/dendrite" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
