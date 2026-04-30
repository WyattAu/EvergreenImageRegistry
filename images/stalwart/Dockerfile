FROM debian:bookworm-slim AS downloader
ARG VERSION=0.8.0
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/stalwartlabs/stalwart/releases/download/v${VERSION}/stalwart-linux-x86_64-musl.tar.gz" \
    -o /tmp/stalwart.tar.gz && \
    tar -xzf /tmp/stalwart.tar.gz -C /tmp && \
    mv /tmp/stalwart /usr/local/bin/stalwart && \
    chmod +x /usr/local/bin/stalwart && \
    strip /usr/local/bin/stalwart || true

FROM scratch
COPY --from=downloader /usr/local/bin/stalwart /usr/local/bin/stalwart
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 25 143 465 587 993
ENTRYPOINT ["/usr/local/bin/stalwart"]
CMD ["mail"]
LABEL org.opencontainers.image.title="stalwart" \
      org.opencontainers.image.description="Stalwart Mail Server - all-in-one mail server written in Rust" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="stalwartlabs" \
      org.opencontainers.image.source="https://github.com/stalwartlabs/stalwart" \
      sovereign.image.tier="2" \
      sovereign.image.category="email" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"
LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
