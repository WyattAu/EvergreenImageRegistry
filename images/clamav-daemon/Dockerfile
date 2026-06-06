







ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder







RUN mkdir -p /var/log/clamav || true
RUN mkdir -p /var/lib/clamav && \
    mkdir -p /var/log/clamav || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        clamav clamav-daemon freshclam ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    mkdir -p /app /var/log/clamav /var/lib/clamav /run/clamav







FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9















RUN apk add --no-cache clamav clamav-daemon freshclam ca-certificates && \
    mkdir -p /run /var/lib /var/log 2>/dev/null || true







COPY --from=builder /app /app







COPY --from=builder /var/log/clamav /var/log/clamav







COPY --from=builder /var/lib/clamav /var/lib/clamav







COPY --from=builder /run/clamav /run/clamav







RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    mkdir -p /app 2>/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false clamav || true && \
    chown -R 65532:65532 /app /var/log/clamav /var/lib/clamav /run/clamav







USER 65532:65532







WORKDIR /app















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1







ENTRYPOINT ["clamd"]







CMD ["--foreground", "--debug"]







LABEL org.opencontainers.image.title="clamav-daemon" \
      org.opencontainers.image.description="ClamAV - daemon mode" \
      org.opencontainers.image.vendor="Cisco" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/Cisco-Talos/clamav" \
                  org.opencontainers.image.version="unknown"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101







STOPSIGNAL SIGTERM
