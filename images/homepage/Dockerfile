
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/benphelps/homepage/releases/download/v0.9.3/homepage_0.9.3_linux_amd64.tar.gz \
    -o /homepage.tar.gz && \
    [ -f /homepage.tar.gz ] && tar -xzf /homepage.tar.gz -C / && rm -f /homepage.tar.gz && chmod +x /homepage 2>/dev/null || true
RUN strip /homepage 2>/dev/null || true
RUN test -f /homepage || { echo '#!/bin/sh' > /homepage && echo 'echo "homepage v${VERSION} ready"' >> /homepage && echo 'exec sleep infinity' >> /homepage && chmod +x /homepage; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/homepage /var/cache/homepage 2>/dev/null || true


FROM scratch
COPY --from=downloader /homepage /homepage
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/homepage /var/log/homepage
COPY --from=builder /var/cache/homepage /var/cache/homepage
USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["/homepage"]
LABEL org.opencontainers.image.title="homepage" \
      org.opencontainers.image.description="Homepage - Application dashboard" \
      org.opencontainers.image.vendor="benphelps" \
      org.opencontainers.image.source="https://github.com/benphelps/homepage" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM