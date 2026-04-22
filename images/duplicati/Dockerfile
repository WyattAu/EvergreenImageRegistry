ARG VERSION=2.1.0.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dot.net/v1/dotnet-install.sh" -o /dotnet-install.sh && \
    chmod +x /dotnet-install.sh && \
    /dotnet-install.sh --channel 8.0 --runtime dotnet --install-dir /usr/share/dotnet && \
    rm /dotnet-install.sh
RUN curl -fsSL "https://github.com/duplicati/duplicati/releases/download/v2.1.0.1/duplicati-2.1.0.1-linux-x64-gui.zip" -o /duplicati.zip && \
    unzip -q /duplicati.zip -d /opt/duplicati && rm /duplicati.zip

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://dot.net/v1/dotnet-install.sh" -o /dotnet-install.sh && \
    chmod +x /dotnet-install.sh && \
    /dotnet-install.sh --channel 8.0 --runtime dotnet --install-dir /usr/share/dotnet && \
    rm /dotnet-install.sh
COPY --from=builder /opt/duplicati /opt/duplicati
RUN mkdir -p /app /var/log/duplicati /var/cache/duplicati /root/.config/Duplicati \
    && chown -R 65534:65534 /app /var/log/duplicati /var/cache/duplicati
USER 65534:65534
WORKDIR /app
ENV DOTNET_ROOT=/usr/share/dotnet
ENV PATH="$PATH:/usr/share/dotnet"
EXPOSE 8200
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8200"]
ENTRYPOINT ["dotnet", "/opt/duplicati/Duplicati.Server.exe"]
LABEL org.opencontainers.image.title="duplicati" \
      org.opencontainers.image.version="2.1.0.1" \
      org.opencontainers.image.vendor="Duplicati" \
      org.opencontainers.image.source="https://github.com/duplicati/duplicati" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
