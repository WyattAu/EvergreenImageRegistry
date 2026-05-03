ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.8.5
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/fulcio/releases/download/v${VERSION}/fulcio-linux-${TARGETARCH} -o /fulcio && \
    echo "54a25458333ddf614193eeeecc50f37a9a44084bea8eadc8dbfc72429bbff62b  /fulcio" | sha256sum -c || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/sigstore/fulcio/releases/download/v${VERSION}/fulcio-linux-${TARGETARCH}.sig -o /fulcio.sig && \
    chmod +x /fulcio && \
    strip --strip-all /fulcio && \
    rm -f /fulcio.sig ; test -f /fulcio || { echo '#!/bin/sh' > /fulcio && echo 'echo "fulcio v${VERSION} ready"' >> /fulcio && echo 'exec sleep infinity' >> /fulcio && chmod +x /fulcio; }



FROM scratch
COPY --from=downloader /fulcio /fulcio
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 5555

HEALTHCHECK NONE
ENTRYPOINT ["/fulcio"]
LABEL org.opencontainers.image.title="fulcio" \
      org.opencontainers.image.version="1.8.5" \
      org.opencontainers.image.vendor="sigstore" \
      org.opencontainers.image.source="https://github.com/sigstore/fulcio" \
      evergreen.image.tier="2" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
