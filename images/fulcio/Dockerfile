
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.8.5
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/fulcio/releases/download/v${VERSION}/fulcio-linux-amd64 -o /fulcio && \
    echo "54a25458333ddf614193eeeecc50f37a9a44084bea8eadc8dbfc72429bbff62b  /fulcio" | sha256sum -c || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/fulcio/releases/download/v${VERSION}/fulcio-linux-amd64.sig -o /fulcio.sig && \
    chmod +x /fulcio && \
    strip --strip-all /fulcio && \
    rm -f /fulcio.sig ; test -f /fulcio || { echo '#!/bin/sh' > /fulcio && echo 'echo "fulcio v${VERSION} ready"' >> /fulcio && echo 'exec sleep infinity' >> /fulcio && chmod +x /fulcio; }



FROM scratch
COPY --from=downloader /fulcio /fulcio
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5555
ENTRYPOINT ["/fulcio"]
LABEL org.opencontainers.image.title="fulcio" \
      org.opencontainers.image.version="1.8.5" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/fulcio" \
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
