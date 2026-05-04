FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=0.9.3
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/foxcpp/maddy/releases/download/v${VERSION}/maddy-linux-amd64.tar.gz" \
    -o /tmp/maddy.tar.gz && \
    tar -xzf /tmp/maddy.tar.gz -C /tmp && \
    mv /tmp/maddy /usr/local/bin/maddy && \
    chmod +x /usr/local/bin/maddy && \
    strip /usr/local/bin/maddy || true
FROM scratch
COPY --from=downloader /usr/local/bin/maddy /usr/local/bin/maddy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 25 143 465 587 993 995

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/maddy"]
CMD ["run"]
LABEL org.opencontainers.image.title="maddy" \
      org.opencontainers.image.description="Maddy - composable all-in-one mail server written in Go" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="foxcpp" \
      org.opencontainers.image.source="https://github.com/foxcpp/maddy" \
      evergreen.image.tier="2" \
      evergreen.image.category="email" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
