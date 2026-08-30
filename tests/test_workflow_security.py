from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _workflow(name: str) -> str:
    return (ROOT / ".github" / "workflows" / name).read_text()


def test_push_lint_gate_is_blocking():
    text = _workflow("build-on-push.yml")
    lint_start = text.index("      - name: Run hadolint")
    lint_end = text.index("      - name: Validate entrypoint patterns", lint_start)
    block = text[lint_start:lint_end]
    assert "continue-on-error" not in block
    assert "|| echo" not in block
    assert "hadolint/hadolint-action@" in text


def test_cis_shell_and_package_checks_are_blocking():
    text = _workflow("cis-gate.yml")
    assert "CIS 4.4.3 — No shell in final stage\n        continue-on-error" not in text
    assert "CIS 4.4.3 — No package manager in final stage\n        continue-on-error" not in text
    assert "CIS 4.4.3 FAIL: Shell installed in final stage" in text
    assert "CIS 4.4.3 FAIL: Package manager used in final stage" in text


def test_lint_cargo_audit_install_is_fail_closed():
    text = _workflow("lint.yml")
    start = text.index("      - name: Run cargo audit")
    end = text.index("      - name: Run cargo test", start)
    assert "cargo install cargo-audit --locked\n" in text[start:end]
    assert "|| true" not in text[start:end]


def test_reusable_build_fails_on_batch_or_attestation_failures():
    text = _workflow("_build-reusable.yml")
    assert "::error::${FAILED} image(s) failed to build" in text
    assert "All ${FAILED} images failed" not in text
    assert "Sign/Attest: ${SIGNED} signed, ${ATTESTED} SLSA attested, ${FAILED} failed" in text
    assert "::error::${FAILED} image attestation operation(s) failed" in text
    assert "Sign failed for ${image} (non-blocking)" not in text


def test_daily_security_scan_does_not_accept_missing_scan_results():
    text = _workflow("daily-security-scan.yml")
    assert 'could not pull for SBOM generation' in text
    assert 'Failed to generate SBOM for ${image}' in text
    assert 'trivy image \\\n              --severity CRITICAL,HIGH,MEDIUM,LOW \\\n              --ignore-unfixed=false \\\n              --format json \\\n              --output "/tmp/trivy-results/${SAFE}.json" \\\n              "$ref" 2>/dev/null || true' not in text


def test_compliance_scan_supply_chain_verification_is_blocking():
    text = _workflow("compliance-scan.yml")
    assert "Verify supply chain\n        id: supply\n        continue-on-error" not in text
    assert "SPDX attestation verification failed" in text
    assert "CIS no-SUID check failed" in text
