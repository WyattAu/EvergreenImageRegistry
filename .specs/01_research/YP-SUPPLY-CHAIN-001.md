# Yellow Paper: Supply Chain Security Theory

## Document Header

```yaml
---
document_id: YP-SUPPLY-CHAIN-001
version: 1.0.0
status: DRAFT
domain: Supply Chain Security
subdomains: [Signing, Attestation, SBOM, Provenance]
applicable_standards: [SLSA, FIPS 140-2, Cosign]
created: 2026-04-19
author: Nexus (Principal Systems Architect)
confidence_level: 0.90
tqa_level: 4
---
```

## Executive Summary

This Yellow Paper establishes the theoretical foundation for supply chain security in container images. The problem is
ensuring image integrity and provenance from build to deployment.

**Scope:**

- IN: Image signing, SBOM generation, attestation
- OUT: Key management infrastructure
- ASSUMPTIONS: HSM hardware available

---

## Nomenclature

| Symbol     | Description                | Units       | Domain    | Source      |
| ---------- | -------------------------- | ----------- | --------- | ----------- |
| $S_{sig}$  | Digital signature          | Binary      | Crypto    | Cosign      |
| $B_{sbom}$ | Software Bill of Materials | JSON        | SPDX      | Syft        |
| $A_{att}$  | Attestation                | Binary      | Predicate | Cosign      |
| $P_{prov}$ | Provenance                 | JSON        | In-toto   | Build       |
| $K_{pub}$  | Public key                 | Binary      | Crypto    | HSM         |
| $T_{log}$  | Transparency log           | Append-only | Rekor     | Certificate |

---

## Theoretical Foundation

### AX-001: Cryptographic Integrity

> Every image must be signed with a private key held in HSM, providing cryptographic proof of origin.

**Justification:** Software-only signing keys can be compromised. HSM provideshardware-level protection.

**Verification:** Key ceremony documentation, HSM audit logs.

### AX-002: Transparency

> All signatures must be recorded in a transparency log to enable detection of compromised keys.

**Justification:** Transparency logs enable detection of unauthorized signings.

**Verification:** Rekor log verification.

### AX-003: SBOM Completeness

> Every image must have a complete SBOM listing all components and dependencies.

**Justification:** Complete inventory enables rapid vulnerability response.

**Verification:** SBOM completeness testing.

### DEF-001: SLSA Level 3 Compliant Build

> A build that provides provenance with build integrity and provenance attestation.

$$\text{SLSA-3} \implies (\text{ prover_attestation } \land \text{ build_config } \land \text{ ETR })$$

---

## Algorithm Specification

### ALG-001: Image Signing

```
Algorithm: SignImage
Input: image_ref, keyref
Output: signature, rekor_entry

1: function SignImage(image_ref, keyref)
2:   digest := compute_sha256(image_ref)
3:   payload := create_oidc_payload(digest)
4:   signature := sign_hsm(payload, keyref)
5:   attest := create_attestation(image_ref, signature)
6:   rekor_entry := upload_transparency_log(attest)
7:   return signature, rekor_entry
8: end function
```

**Complexity:**

| Metric | Value | Derivation         |
| ------ | ----- | ------------------ |
| Time   | O(n)  | n = layer count    |
| Space  | O(s)  | s = signature size |

### ALG-002: SBOM Generation

```
Algorithm: GenerateSBOM
Input: image_ref
Output: sbom_json

1: function GenerateSBOM(image_ref)
2:   layers := extract_layers(image_ref)
3:   packages := []
4:   for layer in layers do
5:     pkgs := extract_packages(layer)
6:     append packages, pkgs
7:   end for
8:   sbom := format_sbom(packages, SPDX)
9:   return sbom
10: end function
```

### ALG-003: Provenance Attestation

```
Algorithm: CreateProvenance
Input: build_Records
Output: attestation

1: function CreateProvenance(build_records)
2:   materials := extract_materials(build_records)
3:   builder := extract_builder(build_records)
4:   commands := extract_commands(build_records)
5:   predicate := in_toto_format(materials, builder, commands)
6:   attestation := sign_predicate(predicate)
7:   return attestation
8: end function
```

---

## Domain Constraints

### SC-001: Key Requirements

| Constraint   | Value             | Rationale         |
| ------------ | ----------------- | ----------------- |
| Key type     | P-256 or RSA-4096 | FIPS approved     |
| Key storage  | HSM               | Hardware security |
| Key ceremony | 2-of-3            | Dual control      |

### SC-002: SLSA Levels

| Level | Requirement     | Implementation    |
| ----- | --------------- | ----------------- |
| 1     | Provenance      | Build attestation |
| 2     | Build integrity | Signed provenance |
| 3     | Build integrity | Hosted build      |

---

## Test Vector Specification

See `.specs/01_research/test_vectors/test_vectors_supply_chain.toml`

---

## Bibliography

| ID   | Citation             | Relevance             | TQA |
| ---- | -------------------- | --------------------- | --- |
| [^1] | SLSA Specification   | Supply chain security | 5   |
| [^2] | FIPS 140-2           | Cryptographic modules | 5   |
| [^3] | Cosign Documentation | Implementation        | 5   |
| [^4] | Rekor Documentation  | Transparency log      | 4   |

---

## Document Control

| Version | Date       | Status | Author |
| ------- | ---------- | ------ | ------ |
| 1.0.0   | 2026-04-19 | DRAFT  | Nexus  |

**END OF YELLOW PAPER**
