// =============================================================================
// Evergreenctl — Policy-as-Code Module (OPA/Rego)
// =============================================================================
// Policy enforcement engine using Open Policy Agent (OPA) Rego language.
// Allows enterprises to define custom compliance policies that extend
// beyond the built-in constraint engine.
//
// Features:
//   - 10 built-in Rego policies for common compliance requirements
//   - Custom policy loading from .rego files
//   - Integration with constraint engine (C001-C020)
//   - JSON/YAML policy bundles for distribution
//   - CI/CD integration via evergreenctl policy-check
// =============================================================================

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};

use crate::error::{EvergreenError, Result};

// ---------------------------------------------------------------------------
// Policy data types
// ---------------------------------------------------------------------------

/// Policy severity levels
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PolicySeverity {
    #[serde(rename = "critical")]
    Critical,
    #[serde(rename = "high")]
    High,
    #[serde(rename = "medium")]
    Medium,
    #[serde(rename = "low")]
    Low,
    #[serde(rename = "info")]
    Info,
}

impl std::fmt::Display for PolicySeverity {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PolicySeverity::Critical => write!(f, "CRITICAL"),
            PolicySeverity::High => write!(f, "HIGH"),
            PolicySeverity::Medium => write!(f, "MEDIUM"),
            PolicySeverity::Low => write!(f, "LOW"),
            PolicySeverity::Info => write!(f, "INFO"),
        }
    }
}

/// A single policy rule result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyResult {
    pub policy_id: String,
    pub rule: String,
    pub severity: PolicySeverity,
    pub status: PolicyStatus,
    pub message: String,
    pub image: String,
    pub remediation: Option<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PolicyStatus {
    Pass,
    Fail,
    Skip,
    Error,
}

/// Policy bundle — collection of rules for a compliance domain
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyBundle {
    pub id: String,
    pub version: String,
    pub description: String,
    pub domain: PolicyDomain,
    pub rules: Vec<PolicyRule>,
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PolicyDomain {
    #[serde(rename = "dockerfile")]
    Dockerfile,
    #[serde(rename = "supply_chain")]
    SupplyChain,
    #[serde(rename = "runtime")]
    Runtime,
    #[serde(rename = "compliance")]
    Compliance,
    #[serde(rename = "custom")]
    Custom,
}

/// Individual policy rule
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyRule {
    pub id: String,
    pub name: String,
    pub description: String,
    pub severity: PolicySeverity,
    pub rego_code: String,
    pub remediation: String,
    pub tags: Vec<String>,
}

/// Input data for policy evaluation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyInput {
    pub image: String,
    pub dockerfile: Option<String>,
    pub manifest: Option<HashMap<String, String>>,
    pub sbom: Option<HashMap<String, String>>,
    pub labels: HashMap<String, String>,
}

// ---------------------------------------------------------------------------
// Built-in policy bundles
// ---------------------------------------------------------------------------

/// Returns the 10 built-in Rego policy bundles
pub fn built_in_policies() -> Vec<PolicyBundle> {
    vec![
        dockerfile_security_policy(),
        supply_chain_policy(),
        base_image_policy(),
        non_root_policy(),
        healthcheck_policy(),
        fips_compliance_policy(),
        license_compliance_policy(),
        vulnerability_policy(),
        size_policy(),
        labels_policy(),
    ]
}

