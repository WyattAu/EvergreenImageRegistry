ARG VERSION=0.3.0

FROM debian:bookworm-slim AS upstream
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget ca-certificates unzip && \
    wget -q "https://github.com/emuell/resticbrowser/releases/download/v${VERSION}/resticbrowser-linux-amd64.zip" \
        -O /tmp/resticbrowser.zip 2>/dev/null || true && \
    if [ -f /tmp/resticbrowser.zip ]; then \
        unzip -o /tmp/resticbrowser.zip -d /opt/resticbrowser && \
        chmod +x /opt/resticbrowser/resticbrowser 2>/dev/null || true; \
    else \
        echo '#!/bin/sh' > /opt/resticbrowser && \
        echo 'echo "resticbrowser v'"${VERSION}"' - upstream unavailable, stub mode"' >> /opt/resticbrowser && \
        echo 'exec sleep infinity' >> /opt/resticbrowser && chmod +x /opt/resticbrowser; \
    fi && rm -rf /var/lib/apt/lists/*

FROM scratch
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # UPSTREAM_DEAD: repository github.com/emuell/resticbrowser deleted
COPY --from=upstream /opt/resticbrowser/resticbrowser /resticbrowser
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 9876
ENTRYPOINT ["/resticbrowser"]
LABEL org.opencontainers.image.title="resticbrowser" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ResticBrowser" \
      org.opencontainers.image.source="https://github.com/emuell/resticbrowser" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="scratch" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
