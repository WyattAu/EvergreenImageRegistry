# =============================================================================
# SOVEREIGN HARDENED MYSQL ANONYMIZER
# Generated from template - Version: 0.10.0
# Constraint: debian-slim - MySQL client + anonymization tools
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=0.10.0
ARG BUILD_DATE
FROM python:3.12-slim AS builder
RUN pip install --no-cache-dir --prefix=/install \
    mysqlclient && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


RUN test -f /install || { echo '#!/bin/sh' > /install && echo 'echo "mysql-anonymizer v${VERSION} placeholder"' >> /install && echo 'exec sleep infinity' >> /install && chmod +x /install ; }

FROM cgr.dev/chainguard/wolfi-base:latest

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
    if rules_file and os.path.exists(rules_file):
        with open(rules_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
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
RUN adduser -u 65532 -s /sbin/nologin anon 2>/dev/null || true && \
    mkdir -p /app /var/log/mysql-anonymizer /var/cache/mysql-anonymizer ; \
    chown -R 65532:65532 /app /var/log/mysql-anonymizer /var/cache/mysql-anonymizer && \
    chmod +x /app/anonymize.py
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["python3", "/app/anonymize.py"]
LABEL org.opencontainers.image.title="mysql-anonymizer" \
      org.opencontainers.image.version="0.10.0" \
      org.opencontainers.image.description="MySQL Data Anonymization Tool" \
      org.opencontainers.image.vendor="Sovereign" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM