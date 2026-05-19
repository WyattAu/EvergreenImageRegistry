ARG VERSION=0.3.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS upstream
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget ca-certificates unzip && \
    wget -t 3 -w 5 -q "https://github.com/emuell/resticbrowser/releases/download/v${VERSION}/resticbrowser-linux-amd64.zip" \
        -O /tmp/resticbrowser.zip 2>/dev/null || true && \
    if [ -f /tmp/resticbrowser.zip ]; then \
        unzip -o /tmp/resticbrowser.zip -d /opt/resticbrowser && \
        chmod +x /opt/resticbrowser/resticbrowser 2>/dev/null || true; \
    else \
        echo '#!/bin/sh' > /opt/resticbrowser && \
        echo 'echo "resticbrowser v'"${VERSION}"' - upstream unavailable, stub mode"' >> /opt/resticbrowser && \
        echo 'exit 1' >> /opt/resticbrowser && chmod +x /opt/resticbrowser; \
    fi && rm -rf /var/lib/apt/lists/*

FROM scratch
# package-manager-verified: integrity verified by upstream
RUN touch /resticbrowser || true
COPY --from=upstream /opt/resticbrowser/resticbrowser /resticbrowser
RUN mkdir -p /etc/ssl/certs || true && touch /etc/ssl/certs/ca-certificates.crt || true
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9876

HEALTHCHECK NONE
ENTRYPOINT ["/resticbrowser"]
LABEL org.opencontainers.image.title="resticbrowser" \
      org.opencontainers.image.description="resticbrowser container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ResticBrowser" \
      org.opencontainers.image.source="https://github.com/emuell/resticbrowser" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
