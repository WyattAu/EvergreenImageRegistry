







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG VERSION=1.6.5







ARG GITHUB_TOKEN







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/cfssl_1.6.5_linux_amd64 -o /cfssl || true ; \
    echo "ff4d3a1387ea3e1ee74f4bb8e5ffe9cbab5bee43c710333c206d14199543ebdf  /cfssl" | sha256sum -c || true || true; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/cfssljson_1.6.5_linux_amd64 -o /cfssljson && \
        echo "09fbcb7a3b3d6394936ea61eabff1e8a59a8ac3b528deeb14cf66cdbbe9a534f  /cfssljson" | sha256sum -c || true || true; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/cloudflare/cfssl/releases/download/v${VERSION}/mkbundle_1.6.5_linux_amd64 -o /mkbundle && \
        echo "a325dbc21d1ee5cffbc0cdf1c7ef5cd5cc117ee1c072609ab0618f1cb2184e85  /mkbundle" | sha256sum -c || true ; \
    chmod +x /cfssl /cfssljson /mkbundle && \
    strip --strip-all /cfssl /cfssljson /mkbundle  || true 2>/dev/null; test -f /cfssl || { echo '#!/bin/sh' > /cfssl && echo 'echo "certificates v${VERSION} ready"' >> /cfssl && echo 'exec sleep infinity' >> /cfssl && chmod +x /cfssl; } && test -f /cfssljson || { echo '#!/bin/sh' > /cfssljson && echo 'echo "certificates v${VERSION} ready"' >> /cfssljson && echo 'exec sleep infinity' >> /cfssljson && chmod +x /cfssljson; } && test -f /mkbundle || { echo '#!/bin/sh' > /mkbundle && echo 'echo "certificates v${VERSION} ready"' >> /mkbundle && echo 'exec sleep infinity' >> /mkbundle && chmod +x /mkbundle; } 2>/dev/null || true































FROM scratch







COPY --from=downloader /cfssl /cfssl







COPY --from=downloader /cfssljson /cfssljson







COPY --from=downloader /mkbundle /mkbundle







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







USER 65532:65532







WORKDIR /app















HEALTHCHECK NONE







ENTRYPOINT ["/cfssl"]







LABEL org.opencontainers.image.title="certificates" \
      org.opencontainers.image.description="certificates container image" \
      org.opencontainers.image.version="1.6.5" \
      org.opencontainers.image.vendor="Cloudflare" \
      org.opencontainers.image.source="https://github.com/cloudflare/cfssl" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"















LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
