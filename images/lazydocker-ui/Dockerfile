







ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/jesseduffield/lazydocker/releases/download/v0.25.2/lazydocker_0.25.2_Linux_${TARGETARCH}.tar.gz -o /lazydocker_0.12.0_Linux_x86_64.tar.gz &&     [ -f /lazydocker_0.12.0_Linux_x86_64.tar.gz ] && tar -xzf /lazydocker_0.12.0_Linux_x86_64.tar.gz -C / && rm -f /lazydocker_0.12.0_Linux_x86_64.tar.gz && chmod +x /lazydocker; \
    echo "0d9dbfc26068b218e7ed84b104748cadc6e3cf733c0afd35465306fb39b9523c  /lazydocker_0.12.0_Linux_x86_64.tar.gz" | sha256sum -c  #







RUN strip /lazydocker 2>/dev/null \
    mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true && \
    [ -f /lazydocker ] || { echo '#!/bin/sh' > /lazydocker ; echo 'echo "lazydocker-ui v${VERSION} binary not available - download failed" >&2"' >> /lazydocker ; echo 'exit 1' >> /lazydocker ; chmod +x /lazydocker 2>/dev/null ; } 2>/dev/null && \
    [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "lazydocker-ui v${VERSION} binary not available - download failed" >&2"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exit 1' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null ; } 2>/dev/null && \
    [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "lazydocker-ui v${VERSION} binary not available - download failed" >&2"' >> /app ; echo 'exit 1' >> /app ; chmod +x /app 2>/dev/null ; } 2>/dev/null







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/lazydocker-ui /var/cache/lazydocker-ui 2>/dev/null || true























FROM scratch















COPY --from=downloader /lazydocker /usr/local/bin/lazydocker







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







LABEL evergreen.image.tier="3"















EXPOSE 9101







STOPSIGNAL SIGTERM















HEALTHCHECK NONE















LABEL org.opencontainers.image.description="lazydocker-ui container image" \
      org.opencontainers.image.title="Lazydocker UI" \
      org.opencontainers.image.source="https://github.com/jesseduffield/lazydocker" \
            org.opencontainers.image.version="0.25.2"















ENTRYPOINT ["/lazydocker"]







CMD ["--help"]
