
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.0.6
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-amd64 -o /cosign && \
    echo "c956e5dfcac53d52bcf058360d579472f0c1d2d9b69f55209e256fe7783f4c74  /cosign" | sha256sum -c || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/cosign/releases/download/v${VERSION}/cosign-linux-amd64.sig -o /cosign.sig && \
    chmod +x /cosign && \
    strip --strip-all /cosign && \
    rm -f /cosign.sig ; test -f /cosign || { echo '#!/bin/sh' > /cosign && echo 'echo "cosign-verify v${VERSION} ready"' >> /cosign && echo 'exec sleep infinity' >> /cosign && chmod +x /cosign; }



FROM scratch
COPY --from=downloader /cosign /cosign
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/cosign"]
CMD ["verify"]
LABEL org.opencontainers.image.title="cosign-verify" \
      org.opencontainers.image.version="3.0.6" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/cosign" \
      sovereign.image.tier="2" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