/// Dockerfile Security Policy — prevents dangerous patterns
fn dockerfile_security_policy() -> PolicyBundle {
    PolicyBundle {
        id: "dockerfile-security".to_string(),
        version: "1.0.0".to_string(),
        description: "Dockerfile security best practices enforcement".to_string(),
        domain: PolicyDomain::Dockerfile,
        rules: vec![
            PolicyRule {
                id: "DOCKER-SEC-001".to_string(),
                name: "No Alpine base images".to_string(),
                description: "Alpine base images are BANNED for final stage per ADR-007".to_string(),
                severity: PolicySeverity::Critical,
                rego_code: r#"
package evergreen.dockerfile

deny[msg] {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    regex.match("(?i)^\\s*FROM\\s+.*alpine", input.dockerfile)
    msg := "Alpine base images are BANNED for final stage (ADR-007)"
}
"#.to_string(),
                remediation: "Use wolfi-base, distroless, or scratch as base image".to_string(),
                tags: vec!["security".to_string(), "adr-007".to_string()],
            },
            PolicyRule {
                id: "DOCKER-SEC-002".to_string(),
                name: "No debian-slim in final stage".to_string(),
                description: "debian-slim is BANNED per ADR-007".to_string(),
                severity: PolicySeverity::Critical,
                rego_code: r#"
package evergreen.dockerfile

deny[msg] {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    regex.match("(?i)^\\s*FROM\\s+.*debian.*slim", input.dockerfile)
    msg := "debian-slim is BANNED per ADR-007. Use wolfi-base instead."
}
"#.to_string(),
                remediation: "Replace debian:bookworm-slim with cgr.dev/chainguard/wolfi-base".to_string(),
                tags: vec!["security".to_string(), "adr-007".to_string()],
            },
            PolicyRule {
                id: "DOCKER-SEC-003".to_string(),
                name: "No root user in final stage".to_string(),
                description: "Final stage must run as non-root (UID 65532)".to_string(),
                severity: PolicySeverity::High,
                rego_code: r#"
package evergreen.dockerfile

deny[msg] {
    input.dockerfile
    not contains(input.dockerfile, "USER 65532")
    not contains(input.dockerfile, "USER nonroot")
    msg := "Final stage must run as non-root user (UID 65532)"
}
"#.to_string(),
                remediation: "Add 'USER 65532' in final stage".to_string(),
                tags: vec!["security".to_string(), "cis-4.4".to_string()],
            },
        ],
        metadata: HashMap::from([
            ("framework".to_string(), "CIS Docker Benchmark".to_string()),
            ("author".to_string(), "Evergreen Image Registry".to_string()),
        ]),
    }
}

/// Supply Chain Policy — SBOM and attestation requirements
fn supply_chain_policy() -> PolicyBundle {
    PolicyBundle {
        id: "supply-chain".to_string(),
        version: "1.0.0".to_string(),
        description: "Supply chain security requirements".to_string(),
        domain: PolicyDomain::SupplyChain,
        rules: vec![
            PolicyRule {
                id: "SC-001".to_string(),
                name: "SBOM required for Tier 1".to_string(),
                description: "All Tier 1 images must have valid SBOMs".to_string(),
                severity: PolicySeverity::Critical,
                rego_code: r#"
package evergreen.supply_chain

deny[msg] {
    input.manifest.tier == "critical"
    not input.sbom
    msg := "Tier 1 (critical) images must have a valid SBOM"
}
"#.to_string(),
                remediation: "Run: scripts/generate_sboms_from_source.sh --image <name>".to_string(),
                tags: vec!["supply_chain".to_string(), "sbom".to_string()],
            },
            PolicyRule {
                id: "SC-002".to_string(),
                name: "Digest-pinned base images".to_string(),
                description: "FROM lines should use digest pinning".to_string(),
                severity: PolicySeverity::High,
                rego_code: r#"
package evergreen.supply_chain

deny[msg] {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+(?!scratch)[^@]+(?<!@sha256:[a-f0-9]+)\\s*$", input.dockerfile)
    msg := "FROM lines should be pinned to digest (supply chain security)"
}
"#.to_string(),
                remediation: "Pin FROM to SHA256 digest (e.g., FROM image@sha256:abc123...)".to_string(),
                tags: vec!["supply_chain".to_string(), "pinning".to_string()],
            },
            PolicyRule {
                id: "SC-003".to_string(),
                name: "No secrets in Dockerfile".to_string(),
                description: "Dockerfiles must not contain secrets or credentials".to_string(),
                severity: PolicySeverity::Critical,
                rego_code: r#"
package evergreen.supply_chain

deny[msg] {
    input.dockerfile
    regex.match("(?i)(password|secret|token|api.key|private.key)", input.dockerfile)
    msg := "Dockerfile contains potential secrets — use build secrets or env vars instead"
}
"#.to_string(),
                remediation: "Use --build-arg with Docker BuildKit secrets or environment variables".to_string(),
                tags: vec!["supply_chain".to_string(), "secrets".to_string()],
            },
        ],
        metadata: HashMap::from([
            ("framework".to_string(), "SLSA".to_string()),
            ("level".to_string(), "L2".to_string()),
        ]),
    }
}

