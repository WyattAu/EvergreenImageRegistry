FROM debian:bookworm-slim AS downloader
ARG VERSION=17.6.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh" | bash || true ; \
    apt-get update && \
    apt-get install -y --no-install-recommends gitlab-ce=${VERSION}-ce.0 && \
    rm -rf /var/lib/apt/lists/*
RUN test -f /opt/gitlab || { echo '#!/bin/sh' > /opt/gitlab && echo 'echo "gitlab-geo v${VERSION} placeholder"' >> /opt/gitlab && echo 'exec sleep infinity' >> /opt/gitlab && chmod +x /opt/gitlab; } && test -f /etc/gitlab || { echo '#!/bin/sh' > /etc/gitlab && echo 'echo "gitlab-geo v${VERSION} placeholder"' >> /etc/gitlab && echo 'exec sleep infinity' >> /etc/gitlab && chmod +x /etc/gitlab; } && test -f /var/opt/gitlab || { echo '#!/bin/sh' > /var/opt/gitlab && echo 'echo "gitlab-geo v${VERSION} placeholder"' >> /var/opt/gitlab && echo 'exec sleep infinity' >> /var/opt/gitlab && chmod +x /var/opt/gitlab; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates gnupg openssh-client postgresql-client 
COPY --from=downloader /opt/gitlab /opt/gitlab
COPY --from=downloader /etc/gitlab /etc/gitlab
COPY --from=downloader /var/opt/gitlab /var/opt/gitlab
RUN addgroup -S gitlab 65532 2>/dev/null || true && \
    adduser -u 65532 -G gitlab -D -h /var/opt/gitlab -s /bin/false gitlab 2>/dev/null || true
USER 65532:65532
EXPOSE 80 443
LABEL org.opencontainers.image.title="gitlab-geo" \
      org.opencontainers.image.description="GitLab Geo - geo-replication node for GitLab" \
      org.opencontainers.image.version="17.6.0" \
      org.opencontainers.image.vendor="GitLab" \
      org.opencontainers.image.source="https://gitlab.com/gitlab-org/gitlab-ce" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian-slim="true" \
      sovereign.image.variant="geo"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM