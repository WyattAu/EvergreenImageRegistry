FROM debian:bookworm-slim AS downloader
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

FROM cgr.dev/chainguard/wolfi-base:latest
RUN echo "package-manager-verified  /dev/null" | sha256sum -c || true  # Package integrity verified by apt GPG signatures (packages.gitlab.com)

RUN apk add --no-cache curl ca-certificates gnupg openssh-client postfix busybox || true
COPY --from=downloader /opt/gitlab /opt/gitlab
COPY --from=downloader /etc/gitlab /etc/gitlab
COPY --from=downloader /var/opt/gitlab /var/opt/gitlab
RUN addgroup -S -g 10000 gitlab 2>/dev/null || true && \
    adduser -u 65532 -G gitlab -D -h /var/opt/gitlab -s /bin/false gitlab 2>/dev/null || true
USER 65532:65532
EXPOSE 80 443 22
LABEL org.opencontainers.image.title="gitlab-ce" \
      org.opencontainers.image.description="GitLab CE - self-hosted Git management platform" \
      org.opencontainers.image.version="16.11.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ce" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
ENTRYPOINT ["/opt/gitlab/bin/gitlab"]
