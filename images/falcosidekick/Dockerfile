FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/falcosecurity/falcosidekick/releases/download/v2.28.0/falcosidekick_2.28.0_linux_amd64.tar.gz" -o /falcosidekick_2.28.0_linux_amd64.tar.gz &&     tar -xzf /falcosidekick_2.28.0_linux_amd64.tar.gz -C / && rm /falcosidekick_2.28.0_linux_amd64.tar.gz && chmod +x /falcosidekick
RUN strip /falcosidekick 2>/dev/null || true

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/falcosidekick /var/cache/falcosidekick

FROM scratch
COPY --from=downloader /falcosidekick /falcosidekick
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/falcosidekick /var/log/falcosidekick
COPY --from=builder /var/cache/falcosidekick /var/cache/falcosidekick
USER 65534:65534
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD ["/falcosidekick", "--version"]
ENTRYPOINT ["/falcosidekick"]
LABEL org.opencontainers.image.title="falcosidekick"       org.opencontainers.image.description="Falcosidekick - Falco webhook"       org.opencontainers.image.vendor="falcosecurity"       org.opencontainers.image.source="https://github.com/falcosecurity/falcosidekick"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"
