# =============================================================================
# PCI DSS v4.0 — Container Image Compliance Policies
# =============================================================================
# Rego policies for PCI DSS compliance in containerized environments.
# Maps PCI DSS requirements to container image security controls.
#
# PCI DSS Categories:
#   Req 1: Install and maintain network security controls
#   Req 2: Apply secure configurations
#   Req 3: Protect stored account data
#   Req 4: Protect cardholder data with strong cryptography
#   Req 6: Develop and maintain secure systems
#   Req 7: Restrict access by business need
#   Req 8: Identify users and authenticate access
#   Req 10: Log and monitor all access
#   Req 11: Test security regularly
#   Req 12: Support information security with policies
# =============================================================================

package evergreen.pci_dss

import rego.v1

# ---------------------------------------------------------------------------
# Requirement 2: Apply Secure Configurations
# ---------------------------------------------------------------------------

# PCI-DSS-2.2.1: System hardening standards
deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+.*alpine", input.dockerfile)
    msg := "PCI DSS 2.2.1: Alpine images do not meet hardening standards. Use wolfi-base or distroless."
}

deny[msg] if {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+.*debian.*slim", input.dockerfile)
    msg := "PCI DSS 2.2.1: debian-slim does not meet hardening standards. Use wolfi-base."
}

# PCI-DSS-2.2.2: Default accounts disabled
deny[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "USER 65532")
    not contains(input.dockerfile, "USER nonroot")
    msg := "PCI DSS 2.2.2: Container must run as non-root (UID 65532)"
}

# ---------------------------------------------------------------------------
# Requirement 4: Protect Cardholder Data with Strong Cryptography
# ---------------------------------------------------------------------------

# PCI-DSS-4.2.1: Strong cryptography for transmission
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "ENTRYPOINT")
    not contains(input.dockerfile, "TLS")
    not contains(input.dockerfile, "ssl")
    not contains(input.dockerfile, "https")
    not input.is_distroless
    msg := "PCI DSS 4.2.1: Container should support TLS for cardholder data transmission"
}

# ---------------------------------------------------------------------------
# Requirement 6: Develop and Maintain Secure Systems
# ---------------------------------------------------------------------------

# PCI-DSS-6.2.1: Security patches applied
deny[msg] if {
    input.manifest.tier == "critical"
    not input.sbom
    msg := "PCI DSS 6.2.1: Tier 1 images must have SBOM for vulnerability tracking"
}

# PCI-DSS-6.3.1: Vulnerability identification
deny[msg] if {
    input.manifest.tier == "critical"
    cve := input.vulnerabilities[_]
    cve.severity == "CRITICAL"
    cve.fixed_version == ""
    msg := sprintf("PCI DSS 6.3.1: Unpatched critical CVE %s in Tier 1 image", [cve.id])
}

# PCI-DSS-6.5.6: Insecure cryptography
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(md5|sha1|des|rc4|3des)", input.dockerfile)
    msg := "PCI DSS 6.5.6: Insecure cryptographic algorithm detected in Dockerfile"
}

# ---------------------------------------------------------------------------
# Requirement 7: Restrict Access by Business Need
# ---------------------------------------------------------------------------

# PCI-DSS-7.2.1: Least privilege
deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "USER root")
    msg := "PCI DSS 7.2.1: Container must not run as root"
}

# ---------------------------------------------------------------------------
# Requirement 8: Identify Users and Authenticate Access
# ---------------------------------------------------------------------------

# PCI-DSS-8.3.1: Strong authentication
deny[msg] if {
    input.dockerfile
    regex.match("(?i)(password|secret|token|api.key)", input.dockerfile)
    not regex.match("(?i)(build-arg|--secret|\\$\\{)", input.dockerfile)
    msg := "PCI DSS 8.3.1: Potential hardcoded credentials in Dockerfile. Use build secrets."
}

# ---------------------------------------------------------------------------
# Requirement 10: Log and Monitor All Access
# ---------------------------------------------------------------------------

# PCI-DSS-10.2.1: Audit logging
warn[msg] if {
    input.dockerfile
    not contains(input.dockerfile, "HEALTHCHECK")
    msg := "PCI DSS 10.2.1: HEALTHCHECK recommended for audit trail"
}

# ---------------------------------------------------------------------------
# Requirement 11: Test Security Regularly
# ---------------------------------------------------------------------------

# PCI-DSS-11.3.1: Vulnerability scanning
deny[msg] if {
    not input.sbom
    msg := "PCI DSS 11.3.1: SBOM required for vulnerability scanning"
}

# ---------------------------------------------------------------------------
# Requirement 12: Support Information Security
# ---------------------------------------------------------------------------

# PCI-DSS-12.3.1: Security policies documented
deny[msg] if {
    not input.labels["org.opencontainers.image.description"]
    msg := "PCI DSS 12.3.1: OCI labels required for security documentation"
}
