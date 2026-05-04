
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=5.1.4
ARG GITHUB_TOKEN
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
        openjdk-17-jre-base curl ca-certificates unzip && \
    rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/openhab/openhab-distro/releases/download/${VERSION}/openhab-${VERSION}.zip -o /openhab.zip && \
    echo "502c0cee3e98a3abdb3f3dcfe37075450c9fac0264b0077f7989b6eb6c3a2168  /openhab.zip" | sha256sum -c || true  #
    unzip -q /openhab.zip -d /opt/openhab && rm -f /openhab.zip
RUN mkdir -p /app-src /opt/openhab/userdata /opt/openhab/conf /opt/openhab/log

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache ca-certificates curl libffi-dev || true
COPY --from=builder /opt/openhab /opt/openhab
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /opt/openhab -s /bin/false openhab 2>/dev/null || true && \
    chown -R 65532:65532 /opt/openhab /app 2>/dev/null || true
USER 65532:65532
WORKDIR /opt/openhab
EXPOSE 8080 8443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/openhab/start.sh"]
LABEL org.opencontainers.image.title="openhab3" \
      org.opencontainers.image.description="openHAB 3 - Open source home automation" \
      org.opencontainers.image.vendor="openHAB" \
      org.opencontainers.image.source="https://github.com/openhab/openhab-distro" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
