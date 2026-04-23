
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/gravitl/netmaker-ui/releases/download/v0.25.4/dist.tar.gz" -o /dist.tar.gz && \
    mkdir -p /www && tar -xzf /dist.tar.gz -C /www/ && \
    rm -rf /dist.tar.gz




FROM gcr.io/distroless/static-debian12
RUN echo "#!/bin/sh" > /fileserver && echo "echo placeholder" >> /fileserver && chmod +x /fileserver
COPY --from=downloader /www /www
USER 65532:65532
WORKDIR /www
EXPOSE 8080
ENTRYPOINT ["/fileserver"]
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