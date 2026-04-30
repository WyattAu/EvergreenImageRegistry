FROM debian:bookworm-slim AS downloader
ARG VERSION=1.0.1
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/mailhog/MailHog/releases/download/v${VERSION}/MailHog_linux_amd64" \
    -o /tmp/MailHog && \
    echo "e2ed634ded49929f089b20045581955ed217672078fd86082dd7a6c67c5d09c7  /tmp/MailHog" | sha256sum -c - && \
    chmod +x /tmp/MailHog && \
    strip /tmp/MailHog || true

FROM scratch
COPY --from=downloader /tmp/MailHog /usr/local/bin/MailHog
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENV MH_SMTP_BIND_ADDR="0.0.0.0:1025"
ENV MH_API_BIND_ADDR="0.0.0.0:8025"
ENV MH_UI_BIND_ADDR="0.0.0.0:8025"
EXPOSE 8025 1025
ENTRYPOINT ["/usr/local/bin/MailHog"]
LABEL org.opencontainers.image.title="mailhog" \
      org.opencontainers.image.description="MailHog - email testing tool" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="MailHog" \
      org.opencontainers.image.source="https://github.com/mailhog/MailHog" \
      sovereign.image.tier="2" \
      sovereign.image.category="email" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM
