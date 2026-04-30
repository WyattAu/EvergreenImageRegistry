FROM debian:bookworm-slim AS downloader
ARG VERSION=0.8.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL \
    "https://gitlab.com/api/v4/projects/famedly%2Fconduit/packages/generic/conduit/v${VERSION}/conduit-x86_64-unknown-linux-musl" \
    -o /tmp/conduit && \
    chmod +x /tmp/conduit && \
    strip /tmp/conduit 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=0.8.0
RUN apk add --no-cache ca-certificates sqlite-libs || true
RUN addgroup -S -g 10000 conduit 2>/dev/null || true && \
    adduser -u 65532 -G conduit -D -h /app -s /bin/sh conduit 2>/dev/null || true
RUN mkdir -p /app/data /app/config 2>/dev/null || true
COPY --from=downloader /tmp/conduit /usr/local/bin/conduit
RUN chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 6167
ENTRYPOINT ["/usr/local/bin/conduit"]
LABEL org.opencontainers.image.title="conduit-admin" \
      org.opencontainers.image.description="Conduit Admin - Conduit Matrix homeserver with admin utilities" \
      org.opencontainers.image.version="0.8.0" \
      org.opencontainers.image.vendor="Famedly" \
      org.opencontainers.image.source="https://gitlab.com/famedly/conduit" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
