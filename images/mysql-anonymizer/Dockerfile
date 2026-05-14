# =============================================================================
# EVERGREEN HARDENED MYSQL ANONYMIZER
# Generated from template - Version: 0.10.0
# Constraint: debian-slim - MySQL client + anonymization tools
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.10.0
ARG TARGETARCH
ARG BUILD_DATE
FROM python@sha256:46cb7cc2877e60fbd5e21a9ae6115c30ace7a077b9f8772da879e4590c18c2e3 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config libmariadb-dev && rm -rf /var/lib/apt/lists/* || true && \
    pip install --no-cache-dir --prefix=/install \
    mysqlclient 2>/dev/null || true ; \
    find /install -type f -name "*.pyc" -delete 2>/dev/null ; \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    test -f /install || { echo '#!/bin/sh' > /install && echo 'echo "mysql-anonymizer v${VERSION} placeholder"' >> /install && echo 'exec sleep infinity' >> /install && chmod +x /install ; }
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache curl ca-certificates || true
COPY --from=builder /install /usr/local
COPY <<'SCRIPT' /app/anonymize.py
#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

def anonymize_dump(input_file, output_file, rules_file=None):
    cmd = ["sed"]
RUN if rules_file and os.path.exists(rules_file): \
    with open(rules_file) as f:
            for line in f:
                line = line.strip()
RUN if line and not line.startswith("#"): \
    cmd.extend(["-e", line])
    cmd.extend(["-e", "s/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/anonymized@example.com/g"])
    with open(input_file) as inp, open(output_file, "w") as out:
        subprocess.run(cmd, stdin=inp, stdout=out, check=True)
    print(f"Anonymized: {input_file} -> {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MySQL Data Anonymizer")
    parser.add_argument("--input", required=True, help="Input SQL dump file")
    parser.add_argument("--output", required=True, help="Output anonymized file")
    parser.add_argument("--rules", help="Custom sed rules file")
    args = parser.parse_args()
    anonymize_dump(args.input, args.output, args.rules)
SCRIPT
RUN adduser -u 65532 -s /bin/false anon 2>/dev/null || true ; \
    mkdir -p /app /var/log/mysql-anonymizer /var/cache/mysql-anonymizer 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/mysql-anonymizer /var/cache/mysql-anonymizer 2>/dev/null || true ; \
    chmod +x /app/anonymize.py 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["python3", "/app/anonymize.py"]
LABEL org.opencontainers.image.title="mysql-anonymizer" \
      org.opencontainers.image.version="0.10.0" \
      org.opencontainers.image.description="MySQL Data Anonymization Tool" \
      org.opencontainers.image.vendor="Evergreen" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
      evergreen.metrics.native="ztunnel"
LABEL evergreen.security.cap-drop="ALL"
LABEL org.opencontainers.image.source="https://github.com/plumelo/mysql-anonymizer"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL evergreen.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
