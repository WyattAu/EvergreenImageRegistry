FROM cgr.dev/chainguard/wolfi-base:latest AS builder
ARG VERSION=0.8.0
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/stalwartlabs/stalwart/releases/download/v${VERSION}/stalwart-linux-x86_64-musl.tar.gz" \
    -o /tmp/stalwart.tar.gz && \
    tar -xzf /tmp/stalwart.tar.gz -C /tmp && \
    mv /tmp/stalwart /usr/local/bin/stalwart && \
    chmod +x /usr/local/bin/stalwart && \
    strip /usr/local/bin/stalwart || true

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=0.8.0
RUN apk add --no-cache ca-certificates || true
RUN addgroup -S -g 10000 stalwart 2>/dev/null || true && \
    adduser -u 65532 -G stalwart -D -h /app -s /bin/false stalwart 2>/dev/null || true
RUN mkdir -p /app /var/lib/stalwart /etc/stalwart /var/log/stalwart 2>/dev/null || true
COPY --from=builder /usr/local/bin/stalwart /usr/local/bin/stalwart
RUN chown -R 65532:65532 /app /var/lib/stalwart /etc/stalwart /var/log/stalwart 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 25 143 465 587 993
ENTRYPOINT ["/usr/local/bin/stalwart"]
CMD ["mail"]
LABEL org.opencontainers.image.title="stalwart-bitnami" \
      org.opencontainers.image.description="Stalwart Mail Server (Bitnami variant) - all-in-one mail server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="stalwartlabs" \
      org.opencontainers.image.source="https://github.com/stalwartlabs/stalwart" \
      sovereign.image.tier="2" \
      sovereign.image.category="email" \
      sovereign.constraint.nonroot="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="tcp"
EXPOSE 9101
STOPSIGNAL SIGTERM
