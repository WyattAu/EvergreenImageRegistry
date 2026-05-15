# Architecture Decision Record: Checksum Verification for Downloaded Artifacts

## ADR-002: SHA256 Checksum Verification for All Downloaded Binaries

### Status

ACCEPTED

### Date

2026-04-19

### Author

Nexus (Principal Systems Architect)

### Context

All 124 multi-stage images (Categories A, B, C) download their primary binary via `curl -fsSL` with **zero integrity
verification**:

```dockerfile
RUN curl -fsSL "https://example.com/binary.tar.gz" -o /binary.tar.gz && \
    tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz
```

This creates a critical supply chain attack vector:

1. **MITM attack**: An attacker intercepting the download could inject malicious code
2. **Compromised CDN**: If the release server is compromised, malicious binaries are served
3. **DNS hijacking**: Redirecting download URLs to attacker-controlled servers
4. **Typosquatting**: Similar-looking URLs serving malicious packages

For **military contractors**, this is a blocking security gap. NIST SP 800-53 SA-10 requires developer security and
integrity verification. FIPS 140-2 requires validated cryptographic verification.

### Decision

**Every downloaded artifact must be verified via SHA256 checksum before use.**

#### Implementation Pattern

```dockerfile
# Step 1: Download binary AND checksum file
RUN curl -fsSL "https://example.com/binary-${VERSION}.tar.gz" -o /binary.tar.gz && \
    curl -fsSL "https://example.com/sha256sums.txt" -o /sha256sums.txt

# Step 2: Verify checksum (FAIL BUILD if mismatch)
RUN sha256sum -c sha256sums.txt --ignore-missing

# Step 3: Extract verified binary
RUN tar -xzf /binary.tar.gz -C / && rm /binary.tar.gz /sha256sums.txt
```

#### Fallback Pattern (when upstream doesn't provide checksums)

```dockerfile
# Compute checksum and compare against hardcoded value
RUN EXPECTED_SHA256="abc123..." && \
    ACTUAL_SHA256=$(sha256sum /binary.tar.gz | cut -d' ' -f1) && \
    if [ "$EXPECTED_SHA256" != "$ACTUAL_SHA256" ]; then \
      echo "CHECKSUM MISMATCH: expected $EXPECTED_SHA256, got $ACTUAL_SHA256" && \
      exit 1; \
    fi
```

#### Per-Image CHECKSUMS File

Each image directory will contain a `CHECKSUMS` file:

```
# CHECKSUMS for nginx
# Generated: 2026-04-19
# Source: https://nginx.org/download/
# Verification: Manual download + sha256sum

BINARY_URL=https://nginx.org/download/nginx-1.27.1.tar.gz
BINARY_SHA256=a1b2c3d4e5f6...7890abcdef1234567890abcdef1234567890abcdef1234
CHECKSUM_URL=https://nginx.org/download/nginx-1.27.1.tar.gz.sha256
```

#### Checksum Update Protocol

1. New version released → Security team member downloads binary
2. Computes SHA256 on air-gapped machine
3. Compares against upstream checksum (if available)
4. Cross-validates with second team member
5. Updates CHECKSUMS file in Git
6. PR requires review from second team member

### Consequences

**Positive:**

- Supply chain integrity verified for all artifacts
- Build fails immediately on tampered downloads
- Audit trail for all binary versions
- Meets NIST SP 800-53 SA-10, FIPS 140-2 requirements

**Negative:**

- Additional build step (marginal time increase)
- CHECKSUMS files must be maintained manually
- Some upstream projects don't provide checksum files
- Need process for updating checksums when versions change

**Risks:**

- Checksum file itself could be tampered with if hosted on same server
- Mitigation: Prefer checksums from separate server or GPG-signed checksums
- Some projects only provide GPG signatures, not SHA256
- Mitigation: For GPG-only projects, verify GPG signature in Dockerfile

### Alternatives Considered

| Alternative                          | Pros                          | Cons                                       | Reason Rejected                         |
| ------------------------------------ | ----------------------------- | ------------------------------------------ | --------------------------------------- |
| GPG signature verification           | Cryptographically stronger    | More complex, not all projects provide GPG | Use when available, fall back to SHA256 |
| No verification (current)            | Simplest                      | Supply chain attack vector                 | Security gap                            |
| Verify only in CI, not in Dockerfile | No Dockerfile change          | Doesn't protect local builds               | Must be enforced at build time          |
| Use SLSA provenance instead          | Strong supply chain guarantee | Not available for all upstream projects    | Complementary, not replacement          |

### Multi-Level Verification Strategy

| Level | Method               | When Used                          | Tool                           |
| ----- | -------------------- | ---------------------------------- | ------------------------------ |
| 1     | SHA256 from upstream | Upstream provides sha256 file      | `sha256sum -c`                 |
| 2     | SHA256 hardcoded     | Upstream doesn't provide checksums | Manual computation + hardcoded |
| 3     | GPG signature        | Upstream provides .asc file        | `gpg --verify`                 |
| 4     | Cosign/SLSA          | Upstream publishes provenance      | `cosign verify`                |

### Related Standards

| Standard       | Clause    | Requirement                                   |
| -------------- | --------- | --------------------------------------------- |
| NIST SP 800-53 | SA-10     | Developer security and integrity verification |
| NIST SP 800-53 | CM-3      | Configuration change control                  |
| FIPS 140-2     | Section 4 | Cryptographic module validation               |
| SLSA           | Level 3   | Provenance requirements                       |

### Related Yellow Papers

- YP-SUPPLY-CHAIN-001: Supply Chain Security Theory (AX-001: Cryptographic Integrity)
- YP-SEC-HARDENING-001: Container Security Hardening (DEF-002: Hardened Container)

### Related Constraints

- C012: No embedded secrets (checksums are not secrets, they are integrity checks)

### Implementation Checklist

- [ ] Create CHECKSUMS file template
- [ ] Audit all 124 multi-stage images for download URLs
- [ ] For each URL, find or compute SHA256 checksum
- [ ] Create CHECKSUMS files for all images
- [ ] Update Dockerfiles to verify checksums before extraction
- [ ] Add pre-commit hook to verify CHECKSUMS file exists when Dockerfile uses curl
- [ ] Add CI check that fails build on checksum mismatch
- [ ] Document checksum update protocol in CONTRIBUTING.md
- [ ] For GPG-signed projects, add GPG verification as Level 3

---

**END OF ADR-002**