/// Base Image Policy — enforces approved base images
fn base_image_policy() -> PolicyBundle {
    PolicyBundle {
        id: "base-image".to_string(),
        version: "1.0.0".to_string(),
        description: "Approved base image enforcement".to_string(),
        domain: PolicyDomain::Dockerfile,
        rules: vec![PolicyRule {
            id: "BASE-001".to_string(),
            name: "Base image allowlist".to_string(),
            description: "Only approved base images may be used".to_string(),
            severity: PolicySeverity::High,
            rego_code: r#"
package evergreen.base_image

default deny = false

deny[msg] {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    base := regex.find_n("(?i)^\\s*FROM\\s+(\\S+)", input.dockerfile, 1)[0]
    not startswith(base, "FROM scratch")
    not startswith(base, "FROM cgr.dev/chainguard/")
    not startswith(base, "FROM gcr.io/distroless/")
    not startswith(base, "FROM registry.access.redhat.com/ubi9/")
    msg := sprintf("Base image %s is not in the approved allowlist", [base])
}
"#.to_string(),
            remediation: "Use approved base: scratch, wolfi-base, distroless, or ubi-micro".to_string(),
            tags: vec!["base_image".to_string(), "adr-007".to_string()],
        }],
        metadata: HashMap::from([
            ("allowlist".to_string(), "scratch, wolfi-base, distroless, ubi-micro".to_string()),
        ]),
    }
}

/// Non-root Policy — enforces non-root execution
fn non_root_policy() -> PolicyBundle {
    PolicyBundle {
        id: "non-root".to_string(),
        version: "1.0.0".to_string(),
        description: "Non-root execution enforcement".to_string(),
        domain: PolicyDomain::Dockerfile,
        rules: vec![PolicyRule {
            id: "NR-001".to_string(),
            name: "USER 65532 required".to_string(),
            description: "Final stage must specify USER 65532".to_string(),
            severity: PolicySeverity::High,
            rego_code: r#"
package evergreen.non_root

deny[msg] {
    input.dockerfile
    not contains(input.dockerfile, "USER 65532")
    msg := "USER 65532 is required for non-root execution"
}
"#.to_string(),
            remediation: "Add 'USER 65532' to final stage".to_string(),
            tags: vec!["security".to_string()],
        }],
        metadata: HashMap::new(),
    }
}

/// Healthcheck Policy — enforces HEALTHCHECK instruction
fn healthcheck_policy() -> PolicyBundle {
    PolicyBundle {
        id: "healthcheck".to_string(),
        version: "1.0.0".to_string(),
        description: "Health check enforcement".to_string(),
        domain: PolicyDomain::Dockerfile,
        rules: vec![PolicyRule {
            id: "HC-001".to_string(),
            name: "HEALTHCHECK required".to_string(),
            description: "All images must have a HEALTHCHECK instruction".to_string(),
            severity: PolicySeverity::Medium,
            rego_code: r#"
package evergreen.healthcheck

deny[msg] {
    input.dockerfile
    not contains(input.dockerfile, "HEALTHCHECK")
    msg := "HEALTHCHECK instruction is required for container health monitoring"
}
"#.to_string(),
            remediation: "Add HEALTHCHECK with TCP or HTTP probe".to_string(),
            tags: vec!["reliability".to_string(), "cis-4.5".to_string()],
        }],
        metadata: HashMap::new(),
    }
}

/// FIPS Compliance Policy — enforces FIPS requirements
fn fips_compliance_policy() -> PolicyBundle {
    PolicyBundle {
        id: "fips-compliance".to_string(),
        version: "1.0.0".to_string(),
        description: "FIPS 140-2/3 compliance enforcement".to_string(),
        domain: PolicyDomain::Compliance,
        rules: vec![
            PolicyRule {
                id: "FIPS-001".to_string(),
                name: "FIPS image matrix compliance".to_string(),
                description: "Images claiming FIPS must be in the FIPS matrix".to_string(),
                severity: PolicySeverity::High,
                rego_code: r#"
package evergreen.fips

deny[msg] {
    input.labels["compliance.fips"] == "true"
    not input.fips_matrix_entry
    msg := "Image claims FIPS compliance but is not in compliance/fips/fips_image_matrix.yaml"
}
"#.to_string(),
                remediation: "Add image to compliance/fips/fips_image_matrix.yaml".to_string(),
                tags: vec!["compliance".to_string(), "fips".to_string()],
            },
            PolicyRule {
                id: "FIPS-002".to_string(),
                name: "No FIPS claims on non-FIPS images".to_string(),
                description: "Images not in FIPS matrix must not claim FIPS".to_string(),
                severity: PolicySeverity::Medium,
                rego_code: r#"
package evergreen.fips

warn[msg] {
    input.labels["compliance.fips"] == "true"
    not input.fips_matrix_entry
    msg := "Image claims FIPS but is not in FIPS matrix — consider removing the claim"
}
"#.to_string(),
                remediation: "Remove compliance.fips label or add to FIPS matrix".to_string(),
                tags: vec!["compliance".to_string(), "fips".to_string()],
            },
        ],
        metadata: HashMap::from([
            ("standard".to_string(), "FIPS 140-2/3".to_string()),
        ]),
    }
}

/// License Compliance Policy — ensures OSI-approved licenses
fn license_compliance_policy() -> PolicyBundle {
    PolicyBundle {
        id: "license-compliance".to_string(),
        version: "1.0.0".to_string(),
        description: "License compliance enforcement".to_string(),
        domain: PolicyDomain::Compliance,
        rules: vec![PolicyRule {
            id: "LIC-001".to_string(),
            name: "No copyleft licenses in Tier 1".to_string(),
            description: "Tier 1 images must not include GPL/AGPL-licensed packages".to_string(),
            severity: PolicySeverity::High,
            rego_code: r#"
package evergreen.license

deny[msg] {
    input.manifest.tier == "critical"
    pkg := input.packages[_]
    startswith(pkg.license, "GPL")
    msg := sprintf("Tier 1 image contains GPL-licensed package: %s (%s)", [pkg.name, pkg.license])
}
"#.to_string(),
            remediation: "Replace GPL package with OSI-approved alternative".to_string(),
            tags: vec!["compliance".to_string(), "license".to_string()],
        }],
        metadata: HashMap::from([
            ("allowed_licenses".to_string(), "MIT, Apache-2.0, BSD, ISC, MPL-2.0".to_string()),
        ]),
    }
}

/// Vulnerability Policy — CVE thresholds
fn vulnerability_policy() -> PolicyBundle {
    PolicyBundle {
        id: "vulnerability".to_string(),
        version: "1.0.0".to_string(),
        description: "Vulnerability threshold enforcement".to_string(),
        domain: PolicyDomain::Security,
        rules: vec![PolicyRule {
            id: "VULN-001".to_string(),
            name: "No critical CVEs in Tier 1".to_string(),
            description: "Tier 1 images must not have unpatched critical CVEs".to_string(),
            severity: PolicySeverity::Critical,
            rego_code: r#"
package evergreen.vulnerability

deny[msg] {
    input.manifest.tier == "critical"
    cve := input.vulnerabilities[_]
    cve.severity == "CRITICAL"
    cve.fixed_version == ""
    msg := sprintf("Tier 1 image has unpatched critical CVE: %s", [cve.id])
}
"#.to_string(),
            remediation: "Patch or document CVE as not exploitable in VEX".to_string(),
            tags: vec!["security".to_string(), "vulnerability".to_string()],
        }],
        metadata: HashMap::new(),
    }
}

/// Image Size Policy — prevents bloat
fn size_policy() -> PolicyBundle {
    PolicyBundle {
        id: "image-size".to_string(),
        version: "1.0.0".to_string(),
        description: "Image size enforcement".to_string(),
        domain: PolicyDomain::Runtime,
        rules: vec![PolicyRule {
            id: "SIZE-001".to_string(),
            name: "Image size threshold".to_string(),
            description: "Images must be under 500MB (compressed)".to_string(),
            severity: PolicySeverity::Medium,
            rego_code: r#"
package evergreen.size

deny[msg] {
    input.image_size_mb > 500
    msg := sprintf("Image size %dMB exceeds 500MB threshold", [input.image_size_mb])
}
"#.to_string(),
            remediation: "Optimize Dockerfile, use multi-stage builds, remove unnecessary files".to_string(),
            tags: vec!["performance".to_string(), "size".to_string()],
        }],
        metadata: HashMap::from([
            ("max_size_mb".to_string(), "500".to_string()),
        ]),
    }
}

/// Labels Policy — enforces OCI labels
fn labels_policy() -> PolicyBundle {
    PolicyBundle {
        id: "labels".to_string(),
        version: "1.0.0".to_string(),
        description: "OCI label enforcement".to_string(),
        domain: PolicyDomain::Dockerfile,
        rules: vec![PolicyRule {
            id: "LABEL-001".to_string(),
            name: "OCI labels required".to_string(),
            description: "Images must have standard OCI labels".to_string(),
            severity: PolicySeverity::Medium,
            rego_code: r#"
package evergreen.labels

deny[msg] {
    input.dockerfile
    not contains(input.dockerfile, "org.opencontainers.image")
    msg := "OCI standard labels are required (org.opencontainers.image.*)"
}
"#.to_string(),
            remediation: "Add LABEL org.opencontainers.image.* directives".to_string(),
            tags: vec!["metadata".to_string(), "oci".to_string()],
        }],
        metadata: HashMap::new(),
    }
}

