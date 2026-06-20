







ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader







ARG TARGETARCH







RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/trufflesecurity/trufflehog/releases/download/v3.82.2/trufflehog_3.82.2_linux_${TARGETARCH}.tar.gz -o /trufflehog_3.82.2_linux_${TARGETARCH}.tar.gz &&     [ -f /trufflehog_3.82.2_linux_${TARGETARCH}.tar.gz ] && tar -xzf /trufflehog_3.82.2_linux_${TARGETARCH}.tar.gz -C / && rm -f /trufflehog_3.82.2_linux_${TARGETARCH}.tar.gz && chmod +x /trufflehog; \
    echo "b4360a24078d17be78353d3eaf78329f67f10d15a3eef4c5cbf775bd79e0b0a4  /trufflehog_3.82.2_linux_${TARGETARCH}.tar.gz" | sha256sum -c  #







RUN strip /trufflehog 2>/dev/null && { echo "Binary not available - download failed" >&2; exit 1; }







FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /app /var/log/truffelsh /var/cache/truffelsh 2>/dev/null || true























ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim







COPY --from=downloader /trufflehog /trufflehog







COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt







COPY --from=builder /app /app







COPY --from=builder /var/log/truffelsh /var/log/truffelsh







COPY --from=builder /var/cache/truffelsh /var/cache/truffelsh







USER 65532:65532







WORKDIR /app







LABEL org.opencontainers.image.title="truffelsh"       org.opencontainers.image.description="TruffleHog - secret scanner (alias)"       org.opencontainers.image.vendor="trufflesecurity"       org.opencontainers.image.source="https://github.com/trufflesecurity/trufflehog"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true" \
      org.opencontainers.image.version="3.82.2"















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







ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/trufflehog"]







CMD ["--help"]
