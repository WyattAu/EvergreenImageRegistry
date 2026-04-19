# CHANGELOG - Sovereign Hardened Image Registry

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-04-19

### Added
- **Requirements:** Complete newrequirements.md with rigorous actionable structure
- **Images:** 1000+ images in requiredimages.md
- **Yellow Papers:**
  - YP-SEC-HARDENING-001 (Container Security Hardening)
  - YP-VULN-SCAN-001 (Vulnerability Scanning)
  - YP-SUPPLY-CHAIN-001 (Supply Chain Security)
  - YP-OBSERVABILITY-001 (Observability)
- **Blue Papers:**
  - BP-IMAGE-REGISTRY-001 (IEEE 1016 compliant)
- **R&D Structure:**
  - Yellow Paper Registry (.specs/01_research/yellow_paper_registry.toml)
  - Blue Paper Registry (.specs/02_architecture/blue_paper_registry.toml)
  - Test Vector definitions (test_vectors_hardening.toml)
  - Domain Constraints (domain_constraints_security.toml)
- **Compliance:**
  - TRACEABILITY_MATRIX.md
  - STANDARD_CONFLICTS.md
  - Tool Requirements (tool_requirements.toml)
- **Reports:**
  - Phase 0 Report
  - Phase 1 Report
  - Phase 2 Report

### Changed
- **Requirements:** Completely restructured newrequirements.md from v1 (295 lines) to v2 (247 reqs, structured 10 parts)
- **domain_analysis.md:** Updated with complete multi-lingual requirements

### Fixed
- Directory structure verified per R&D v5.0 specification
- All papers documented with proper metadata

---

## [1.0.0] - 2026-04-19 (Initial)

### Added
- Initial newrequirements.md structure
- Initial requiredimages.md (1010 images)
- YP-SEC-HARDENING-001.md
- YP-VULN-SCAN-001.md
- BP-IMAGE-REGISTRY-001.md
- domain_analysis.md
- requirements.md
- Basic test_vectors

---

## [Unreleased]

### Known Issues
- None currently identified

---

## Version History

| Version | Phase | Status |
|---------|-------|--------|
| 2.0.0 | Phase 2 | IN PROGRESS |

---

**END OF CHANGELOG**