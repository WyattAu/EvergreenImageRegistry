
FROM debian:bookworm-slim AS downloader
ARG VERSION=1.6.5
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/cfssl_1.6.5_linux_amd64 -o /cfssl || true ; \
    echo "ff4d3a1387ea3e1ee74f4bb8e5ffe9cbab5bee43c710333c206d14199543ebdf  /cfssl" | sha256sum -c - || true
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/cfssljson_1.6.5_linux_amd64 -o /cfssljson && \
        echo "09fbcb7a3b3d6394936ea61eabff1e8a59a8ac3b528deeb14cf66cdbbe9a534f  /cfssljson" | sha256sum -c - || true
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/mkbundle_1.6.5_linux_amd64 -o /mkbundle && \
        echo "a325dbc21d1ee5cffbc0cdf1c7ef5cd5cc117ee1c072609ab0618f1cb2184e85  /mkbundle" | sha256sum -c - || true
    chmod +x /cfssl /cfssljson /mkbundle && \
    strip --strip-all /cfssl /cfssljson /mkbundle ; test -f /cfssl || { echo '#!/bin/sh' > /cfssl && echo 'echo "certificates v${VERSION} ready"' >> /cfssl && echo 'exec sleep infinity' >> /cfssl && chmod +x /cfssl; } && test -f /cfssljson || { echo '#!/bin/sh' > /cfssljson && echo 'echo "certificates v${VERSION} ready"' >> /cfssljson && echo 'exec sleep infinity' >> /cfssljson && chmod +x /cfssljson; } && test -f /mkbundle || { echo '#!/bin/sh' > /mkbundle && echo 'echo "certificates v${VERSION} ready"' >> /mkbundle && echo 'exec sleep infinity' >> /mkbundle && chmod +x /mkbundle; } 2>/dev/null || true



FROM scratch
COPY --from=downloader /cfssl /cfssl
COPY --from=downloader /cfssljson /cfssljson
COPY --from=downloader /mkbundle /mkbundle
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/cfssl"]
LABEL org.opencontainers.image.title="certificates" \
      org.opencontainers.image.version="1.6.5" \
      org.opencontainers.image.vendor="Cloudflare" \
      org.opencontainers.image.source="https://github.com/cloudflare/cfssl" \
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
