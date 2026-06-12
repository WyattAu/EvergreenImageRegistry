ARG VERSION=25.04.9.4.1
ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM --platform=linux/amd64 debian:bookworm-slim
COPY --from=shim /shim /usr/local/bin/shim

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy collabora rootfs extracted from upstream
COPY collabora-rootfs.tar /tmp/
RUN tar xf /tmp/collabora-rootfs.tar -C / 2>/dev/null || true && rm /tmp/collabora-rootfs.tar

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app

EXPOSE 9980 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9980"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "coolwsd", "--o:security.capabilities=false", "--o:security.seccomp=false", "--o:child_root_path=/tmp/jails", "--o:ssl.enable=false", "--o:ssl.termination=true"]
LABEL org.opencontainers.image.title="collabora" \
      org.opencontainers.image.description="Collabora Online - LibreOffice-based online office suite" \
      org.opencontainers.image.version="25.04.9.4.1" \
      org.opencontainers.image.vendor="Collabora" \
      org.opencontainers.image.source="https://github.com/CollaboraOnline/online"
LABEL evergreen.base.image="debian-bookworm-slim" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true"
STOPSIGNAL SIGTERM
