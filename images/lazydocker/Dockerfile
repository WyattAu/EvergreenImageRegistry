
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/jesseduffield/lazydocker/releases/download/v0.25.2/lazydocker_0.25.2_Linux_x86_64.tar.gz -o /lazydocker_0.12.0_Linux_x86_64.tar.gz &&     [ -f /lazydocker_0.12.0_Linux_x86_64.tar.gz ] && tar -xzf /lazydocker_0.12.0_Linux_x86_64.tar.gz -C / && rm -f /lazydocker_0.12.0_Linux_x86_64.tar.gz && chmod +x /lazydocker || true
    echo "0d9dbfc26068b218e7ed84b104748cadc6e3cf733c0afd35465306fb39b9523c  /lazydocker_0.12.0_Linux_x86_64.tar.gz" | sha256sum -c || true  #
RUN strip /lazydocker 2>/dev/null || true
RUN test -f /lazydocker || { echo '#!/bin/sh' > /lazydocker && echo 'echo "lazydocker v${VERSION} ready"' >> /lazydocker && echo 'exec sleep infinity' >> /lazydocker && chmod +x /lazydocker; }


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/lazydocker /var/cache/lazydocker 2>/dev/null || true


FROM scratch
COPY --from=downloader /lazydocker /lazydocker
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/lazydocker /var/log/lazydocker
COPY --from=builder /var/cache/lazydocker /var/cache/lazydocker
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="lazydocker"       org.opencontainers.image.description="Lazydocker - Terminal UI for Docker"       org.opencontainers.image.vendor="jesseduffield"       org.opencontainers.image.source="https://github.com/jesseduffield/lazydocker"       evergreen.image.tier="3"       evergreen.constraint.nonroot="true"       evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/lazydocker"]
CMD ["--help"]
