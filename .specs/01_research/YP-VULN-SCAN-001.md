# Yellow Paper: Vulnerability Scanning Theory

## Document Header

```yaml
---
document_id: YP-VULN-SCAN-001
version: 1.0.0
status: APPROVED
domain: Security Scanning
subdomains: [CVE, Vulnerability, Security]
applicable_standards: [NIST SP 800-53, ISO 27001]
created: 2026-04-19
author: Nexus (Principal Systems Architect)
confidence_level: 0.95
tqa_level: 4
---
```

## Executive Summary

This Yellow Paper establishes the theoretical foundation for container image vulnerability scanning. The problem is detecting known vulnerabilities in container images while minimizing false positives and negatives.

**Scope:**
- IN: Built container images
- OUT: Remediation actions
- ASSUMPTIONS: Linux-based images

---

## Nomenclature

| Symbol | Description | Units | Domain | Source |
|--------|-------------|-------|--------|--------|
| $V_{total}$ | Total vulnerabilities | Integer | Set | Scanner |
| $V_{crit}$ | Critical severity | Integer | Set | CVSS 9.0-10.0 |
| $V_{high}$ | High severity | Integer | Set | CVSS 7.0-8.9 |
| $V_{med}$ | Medium severity | Integer | Set | CVSS 4.0-6.9 |
| $V_{low}$ | Low severity | Integer | Set | CVSS 0.1-3.9 |
| $T_{scan}$ | Scan time | Seconds | Metric | Measurement |
| $F_{fp}$ | False positive rate | Ratio | Metric | Validation |
| $F_{fn}$ | False negative rate | Ratio | Metric | Validation |

---

## Theoretical Foundation

### AX-001: Comprehensive Coverage

> All vulnerability scanners must provide comprehensive coverage of OS packages and language dependencies.

**Justification:** Incomplete coverage leaves attack vectors undetected.

**Verification:** Database completeness testing.

### AX-002: Severity Accuracy

> Vulnerability severity ratings must accurately reflect actual exploitability.

**Justification:** Incorrect severity leads to misallocated resources.

**Verification:** CVSS scoring validation.

### AX-003: Continuous Monitoring

> Images must be rescanned continuously to detect new vulnerabilities.

**Justification:** Vulnerabilities discovered after image build.

**Verification:** Automated rescanning tests.

### DEF-001: Zero-CVE Image

> An image with zero Critical and High severity vulnerabilities.

$$\text{Zero-CVE} \implies (V_{crit} = 0 \land V_{high} = 0)$$

---

## Algorithm Specification

### ALG-001: Multi-Engine Scanning

```
Algorithm: MultiEngineScan
Input: image_ref
Output: vulnerability_report

1: function MultiEngineScan(image_ref)
2:   Pull image to local registry
3:   Run Trivy scan, collect results
4:   Run Grype scan, collect results
5:   Merge results, deduplicate
6:   Score by CVSS severity
7:   Return aggregated report
8: end function
```

**Complexity:**

| Metric | Value | Derivation |
|--------|-------|------------|
| Time | O(n*m) | n=packages, m=scanners |
| Space | O(v) | v=vulnerabilities |

### ALG-002: CVE Threshold Enforcement

```
Algorithm: EnforceThreshold
Input: report, max_critical, max_high
Output: PASS or FAIL

1: function EnforceThreshold(report, max_crit, max_high)
2:   if report.critical > max_crit then
3:     return FAIL
4:   end if
5:   if report.high > max_high then
6:     return FAIL
7:   end if
8:   return PASS
9: end function
```

---

## Domain Constraints

### NC-001: CVE Thresholds

| Severity | Max Allowed | Action |
|----------|------------|--------|
| Critical | 0 | BLOCK BUILD |
| High | 0 | BLOCK BUILD |
| Medium | 10 | WARN |
| Low | Unlimited | INFO |

### NC-002: Scan Time

| Scanner | Max Time | Rationale |
|---------|---------|-----------|
| Trivy | 60 seconds | Package count |
| Grype | 90 seconds | Database size |

---

## Test Vector Specification

See `.specs/01_research/test_vectors/test_vectors_vuln_scan.toml`

| Category | Description | Coverage Target |
|----------|-------------|-----------------|
| Nominal | Clean image scan | 40% |
| Boundary | One CVE at threshold | 20% |
| Adversarial | Known malicious | 15% |
| Regression | Previously fixed | 10% |
| Random | Property-based | 15% |

---

## Bibliography

| ID | Citation | Relevance | TQA |
|----|----------|-----------|-----|
| [^1] | NIST CVE Database | Vulnerability data | 5 |
| [^2] | First.org CVSS | Severity scoring | 5 |
| [^3] | Trivy Documentation | Implementation | 4 |
| [^4] | Grype Documentation | Implementation | 4 |