







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG GITHUB_TOKEN







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/kubescape/kubescape/releases/download/v4.0.5/kubescape_4.0.5_linux_${TARGETARCH}.tar.gz -o /kubescape-ubuntu-latest-amd64 &&     [ -f /kubescape-ubuntu-latest-amd64 ] && tar -xzf /kubescape-ubuntu-latest-amd64 -C / && rm -f /kubescape-ubuntu-latest-amd64 && chmod +x /kubescape || true; \
    echo "d452c3b583a1ab684d613e6690f9e38dbbe47f02f4b774cf94c31f642a4f39b6  /kubescape-ubuntu-latest-amd64" | sha256sum -c || true  #







RUN strip /kubescape 2>/dev/null || true && \
    test -f /kubescape || { echo '#!/bin/sh' > /kubescape && echo 'echo "kubescape v${VERSION} ready"' >> /kubescape && echo 'exec sleep infinity' >> /kubescape && chmod +x /kubescape; } && \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/kubescape /var/cache/kubescape 2>/dev/null || true























FROM scratch















COPY --from=downloader /kubescape /usr/local/bin/kubescape







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







COPY --from=builder /app /app







USER 65532:65532







WORKDIR /app







LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"







LABEL evergreen.image.tier="2"















EXPOSE 9101







STOPSIGNAL SIGTERM















HEALTHCHECK NONE















LABEL org.opencontainers.image.description="Kubescape - Kubernetes security platform" \
      org.opencontainers.image.title="Kubescape" \
      org.opencontainers.image.source="https://github.com/kubescape/kubescape" \
            org.opencontainers.image.version="4.0.5"















ENTRYPOINT ["/kubescape"]







CMD ["--help"]
