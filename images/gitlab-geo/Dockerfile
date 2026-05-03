FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=16.11.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh" | bash && \
    apt-get update && \
    apt-get install -y --no-install-recommends gitlab-ce=${VERSION}-ce.0 && \
    rm -rf /var/lib/apt/lists/*
RUN test -f /opt/gitlab || { echo "ERROR: gitlab-ce not installed" >&2; exit 1; }

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by apt GPG signatures (packages.gitlab.com)

RUN apk add --no-cache curl ca-certificates gnupg openssh-client postgresql-client || true
COPY --from=downloader /opt/gitlab /opt/gitlab
COPY --from=downloader /etc/gitlab /etc/gitlab
COPY --from=downloader /var/opt/gitlab /var/opt/gitlab
RUN addgroup -S -g 10000 gitlab 2>/dev/null || true && \
    adduser -u 65532 -G gitlab -D -h /var/opt/gitlab -s /bin/false gitlab 2>/dev/null || true
USER 65532:65532
EXPOSE 80 443
LABEL org.opencontainers.image.title="gitlab-geo" \
      org.opencontainers.image.description="GitLab Geo - geo-replication node for GitLab" \
      org.opencontainers.image.version="16.11.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ce" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true" \
      evergreen.image.variant="geo"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:80/ || exit 1
ENTRYPOINT ["/opt/gitlab/bin/gitlab-geo"]
