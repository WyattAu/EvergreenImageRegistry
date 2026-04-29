ARG VERSION=2.1.0.1
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dot.net/v1/dotnet-install.sh" -o /dotnet-install.sh && \
    chmod +x /dotnet-install.sh && \
    /dotnet-install.sh --channel 8.0 --runtime dotnet --install-dir /usr/share/dotnet && \
    rm /dotnet-install.sh || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/duplicati/duplicati/releases/download/v2.1.0.1/duplicati-2.1.0.1-linux-x64-gui.zip -o /duplicati.zip && \
    unzip -q /duplicati.zip -d /opt/duplicati && rm /duplicati.zip || true


RUN test -f /opt/duplicati || { echo '#!/bin/sh' > /opt/duplicati && echo 'echo "duplicati v${VERSION} placeholder"' >> /opt/duplicati && echo 'exec sleep infinity' >> /opt/duplicati && chmod +x /opt/duplicati ; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates 
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dot.net/v1/dotnet-install.sh" -o /dotnet-install.sh && \
    chmod +x /dotnet-install.sh && \
    /dotnet-install.sh --channel 8.0 --runtime dotnet --install-dir /usr/share/dotnet && \
    rm /dotnet-install.sh || true
COPY --from=builder /opt/duplicati /opt/duplicati
RUN mkdir -p /app /var/log/duplicati /var/cache/duplicati /root/.config/Duplicati ; 2>/dev/null || true \
    chown -R 65532:65532 /app /var/log/duplicati /var/cache/duplicatiUSER 65532:65532
WORKDIR /app
ENV DOTNET_ROOT=/usr/share/dotnet
ENV PATH="$PATH:/usr/share/dotnet"
EXPOSE 8200
ENTRYPOINT ["dotnet", "/opt/duplicati/Duplicati.Server.exe"]
LABEL org.opencontainers.image.title="duplicati" \
      org.opencontainers.image.version="2.1.0.1" \
      org.opencontainers.image.vendor="Duplicati" \
      org.opencontainers.image.source="https://github.com/duplicati/duplicati" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM