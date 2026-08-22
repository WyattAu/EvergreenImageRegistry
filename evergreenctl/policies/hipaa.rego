# =============================================================================
# HIPAA — Container Image Compliance Policies
# =============================================================================
# Rego policies for HIPAA compliance in containerized healthcare environments.
# Focuses on PHI protection, access controls, and audit requirements.
#
# HIPAA Rules:
#   §164.312(a): Access control
#   §164.312(b): Audit controls
#   §164.312(c): Integrity
#   §164.312(d): Authentication
#   §164.312(e): Transmission security
# =============================================================================

package evergreen.hipaa

import rego.v1

# ---------------------------------------------------------------------------
# §164.312(a): Access Control
# ---------------------------------------------------------------------------

# HIPAA-AC-01: Minimum necessary access
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "USER root")
    msg := "HIPAA §164.312(a): Container must not run as root — minimum necessary access"
}

deny[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "USER 65532")
    msg := "HIPAA §164.312(a): Container must specify non-root USER (UID 65532)"
}

# HIPAA-AC-02: No unnecessary packages
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "apt-get install")
    not contains(input.dockerfile, "--no-install-recommends")
    msg := "HIPAA §164.312(a): Use --no-install-recommends to minimize attack surface"
}

# HIPAA-AC-03: No interactive shells
deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*(CMD|ENTRYPOINT)\\s+.*(/bin/sh|/bin/bash|bash|sh)", input.dockerfile)
    msg := "HIPAA §164.312(a): Interactive shells increase attack surface"
}

# ---------------------------------------------------------------------------
# §164.312(b): Audit Controls
# ---------------------------------------------------------------------------

# HIPAA-AUDIT-01: Health monitoring
warn[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "HEALTHCHECK")
    msg := "HIPAA §164.312(b): HEALTHCHECK required for availability monitoring"
}

# HIPAA-AUDIT-02: Logging capability
warn[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "STOPSIGNAL")
    msg := "HIPAA §164.312(b): STOPSIGNAL recommended for graceful shutdown logging"
}

# ---------------------------------------------------------------------------
# §164.312(c): Integrity
# ---------------------------------------------------------------------------

# HIPAA-INT-01: Image integrity
deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+(?!scratch|cgr\\.dev|gcr\\.io/distroless|registry\\.access\\.redhat\\.com)", input.dockerfile)
    msg := "HIPAA §164.312(c): Only approved base images allowed (integrity control)"
}

# HIPAA-INT-02: SBOM for integrity verification
deny[msg] if {
    input.manifest.tier == "critical"
    not input.sbom
    msg := "HIPAA §164.312(c): SBOM required for package integrity verification"
}

# ---------------------------------------------------------------------------
# §164.312(d): Authentication
# ---------------------------------------------------------------------------

# HIPAA-AUTH-01: No hardcoded credentials
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(password|secret|token|api.key|private.key)", input.dockerfile)
    not regex.match("(?i)(build-arg|--secret|\\$\\{)", input.dockerfile)
    msg := "HIPAA §164.312(d): Hardcoded credentials detected — use build secrets"
}

# HIPAA-AUTH-02: No default passwords
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(MYSQL_ROOT_PASSWORD|POSTGRES_PASSWORD|MONGO_INITDB_ROOT_PASSWORD)", input.dockerfile)
    not regex.match("(?i)(build-arg|--secret|\\$\\{)", input.dockerfile)
    msg := "HIPAA §164.312(d): Database passwords must not be hardcoded"
}

# ---------------------------------------------------------------------------
# §164.312(e): Transmission Security
# ---------------------------------------------------------------------------

# HIPAA-TLS-01: TLS required for data in transit
deny[msg] if {
    input.manifest.tier == "critical"
    not input.dockerfile
    msg := "HIPAA §164.312(e): Tier 1 images must have Dockerfile for TLS configuration"
}

# HIPAA-TLS-02: No insecure protocols
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(http://|telnet://|ftp://)", input.dockerfile)
    not regex.match("(?i)(https://|ftps://)", input.dockerfile)
    msg := "HIPAA §164.312(e): Insecure protocol detected — use HTTPS/TLS"
}

# ---------------------------------------------------------------------------
# Additional HIPAA Requirements
# ---------------------------------------------------------------------------

# HIPAA-FIPS: FIPS 140-2 for PHI encryption
warn[msg] if {
    input.labels["compliance.hipaa"] == "true"
    not input.labels["compliance.fips"] == "true"
    msg := "HIPAA: FIPS 140-2 compliance recommended for PHI encryption"
}

# HIPAA-AUTO-UPDATE: Auto-patching for PHI systems
deny[msg] if {
    input.labels["compliance.hipaa"] == "true"
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+.*:latest", input.dockerfile)
    msg := "HIPAA: :latest tag not allowed for PHI systems — use pinned versions"
}
