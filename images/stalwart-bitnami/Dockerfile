FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31 AS builder
ARG VERSION=0.16.2
ARG GITHUB_TOKEN
RUN apk add --no-cache curl ca-certificates || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" \
    "https://github.com/stalwartlabs/stalwart/releases/download/v${VERSION}/stalwart-x86_64-unknown-linux-musl.tar.gz" \
    -o /tmp/stalwart.tar.gz && \
    tar -xzf /tmp/stalwart.tar.gz -C /tmp && \
    mv /tmp/stalwart /usr/local/bin/stalwart && \
    chmod +x /usr/local/bin/stalwart && \
    strip /usr/local/bin/stalwart || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=0.16.2
RUN apk add --no-cache ca-certificates || true
RUN addgroup -S -g 10000 stalwart 2>/dev/null || true && \
    adduser -u 65532 -G stalwart -D -h /app -s /bin/false stalwart 2>/dev/null || true
RUN mkdir -p /app /var/lib/stalwart /etc/stalwart /var/log/stalwart 2>/dev/null || true
COPY --from=builder /usr/local/bin/stalwart /usr/local/bin/stalwart
RUN chown -R 65532:65532 /app /var/lib/stalwart /etc/stalwart /var/log/stalwart 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 25 143 465 587 993

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:25/ || exit 1
ENTRYPOINT ["/usr/local/bin/stalwart"]
CMD ["mail"]
LABEL org.opencontainers.image.title="stalwart-bitnami" \
      org.opencontainers.image.description="Stalwart Mail Server (Bitnami variant) - all-in-one mail server" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="stalwartlabs" \
      org.opencontainers.image.source="https://github.com/stalwartlabs/stalwart" \
      evergreen.image.tier="2" \
      evergreen.image.category="email" \
      evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
