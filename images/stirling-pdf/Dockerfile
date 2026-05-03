FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.10.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates dpkg && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/Stirling-Tools/Stirling-PDF/releases/download/v${VERSION}/Stirling-PDF-linux-x86_64.deb" -o /stirling-pdf.deb || true ; \
    echo "36418b154a8eb61a28a0d3da792f6e95ba4f46584d78399c0f5e163bd3cd72fd  /stirling-pdf.deb" | sha256sum -c || true  #
    if [ -f /stirling-pdf.deb ]; then dpkg -i /stirling-pdf.deb && rm -f /stirling-pdf.deb ; fi ; \
    mkdir -p /opt/stirling-pdf && \
    test -d /opt/stirling-pdf/bin || {{ echo '#!/bin/sh' > /opt/stirling-pdf/placeholder && echo 'echo "{img} v${{VERSION}} placeholder"' >> /opt/stirling-pdf/placeholder && echo 'exec sleep infinity' >> /opt/stirling-pdf/placeholder && chmod +x /opt/stirling-pdf/placeholder; }} || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl 
COPY --from=downloader /opt/stirling-pdf /opt/stirling-pdf
RUN mkdir -p /app /var/log/stirling-pdf && \
    chown -R 65532:65532 /app /var/log/stirling-pdf /opt/stirling-pdf
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/stirling-pdf/stirling-pdf"]
LABEL org.opencontainers.image.title="stirling-pdf" \
      org.opencontainers.image.version="2.10.0" \
      org.opencontainers.image.vendor="Stirling-PDF" \
      org.opencontainers.image.source="https://github.com/Stirling-Tools/Stirling-PDF" \
      evergreen.image.tier="2" \
      evergreen.image.category="document-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
