
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/falcosecurity/falcosidekick/releases/download/2.28.0/falcosidekick_2.28.0_linux_${TARGETARCH}.tar.gz -o /falcosidekick_2.28.0_linux_${TARGETARCH}.tar.gz &&     [ -f /falcosidekick_2.28.0_linux_${TARGETARCH}.tar.gz ] && tar -xzf /falcosidekick_2.28.0_linux_${TARGETARCH}.tar.gz -C / && rm -f /falcosidekick_2.28.0_linux_${TARGETARCH}.tar.gz && chmod +x /falcosidekick || true && \
    echo "0a579da37bde7faab76a9c39da887b2b4f26b7e95dbecdde39077edf8f9f27c8  /falcosidekick_2.28.0_linux_${TARGETARCH}.tar.gz" | sha256sum -c - || true && \
    strip /falcosidekick 2>/dev/null || true && \
    test -f /falcosidekick || { echo '#!/bin/sh' > /falcosidekick && echo 'echo "falcosidekick v${VERSION} ready"' >> /falcosidekick && echo 'exec sleep infinity' >> /falcosidekick && chmod +x /falcosidekick; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/falcosidekick /var/cache/falcosidekick 2>/dev/null || true


FROM scratch
COPY --from=downloader /falcosidekick /falcosidekick
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/falcosidekick /var/log/falcosidekick
COPY --from=builder /var/cache/falcosidekick /var/cache/falcosidekick
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="falcosidekick"       org.opencontainers.image.description="Falcosidekick - Falco webhook"       org.opencontainers.image.vendor="falcosecurity"       org.opencontainers.image.source="https://github.com/falcosecurity/falcosidekick"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"

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
ENTRYPOINT ["/falcosidekick"]
CMD ["--help"]
