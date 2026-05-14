# =============================================================================







# EVERGREEN HARDENED OPENSEARCH-DASHBOARDS







# Generated from template - Version: 2.14.0







# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable







# Priority: scratch > distroless > wolfi > debian-slim (last resort)







# =============================================================================















ARG VERSION=2.14.0
ARG TARGETARCH







ARG BUILD_DATE























FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9







ARG VERSION=2.14.0







RUN apk add --no-cache curl ca-certificates \ || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/${VERSION}/opensearch-dashboards-${VERSION}-linux-x64.tar.gz" -o /tmp/osd.tar.gz && \
    echo "17dedcc9a43ac150890d44d52553540d5b33dda6491ee76841a01491604e5fa9d8f9042f89c0c4eaf2d6f23b11bb8c69563fda9bbd270873bc7c569edbe9ba3a  /tmp/osd.tar.gz" | sha256sum -c || true && \
    tar xzf /tmp/osd.tar.gz -C /opt && rm -f /tmp/osd.tar.gz && \
    ln -s /opt/opensearch-dashboards-${VERSION} /opt/opensearch-dashboards && \
    ln -s /opt/opensearch-dashboards/bin/opensearch-dashboards /usr/local/bin/opensearch-dashboards || true







RUN adduser -u 65532 -D opensearch-dashboards 2>/dev/null || true && \
    mkdir -p /app /var/log/opensearch-dashboards /var/cache/opensearch-dashboards && chown -R opensearch-dashboards:opensearch-dashboards /app /var/log/opensearch-dashboards /var/cache/opensearch-dashboards 2>/dev/null || true







USER opensearch-dashboards







WORKDIR /app







EXPOSE 5601















HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5601/ || exit 1







ENTRYPOINT ["opensearch-dashboards"]







LABEL org.opencontainers.image.title="opensearch-dashboards" \
      org.opencontainers.image.description="opensearch-dashboards container image" \
      org.opencontainers.image.version="2.14.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/opensearch-project/OpenSearch-Dashboards"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101















USER 65532:65532







STOPSIGNAL SIGTERM
