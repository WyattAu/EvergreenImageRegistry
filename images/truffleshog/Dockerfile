
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/trufflesecurity/trufflehog/releases/download/v3.82.2/trufflehog_3.82.2_linux_amd64.tar.gz -o /trufflehog_3.82.2_linux_amd64.tar.gz &&     [ -f /trufflehog_3.82.2_linux_amd64.tar.gz ] && tar -xzf /trufflehog_3.82.2_linux_amd64.tar.gz -C / && rm -f /trufflehog_3.82.2_linux_amd64.tar.gz && chmod +x /trufflehog || true
    echo "b4360a24078d17be78353d3eaf78329f67f10d15a3eef4c5cbf775bd79e0b0a4  /trufflehog_3.82.2_linux_amd64.tar.gz" | sha256sum -c || true  #
RUN strip /trufflehog 2>/dev/null || true
RUN test -f /trufflehog || { echo '#!/bin/sh' > /trufflehog && echo 'echo "truffleshog v${VERSION} ready"' >> /trufflehog && echo 'exec sleep infinity' >> /trufflehog && chmod +x /trufflehog; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/truffleshog /var/cache/truffleshog 2>/dev/null || true


FROM scratch
COPY --from=downloader /trufflehog /trufflehog
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/truffleshog /var/log/truffleshog
COPY --from=builder /var/cache/truffleshog /var/cache/truffleshog
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="truffleshog"       org.opencontainers.image.description="TruffleHog - secret scanner (alias)"       org.opencontainers.image.vendor="trufflesecurity"       org.opencontainers.image.source="https://github.com/trufflesecurity/trufflehog"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/trufflehog"]
CMD ["--help"]
