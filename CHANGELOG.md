### evergreenctl 1.1.1: HIPAA INT-01 RE2-safe rewrite; Python shadow evaluator removed
  negative lookahead (`FROM\s+(?!scratch|cgr\.dev|...)`), which neither RE2 nor regorus can compile; under `rego-eval`
### evergreenctl 1.1.0: Rego evaluation behind `rego-eval` (regorus)
  - Adopts `regorus` 0.12 (Microsoft's OPA-compatible Rego interpreter) to evaluate the 10 built-in policy bundles -
  - Rego dialect auto-detection per rule: regorus v1 (default) first, v0 fallback; both the generated v0 bundles and
    OPA/RE2 nor regorus can evaluate; the rule could never have fired. New form flags each unpinned non-scratch `FROM`
- **read-only-rootfs label**: 100% (997/997); `evergreen.security.read-only-rootfs="true"`
- **seccomp label**: 100% (997/997); `evergreen.security.seccomp="runtime-default"`
| R15          |;          |;             | Regression fixes, chmod arg order       |
| R16          |;          |;             | addgroup arg order (35 images)          |
| R17          |;          |;             | 50 dewhitespace'd RUN/COPY, missing git |
- **Round 15 (0b942149):** 27 files; 2 elasticsearch user creation, 1 elasticsearch-exporter chmod, 24 chmod arg order
- **Option B (44ae9637):** 14 files; CI timeout 180→360min, per-image 15min cap, 13 version updates via GitHub API
- **Round 16 (c10a6456):** 37 files; 35 addgroup argument order, 1 git-secrets curl, 1 pip-audit
- **Round 17 (11d33f3d):** 53 files; 50 dewhitespace'd indented Dockerfile instructions, 7 unterminated quotes, 2
- **Round 18 (a247ae25):** 5 files; 5 missing git clone before bare URL
- **Round 19 (b04118a0):** 11 files; 7 version URL fixes (cinny, element-web, node-exporter, roundcube,
- **Round 19.1 (23964c92):** 1 file; graylog-sidecar broken placeholder echo
- **Round 19.2 (f9b6f17d):** 1 file; linguist pkg-config + libgit2-dev
- **Round 20 (ab1fb16e):** 31 files; envoy 1.29→1.38 (×5), etcd 3.5.15→3.6.10 (×3), dendrite 0.13→0.13.8 (×3), gitea
- **Round 20b (bb1a4404):** 11 files; argocd 2.14→3.3.8 (×5), cubrid, datadog-agent, drone 2.28.1→2.28.2 (×3), whoogle
- **Round 20c (7fe0c7cb):** 3 files; adempiere, gitserver, sbt
- **Round 20d (50ed2acc):** 1 file; mattermost-bridge
- **Round 23 (e491bdb0):** 1 file; linguist libicu-dev for charlock_holmes gem
- **chmod arg order:** `chmod +x 2>/dev/null || true /path` is wrong; redirect parsed before target
- **Indented Dockerfile instructions:** `  RUN cmd` is NOT a valid Dockerfile instruction in BuildKit; dewhitespace
- **CAP_DROP label**: 0% → 100% (997/997 images); `evergreen.security.cap-drop="ALL"`
- **no-new-privileges label**: 0% → 100% (997/997 images); `evergreen.security.no-new-privileges="true"`
- **TOML fixes**: 7 broken manifests fixed (WireGuard ecosystem; unquoted port strings in TOML arrays)
- **Wolfi package audit report:** `.reports/wolfi_package_audit.md`; 2,615-line detailed per-image analysis.
- **Wolfi invalid packages JSON:** `.reports/wolfi_invalid_packages.json`; structured data for future CI integration.
- **HC-001:** Fixed HEALTHCHECK for ALL 104 scratch images; converted shell-form to exec-form with absolute path
- **HC-002:** Fixed HEALTHCHECK for ALL 7 distroless images; converted to exec-form
- **TST-001:** Fixed test framework arithmetic bug; `|| ((failed++)) || ((passed++))` replaced with proper if/else
- **Trivy:** Removed `ignore-unfixed: true`; now scans ALL CVEs including unfixed
- **Master Plan:** `.specs/08_roadmap/master_plan.toml`; 47 tasks across 7 phases
- **Phase 0 Plan:** `.specs/08_roadmap/phase_0_plan.md`; Detailed execution specification