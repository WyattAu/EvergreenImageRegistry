# =============================================================================
# SOVEREIGN HARDENED ZITADEL
# Generated from template - Version: 2.50.0
# Constraint: wolfi - Chaenguard minimal base with package manager
# Priority: scratch > distroless > wolfi (best) > debian-slim
# =============================================================================

ARG VERSION=2.50.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest AS downloader
RUN apk add --no-cache curl ca-certificates
RUN curl -fsSL "https://github.com/zitadel/zitadel/releases/download/v${VERSION}/zitadel_${VERSION}_linux_amd64.tar.gz" -o /zitadel.tar.gz && \
    tar -xzf /zitadel.tar.gz -C / && rm /zitadel.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest
RUN addgroup -g 65534 zitadel || true
RUN adduser -D -u 65534 -G zitadel zitadel || true
RUN mkdir -p /app /var/log/zitadel /var/cache/zitadel
COPY --from=downloader /zitadel /app/zitadel
USER zitadel
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /app/zitadel zitadel --version || exit 1
ENTRYPOINT ["/app/zitadel"]
LABEL org.opencontainers.image.title="zitadel" \
      org.opencontainers.image.version="2.50.0" \
      org.opencontainers.image.vendor="Zitadel" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"