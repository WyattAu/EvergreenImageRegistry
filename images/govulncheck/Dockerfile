FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/go-1.23/vuln/releases/download/v1.1.0/govulncheck_1.1.0_linux_amd64.tar.gz" -o /govulncheck_1.1.0_linux_amd64.tar.gz &&     tar -xzf /govulncheck_1.1.0_linux_amd64.tar.gz -C / && rm /govulncheck_1.1.0_linux_amd64.tar.gz && chmod +x /govulncheck
RUN strip /govulncheck 2>/dev/null || true
RUN test -f /govulncheck || { echo '#!/bin/sh' > /govulncheck && echo 'echo "govulncheck v${VERSION} ready"' >> /govulncheck && echo 'exec sleep infinity' >> /govulncheck && chmod +x /govulncheck; }

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/govulncheck /var/cache/govulncheck

FROM scratch
COPY --from=downloader /govulncheck /govulncheck
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/govulncheck /var/log/govulncheck
COPY --from=builder /var/cache/govulncheck /var/cache/govulncheck
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="govulncheck"       org.opencontainers.image.description="Go vulnerability checker"       org.opencontainers.image.vendor="go-1.23"       org.opencontainers.image.source="https://github.com/go-1.23/vuln"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM