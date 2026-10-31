| Trivy CVE scanning    | PARTIAL | `build.yml:438`; uses `--ignore-unfixed=false` (good) but no `.trivyignore` management |
| Grype CVE scanning    | PARTIAL | `build.yml:448`; secondary scan, no unfixed filtering                                  |
| Cosign signing        | PARTIAL | `build.yml:506-530`; key-based OR keyless, but no Fulcio/Rekor documented              |
| SBOM generation       | PARTIAL | `build.yml:532-561`; syft generates SPDX, cosign attests                               |
| SLSA provenance       | PARTIAL | `build.yml:270`; `--attest "type=provenance,mode=max"` on push                         |
| TruffleHog scanning   | WEAK    | `build.yml:184-189`; `continue-on-error: true`, scans full repo only                   |
| SC-001 | No checksum verification on downloads        | CRITICAL; arbitrary code execution   | ~107            |
| SC-002 | TruffleHog `continue-on-error: true`         | HIGH; secrets may pass undetected    | All             |
| SC-003 | No hermetic CI environment                   | MEDIUM; build reproducibility risk   | All             |
| SC-004 | No SLSA provenance verification in consumers | MEDIUM; supply chain trust gap       | All             |
| SC-005 | No `.trivyignore` governance                 | LOW; no documented exception process | All             |
Stream A: Checksum Verification (T1.1.1 -> T1.1.2); BLOCKING on T0.3.1
Stream B: Signing & Provenance (T1.2.1 -> T1.2.2, T1.3.2); Independent
Stream C: Secret Scanning (T1.3.1); Independent
Stream D: Trivy Hardening (T1.4.1); Independent
Stream E: Hermetic CI (T1.4.2); Independent
# Fallback removed: build fails if primary download fails checksum