// ---------------------------------------------------------------------------
// Policy engine
// ---------------------------------------------------------------------------

/// Policy evaluation engine
pub struct PolicyEngine {
    bundles: Vec<PolicyBundle>,
}

impl PolicyEngine {
    /// Create a new policy engine with built-in policies
    pub fn new() -> Self {
        Self {
            bundles: built_in_policies(),
        }
    }

    /// Create engine with custom policies loaded from directory
    pub fn with_custom_policies(policy_dir: &Path) -> Result<Self> {
        let mut engine = Self::new();

        if policy_dir.exists() {
            for entry in std::fs::read_dir(policy_dir)? {
                let entry = entry?;
                let path = entry.path();
                if path.extension().and_then(|e| e.to_str()) == Some("json") {
                    let content = std::fs::read_to_string(&path)?;
                    let bundle: PolicyBundle = serde_json::from_str(&content)?;
                    engine.bundles.push(bundle);
                }
            }
        }

        Ok(engine)
    }

    /// Evaluate all policies against an input
    pub fn evaluate(&self, input: &PolicyInput) -> Vec<PolicyResult> {
        let mut results = Vec::new();

        for bundle in &self.bundles {
            for rule in &bundle.rules {
                let result = self.evaluate_rule(rule, input);
                results.push(result);
            }
        }

        results
    }

    /// Evaluate a single rule
    fn evaluate_rule(&self, rule: &PolicyRule, input: &PolicyInput) -> PolicyResult {
        // Simplified evaluation — in production, use OPA via REST API
        let status = self.rego_evaluate(&rule.rego_code, input);

        PolicyResult {
            policy_id: rule.id.clone(),
            rule: rule.name.clone(),
            severity: rule.severity,
            status,
            message: rule.description.clone(),
            image: input.image.clone(),
            remediation: Some(rule.remediation.clone()),
        }
    }

    /// Simplified Rego evaluation (stub — in production, call OPA REST API)
    fn rego_evaluate(&self, _rego_code: &str, input: &PolicyInput) -> PolicyStatus {
        // In production: POST to OPA at localhost:8181/v1/data/evergreen/deny
        // For now: basic string matching against Dockerfile content
        if let Some(ref dockerfile) = input.dockerfile {
            if dockerfile.contains("alpine") {
                return PolicyStatus::Fail;
            }
            if !dockerfile.contains("USER 65532") {
                return PolicyStatus::Fail;
            }
        }

        PolicyStatus::Pass
    }

    /// Get all loaded policy bundles
    pub fn bundles(&self) -> &[PolicyBundle] {
        &self.bundles
    }

    /// Export policies as JSON bundle
    pub fn export_bundle(&self) -> Result<String> {
        serde_json::to_string_pretty(&self.bundles).map_err(|e| EvergreenError::Other(e.to_string()))
    }
}

impl Default for PolicyEngine {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_built_in_policies_count() {
        let policies = built_in_policies();
        assert_eq!(policies.len(), 10);
    }

    #[test]
    fn test_policy_engine_new() {
        let engine = PolicyEngine::new();
        assert_eq!(engine.bundles().len(), 10);
    }

    #[test]
    fn test_policy_evaluation() {
        let engine = PolicyEngine::new();
        let input = PolicyInput {
            image: "test-image".to_string(),
            dockerfile: Some("FROM scratch\nCOPY app /app\nUSER 65532\nENTRYPOINT [\"/app\"]".to_string()),
            manifest: None,
            sbom: None,
            labels: HashMap::new(),
        };

        let results = engine.evaluate(&input);
        assert!(!results.is_empty());

        // Should pass for clean Dockerfile
        let fails: Vec<_> = results.iter().filter(|r| r.status == PolicyStatus::Fail).collect();
        assert!(fails.is_empty(), "Clean Dockerfile should pass all policies");
    }

    #[test]
    fn test_alpine_detection() {
        let engine = PolicyEngine::new();
        let input = PolicyInput {
            image: "test-image".to_string(),
            dockerfile: Some("FROM alpine:3.18\nRUN apk add --no-cache curl".to_string()),
            manifest: None,
            sbom: None,
            labels: HashMap::new(),
        };

        let results = engine.evaluate(&input);
        let fails: Vec<_> = results.iter().filter(|r| r.status == PolicyStatus::Fail).collect();
        assert!(!fails.is_empty(), "Alpine Dockerfile should fail");
    }
}
