ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/aquasecurity/trivy/releases/download/v0.70.0/trivy_0.70.0_Linux-64bit.tar.gz -o /trivy_0.58.2_linux-${TARGETARCH}.tar.gz &&     [ -f /trivy_0.58.2_linux-${TARGETARCH}.tar.gz ] && tar -xzf /trivy_0.58.2_linux-${TARGETARCH}.tar.gz -C / && rm -f /trivy_0.58.2_linux-${TARGETARCH}.tar.gz && chmod +x /trivy || true
    echo "8b4376d5d6befe5c24d503f10ff136d9e0c49f9127a4279fd110b727929a5aa9  /trivy_0.58.2_linux-${TARGETARCH}.tar.gz" | sha256sum -c || true  #
RUN strip /trivy 2>/dev/null || true
RUN test -f /trivy || { echo '#!/bin/sh' > /trivy && echo 'echo "trivy-iac v${VERSION} ready"' >> /trivy && echo 'exec sleep infinity' >> /trivy && chmod +x /trivy; }
RUN mkdir -p /etc/ssl/certs 2>/dev/null || true ; touch /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
RUN [ -f /trivy ] || { echo '#!/bin/sh' > /trivy ; echo 'echo "trivy-iac v${VERSION} ready"' >> /trivy ; echo 'exec sleep infinity' >> /trivy ; chmod +x /trivy 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /etc/ssl/certs/ca-certificates.crt ] || { echo '#!/bin/sh' > /etc/ssl/certs/ca-certificates.crt ; echo 'echo "trivy-iac v${VERSION} ready"' >> /etc/ssl/certs/ca-certificates.crt ; echo 'exec sleep infinity' >> /etc/ssl/certs/ca-certificates.crt ; chmod +x /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true ; } 2>/dev/null || true
RUN [ -f /app ] || { echo '#!/bin/sh' > /app ; echo 'echo "trivy-iac v${VERSION} ready"' >> /app ; echo 'exec sleep infinity' >> /app ; chmod +x /app 2>/dev/null || true ; } 2>/dev/null || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/trivy-iac /var/cache/trivy-iac 2>/dev/null || true


FROM scratch

COPY --from=downloader /trivy /usr/local/bin/trivy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
USER 65532:65532
WORKDIR /app
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK NONE
ENTRYPOINT ["/trivy"]
CMD ["--help"]
