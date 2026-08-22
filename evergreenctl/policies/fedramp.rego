# =============================================================================
# FedRAMP — Container Image Compliance Policies
# =============================================================================
# Rego policies for FedRAMP compliance in federal cloud environments.
# Maps to NIST SP 800-53 Rev 5 controls.
#
# FedRAMP Baselines:
#   Low: 125 controls
#   Moderate: 325 controls
#   High: 421 controls
#
# Key Control Families:
#   AC: Access Control
#   AU: Audit and Accountability
#   CM: Configuration Management
#   IA: Identification and Authentication
#   RA: Risk Assessment
#   SC: System and Communications Protection
#   SI: System and Information Integrity
# =============================================================================

package evergreen.fedramp

import rego.v1

# ---------------------------------------------------------------------------
# AC: Access Control
# ---------------------------------------------------------------------------

# FEDRAMP-AC-2: Least privilege
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "USER root")
    msg := "FedRAMP AC-2: Container must not run as root"
}

# FEDRAMP-AC-6: Least privilege enforcement
deny[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "USER 65532")
    msg := "FedRAMP AC-6: Container must specify non-root USER"
}

# FEDRAMP-AC-6(5): Privileged access restrictions
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "CAPABILITY")
    not contains(input.dockerfile, "DROP ALL")
    msg := "FedRAMP AC-6(5): Capabilities must be explicitly dropped"
}

# FEDRAMP-AC-17: Remote access
deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*(EXPOSE|CMD|ENTRYPOINT).*0\\.0\\.0\\.0", input.dockerfile)
    msg := "FedRAMP AC-17: Service should not bind to all interfaces"
}

# ---------------------------------------------------------------------------
# AU: Audit and Accountability
# ---------------------------------------------------------------------------

# FEDRAMP-AU-2: Audit events
warn[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "HEALTHCHECK")
    msg := "FedRAMP AU-2: HEALTHCHECK recommended for audit trail"
}

# FEDRAMP-AU-3: Content of audit records
warn[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "STOPSIGNAL")
    msg := "FedRAMP AU-3: STOPSIGNAL recommended for graceful audit shutdown"
}

# FEDRAMP-AU-6: Audit review and analysis
deny[msg] if {
    not input.sbom
    msg := "FedRAMP AU-6: SBOM required for audit trail of package inventory"
}

# ---------------------------------------------------------------------------
# CM: Configuration Management
# ---------------------------------------------------------------------------

# FEDRAMP-CM-2: Baseline configuration
deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+.*alpine", input.dockerfile)
    msg := "FedRAMP CM-2: Alpine not in approved baseline. Use wolfi-base or distroless."
}

deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+.*debian.*slim", input.dockerfile)
    msg := "FedRAMP CM-2: debian-slim not in approved baseline. Use wolfi-base."
}

# FEDRAMP-CM-3: Configuration change control
deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+.*:latest", input.dockerfile)
    msg := "FedRAMP CM-3: :latest tag not allowed — pin to specific version"
}

# FEDRAMP-CM-6: Configuration settings
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(debug|verbose|trace|insecure)", input.dockerfile)
    msg := "FedRAMP CM-6: Debug/verbose settings detected in Dockerfile"
}

# FEDRAMP-CM-7: Least functionality
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "apt-get install")
    not contains(input.dockerfile, "--no-install-recommends")
    msg := "FedRAMP CM-7: Use --no-install-recommends for least functionality"
}

# FEDRAMP-CM-8: System component inventory
deny[msg] if {
    not input.sbom
    msg := "FedRAMP CM-8: SBOM required for component inventory"
}

# ---------------------------------------------------------------------------
# IA: Identification and Authentication
# ---------------------------------------------------------------------------

# FEDRAMP-IA-2: User identification
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(password|secret|token|api.key)", input.dockerfile)
    not regex.match("(?i)(build-arg|--secret|\\$\\{)", input.dockerfile)
    msg := "FedRAMP IA-2: Hardcoded credentials detected"
}

# FEDRAMP-IA-5: Authenticator management
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(MYSQL_ROOT_PASSWORD|POSTGRES_PASSWORD)", input.dockerfile)
    msg := "FedRAMP IA-5: Database passwords must use build secrets"
}

# ---------------------------------------------------------------------------
# RA: Risk Assessment
# ---------------------------------------------------------------------------

# FEDRAMP-RA-5: Vulnerability monitoring
deny[msg] if {
    input.manifest.tier == "critical"
    not input.sbom
    msg := "FedRAMP RA-5: Tier 1 images must have SBOM for vulnerability monitoring"
}

# FEDRAMP-RA-5(2): Automated vulnerability scanning
deny[msg] if {
    input.manifest.tier == "critical"
    cve := input.vulnerabilities[_]
    cve.severity == "CRITICAL"
    cve.fixed_version == ""
    msg := sprintf("FedRAMP RA-5: Unpatched critical CVE %s", [cve.id])
}

# ---------------------------------------------------------------------------
# SC: System and Communications Protection
# ---------------------------------------------------------------------------

# FEDRAMP-SC-8: Confidentiality of transmission
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(http://|telnet://|ftp://)", input.dockerfile)
    msg := "FedRAMP SC-8: Insecure protocol — use HTTPS/TLS"
}

# FEDRAMP-SC-12: Cryptographic key management
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(md5|sha1|des|rc4|3des)", input.dockerfile)
    msg := "FedRAMP SC-12: Weak cryptographic algorithm detected"
}

# FEDRAMP-SC-13: Cryptographic protection
warn[msg] if {
    input.labels["compliance.fedramp"] == "true"
    not input.labels["compliance.fips"] == "true"
    msg := "FedRAMP SC-13: FIPS 140-2 validation recommended"
}

# FEDRAMP-SC-17: PKI certificates
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "ssl_verify")
    regex.match("(?i)ssl_verify\\s*=\\s*(off|false|0)", input.dockerfile)
    msg := "FedRAMP SC-17: SSL verification must not be disabled"
}

# ---------------------------------------------------------------------------
# SI: System and Information Integrity
# ---------------------------------------------------------------------------

# FEDRAMP-SI-2: Flaw remediation
deny[msg] if {
    input.manifest.tier == "critical"
    cve := input.vulnerabilities[_]
    cve.severity == "CRITICAL"
    msg := sprintf("FedRAMP SI-2: Critical CVE %s requires remediation", [cve.id])
}

# FEDRAMP-SI-3: Malicious code protection
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(curl|wget)\\s+.*\\|\\s*(sh|bash)", input.dockerfile)
    msg := "FedRAMP SI-3: Piping remote content to shell is prohibited"
}

# FEDRAMP-SI-5: Security alerts and advisories
deny[msg] if {
    not input.labels["org.opencontainers.image.source"]
    msg := "FedRAMP SI-5: OCI source label required for security advisory tracking"
}

# FEDRAMP-SI-7: Software integrity
deny[msg] if {
    not input.sbom
    msg := "FedRAMP SI-7: SBOM required for software integrity verification"
}
