FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 py3-pip python3 git ca-certificates curl jq \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir git+https://github.com/home-assistant/supervisor.git@main
RUN mkdir -p /data /app

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache python3 ca-certificates tzdata dbus curl jq
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /data -s /sbin/nologin supervisor 2>/dev/null || true && \
    mkdir -p /data && chown -R 65532:65532 /data /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH" HOME="/data" SUPERVISOR="1"
WORKDIR /data
EXPOSE 80
ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["-m", "supervisor"]
LABEL org.opencontainers.image.title="homeassistant-supervisor" \
      org.opencontainers.image.description="Home Assistant Supervisor - manages add-ons" \
      org.opencontainers.image.vendor="Home Assistant" \
      org.opencontainers.image.source="https://github.com/home-assistant/supervisor" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM