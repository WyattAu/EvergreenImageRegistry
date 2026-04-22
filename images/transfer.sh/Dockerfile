FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/dutchcoders/transfer.sh/releases/download/v1.7.1/transfer.sh-linux-amd64" -o /transfer.sh && \
    chmod +x /transfer.sh && strip /transfer.sh

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app/data /var/log/transfer /var/cache/transfer /tmp

FROM scratch
COPY --from=downloader /transfer.sh /transfer.sh
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/transfer /var/log/transfer
COPY --from=builder /var/cache/transfer /var/cache/transfer
COPY --from=builder /tmp /tmp
USER 65534:65534
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/transfer.sh", "--version"] || exit 0
ENTRYPOINT ["/transfer.sh"]
LABEL org.opencontainers.image.title="transfer.sh" \
      org.opencontainers.image.description="transfer.sh - Easy file sharing from CLI" \
      org.opencontainers.image.vendor="dutchcoders" \
      org.opencontainers.image.source="https://github.com/dutchcoders/transfer.sh" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
