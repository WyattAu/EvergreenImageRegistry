ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Readarr/Readarr/releases/download/v0.4.5/Readarr.develop.0.4.5.linux-core-x64.tar.gz -o /Readarr.tar.gz && \
    mkdir -p / 2>/dev/null || true ; touch --chown=65532:65532 2>/dev/null || true \
    [ -f /Readarr.tar.gz ] && tar -xzf /Readarr.tar.gz -C /app && rm /Readarr.tar.gz && chmod +x /app/Readarr 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Readarr/Readarr/releases/download/v0.4.5/Readarr.develop.0.4.5.linux-core-x64.tar.gz -o /app/Readarr && chmod +x /app/Readarr || true


RUN apk add --no-cache ca-certificates curl 
RUN adduser -u 65532 -D app 2>/dev/null || true
COPY --from=downloader --chown=65532:65532 /app /app
RUN mkdir -p /var/log/readarr /var/cache/readarr && chown -R 65532:65532 /var/log/readarr /var/cache/readarr 2>/dev/null || true
USER 65532:65532
WORKDIR /app
EXPOSE 8787
ENTRYPOINT ["/app/Readarr"]
LABEL org.opencontainers.image.title="readarr" \
      org.opencontainers.image.version="0.4.5" \
      org.opencontainers.image.vendor="Readarr" \
      org.opencontainers.image.source="https://github.com/Readarr/Readarr/releases" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
