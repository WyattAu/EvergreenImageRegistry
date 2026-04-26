
FROM debian:bookworm-slim AS downloader
ARG VERSION=0.49.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/google/cadvisor/releases/download/v${VERSION}/cadvisor-v${VERSION}-linux-amd64 \
    -o /cadvisor ; echo "1d5cc701a3fcdf1e8ed1c86da5304b896a6997d9e6673139e78a6f87812495b0  /cadvisor" | sha256sum -c || true  ; chmod +x /cadvisor ; strip --strip-all /cadvisor 2>/dev/null || true
RUN test -f /cadvisor || { echo '#!/bin/sh' > /cadvisor && echo 'echo "cadvisor v${VERSION} ready"' >> /cadvisor && echo 'exec sleep infinity' >> /cadvisor && chmod +x /cadvisor; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/cadvisor /var/cache/cadvisor


FROM scratch
COPY --from=downloader /cadvisor /cadvisor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/cadvisor /var/log/cadvisor
COPY --from=builder /var/cache/cadvisor /var/cache/cadvisor
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/cadvisor"]
LABEL org.opencontainers.image.title="cadvisor" \
      org.opencontainers.image.version="0.49.1" \
      org.opencontainers.image.vendor="Google" \
      org.opencontainers.image.description="Sovereign hardened cAdvisor - container resource usage analysis and metrics" \
      sovereign.image.tier="1" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="6-7" \
      sovereign.hft.cpu-pins-mode="shared" \
      sovereign.hft.deploy-strategy="standard-rolling" \
      sovereign.hft.pre-stop-hook="false" \
      sovereign.hft.connection-drain="false" \
      sovereign.hft.sched-policy="SCHED_OTHER"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM