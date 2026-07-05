# =============================================================================
# EVERGREEN HARDENED INFRA-WEBHOOK
# Multi-tool deployment webhook (ansible, docker, sops, age)
# wolfi-base (needs bash, python3, git, docker-cli)
# =============================================================================
ARG SHIM_VERSION=v1.3.0
ARG SOPS_VERSION=3.12.2
ARG AGE_VERSION=1.2.0
ARG WEBHOOK_VERSION=2.8.3
ARG ANSIBLE_VERSION=2.20.4
ARG COMPOSE_VERSION=v2.32.3

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base
ARG SOPS_VERSION=3.12.2
ARG AGE_VERSION=1.2.0
ARG WEBHOOK_VERSION=2.8.3
ARG ANSIBLE_VERSION=2.20.4
ARG COMPOSE_VERSION=v5.1.4
ARG TARGETARCH
COPY --from=shim /shim /usr/local/bin/shim

RUN apk add --no-cache \
    bash \
    python3 \
    py3-pip \
    git \
    curl \
    openssh-client \
    su-exec \
    gettext \
    util-linux \
    docker-cli \
    ca-certificates \
    wget

RUN pip3 install --break-system-packages ansible-core==${ANSIBLE_VERSION} && \
    ansible-galaxy collection install community.docker && \
    pip3 install --break-system-packages requests

ARG TARGETARCH
RUN ARCH="${TARGETARCH:-amd64}" && \
    mkdir -p /usr/local/lib/docker/cli-plugins && \
    wget -qO /usr/local/lib/docker/cli-plugins/docker-compose \
        "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-${ARCH}" && \
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

RUN ARCH="${TARGETARCH:-amd64}" && \
    wget -qO /usr/local/bin/sops \
        "https://github.com/getsops/sops/releases/download/v${SOPS_VERSION}/sops-v${SOPS_VERSION}.linux.${ARCH}" && \
    chmod +x /usr/local/bin/sops && \
    wget -qO /tmp/age.tar.gz \
        "https://github.com/FiloSottile/age/releases/download/v${AGE_VERSION}/age-v${AGE_VERSION}-linux-${ARCH}.tar.gz" && \
    tar xzf /tmp/age.tar.gz -C /usr/local/bin age && \
    rm /tmp/age.tar.gz && \
    wget -qO /tmp/webhook.tar.gz \
        "https://github.com/adnanh/webhook/releases/download/${WEBHOOK_VERSION}/webhook-linux-${ARCH}.tar.gz" && \
    tar xzf /tmp/webhook.tar.gz -C /usr/local/bin --strip-components=1 && \
    rm -f /tmp/webhook.tar.gz

RUN mkdir -p /opt/webhook /home/webhook/.ssh && \
    git config --global user.email "infra-deploy@wyattau.com" && \
    git config --global user.name "Infra Deploy"
ENV HOME=/home/webhook
WORKDIR /opt/webhook

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
EXPOSE 9000 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--http", "127.0.0.1:9000/hooks/deploy"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/webhook"]
CMD ["-hooks", "/opt/webhook/hooks.yaml", "-verbose", "-http-methods", "POST"]

LABEL org.opencontainers.image.title="infra-webhook" \
      org.opencontainers.image.description="Infrastructure deployment webhook (ansible, docker, sops, age)" \
      org.opencontainers.image.vendor="wyattau"
LABEL evergreen.base.image="wolfi" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
STOPSIGNAL SIGTERM
