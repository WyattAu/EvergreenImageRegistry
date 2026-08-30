ARG VERSION=v3.7.0
ARG SHIM_VERSION=v2.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* &&     arch=$(case ${TARGETARCH} in amd64) echo "amd64";; arm64) echo "arm64";; *) echo "amd64";; esac) &&     curl -fsSL "https://github.com/etcd-io/etcd/releases/download/${VERSION}/etcd-${VERSION}-linux-${arch}.tar.gz" -o /tmp/etcd.tar.gz &&     tar -xzf /tmp/etcd.tar.gz -C /tmp &&     cp /tmp/etcd-${VERSION}-linux-${arch}/etcd /etcd &&     cp /tmp/etcd-${VERSION}-linux-${arch}/etcdctl /etcdctl &&     chmod +x /etcd /etcdctl

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /etcd /usr/local/bin/etcd
COPY --from=downloader /etcdctl /usr/local/bin/etcdctl
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 2379 2380 9101
VOLUME /etcd-data

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=5   CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:2379"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/etcd"]
CMD []

LABEL org.opencontainers.image.title="etcd" evergreen.image.tier="standard" evergreen.constraint.nonroot="true"
LABEL evergreen.base.image="scratch" evergreen.security.cap-drop="ALL"
STOPSIGNAL SIGTERM
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="false"
LABEL evergreen.security.seccomp="runtime-default"
