FROM debian:bookworm-slim AS downloader
ARG VERSION=0.9.5
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://gitlab.com/api/v4/projects/famedly%2Fconduit/packages/generic/conduit-v0.9.x/v${VERSION}/conduit-x86_64-unknown-linux-musl" \
    -o /tmp/conduit && \
    chmod +x /tmp/conduit && \
    strip /tmp/conduit 2>/dev/null || true

FROM scratch
COPY --from=downloader /tmp/conduit /usr/local/bin/conduit
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 6167
ENTRYPOINT ["/usr/local/bin/conduit"]
LABEL org.opencontainers.image.title="conduit" \
      org.opencontainers.image.description="Conduit - lightweight Matrix homeserver written in Rust" \
      org.opencontainers.image.version="0.9.5" \
      org.opencontainers.image.vendor="Famedly" \
      org.opencontainers.image.source="https://gitlab.com/famedly/conduit" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
