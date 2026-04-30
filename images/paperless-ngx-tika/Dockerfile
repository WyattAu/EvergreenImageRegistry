ARG VERSION=2.14.4
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates curl ; rm -rf /var/lib/apt/lists/* || true

RUN python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir paperless-ngx || true

USER 65532:65532
EXPOSE 9101
STOPSIGNAL SIGTERM

ENTRYPOINT ["python", "-m", "paperless-ngx"]
CMD ["--help"]
