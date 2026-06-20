







ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/jesseduffield/lazydocker/releases/download/v0.25.2/lazydocker_0.25.2_Linux_${TARGETARCH}.tar.gz -o /lazydocker_0.12.0_Linux_x86_64.tar.gz &&     [ -f /lazydocker_0.12.0_Linux_x86_64.tar.gz ] && tar -xzf /lazydocker_0.12.0_Linux_x86_64.tar.gz -C / && rm -f /lazydocker_0.12.0_Linux_x86_64.tar.gz && chmod +x /lazydocker; \
    echo "0d9dbfc26068b218e7ed84b104748cadc6e3cf733c0afd35465306fb39b9523c  /lazydocker_0.12.0_Linux_x86_64.tar.gz" | sha256sum -c  #







RUN strip /lazydocker 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/lazydocker /var/cache/lazydocker 2>/dev/null || true























ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim







COPY --from=downloader /lazydocker /lazydocker







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







COPY --from=builder /app /app







COPY --from=builder /var/log/lazydocker /var/log/lazydocker







COPY --from=builder /var/cache/lazydocker /var/cache/lazydocker







USER 65532:65532







WORKDIR /app







LABEL org.opencontainers.image.title="lazydocker"       org.opencontainers.image.description="Lazydocker - Terminal UI for Docker"       org.opencontainers.image.vendor="jesseduffield"       org.opencontainers.image.source="https://github.com/jesseduffield/lazydocker"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="0.25.2"















LABEL evergreen.base.image="scratch"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM















HEALTHCHECK NONE







ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/lazydocker"]







CMD ["--help"]
