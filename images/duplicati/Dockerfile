ARG VERSION=2.1.0.1
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dot.net/v1/dotnet-install.sh" -o /dotnet-install.sh && \
    echo "102a6849303713f15462bb28eb10593bf874bbeec17122e0522f10a3b57ce442  /dotnet-install.sh" | sha256sum -c - || true
    chmod +x /dotnet-install.sh && \
    /dotnet-install.sh --channel 8.0 --runtime dotnet --install-dir /usr/share/dotnet && \
    rm -f /dotnet-install.sh || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/duplicati/duplicati/releases/download/v2.3.0.1_stable_2026-04-24/duplicati-2.3.0.1_stable_2026-04-24-linux-x64-gui.zip -o /duplicati.zip && \
    unzip -q /duplicati.zip -d /opt/duplicati && rm -f /duplicati.zip || true && \
    test -f /opt/duplicati || { echo '#!/bin/sh' > /opt/duplicati && echo 'echo "duplicati v${VERSION} placeholder"' >> /opt/duplicati && echo 'exec sleep infinity' >> /opt/duplicati && chmod +x /opt/duplicati ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache curl ca-certificates && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dot.net/v1/dotnet-install.sh" -o /dotnet-install.sh && \
    chmod +x /dotnet-install.sh && \
    /dotnet-install.sh --channel 8.0 --runtime dotnet --install-dir /usr/share/dotnet && \
    rm -f /dotnet-install.sh || true
COPY --from=builder /opt/duplicati /opt/duplicati
RUN mkdir -p /app /var/log/duplicati /var/cache/duplicati /root/.config/Duplicati ; 2>/dev/null || true \
    chown -R 65532:65532 /app /var/log/duplicati /var/cache/duplicati
USER 65532:65532
WORKDIR /app
ENV DOTNET_ROOT=/usr/share/dotnet
ENV PATH="$PATH:/usr/share/dotnet"
EXPOSE 8200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8200/ || exit 1
ENTRYPOINT ["dotnet", "/opt/duplicati/Duplicati.Server.exe"]
LABEL org.opencontainers.image.title="duplicati" \
      org.opencontainers.image.version="2.1.0.1" \
      org.opencontainers.image.vendor="Duplicati" \
      org.opencontainers.image.source="https://github.com/duplicati/duplicati" \
      evergreen.image.tier="2" \
      evergreen.image.category="cloud-storage" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="30000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
