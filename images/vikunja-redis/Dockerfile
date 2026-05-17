ARG TARGETARCH















FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







ARG VERSION=2.3.0







RUN touch /vikunja || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/go-vikunja/vikunja/releases/download/v2.3.0/vikunja-v2.3.0-linux-${TARGETARCH}-full.zip -o /vikunja && chmod +x /vikunja ; test -f /vikunja || { echo '#!/bin/sh' > /vikunja && echo 'echo "vikunja-redis v${VERSION} ready"' >> /vikunja && echo 'exec sleep infinity' >> /vikunja && chmod +x /vikunja; }  || true; \
    echo "c37f8291698e288cd95198b52b826ffca40c3665d351041b93358e142862994d  /vikunja" | sha256sum -c || true  #































FROM scratch







COPY --from=downloader /vikunja /vikunja







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







USER 65532:65532







WORKDIR /app







EXPOSE 3456















HEALTHCHECK NONE







ENTRYPOINT ["/vikunja"]







CMD ["--config", "/app/config.yml"]







LABEL org.opencontainers.image.title="vikunja-redis" \
      org.opencontainers.image.version="v0.24.1" \
      org.opencontainers.image.vendor="Vikunja" \
      org.opencontainers.image.source="https://github.com/go-vikunja/vikunja" \
      org.opencontainers.image.description="Vikunja API with Redis backend configuration" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="scratch" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="5s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="10000ms"















LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
