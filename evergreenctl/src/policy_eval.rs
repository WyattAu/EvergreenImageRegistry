// =============================================================================
// Evergreenctl — Rego Policy Evaluation (policy-kit adapter)
// =============================================================================
// Generic Rego evaluation (bundle loading, dialect auto-detect, fail-closed
// aggregation, strict builtin errors, null-stripping) lives in `policy-kit`
// (crates.io, extracted from this very module). This adapter keeps only the
// Dockerfile-specific parts: the EIR input shaping (`PolicyInput` → JSON)
// and the per-rule engine isolation that lets EIR rule bundles reuse
// package names (`package evergreen.dockerfile` in many rules).
//
// Semantics are unchanged from the 1.1.x in-tree evaluator:
//   - `deny[msg]` and `warn[msg]` outputs are collected as violations
//     (v0 string-array form and v1 `{msg: true}` map form both handled by
//     policy-kit).
//   - A `default deny = false` that does not fire is not a violation.
//   - Builtins that fail at runtime (e.g. an invalid regex) produce
//     `PolicyVerdict::EvalError` (strict builtin errors, fail-closed).
//   - For bundles, the first rule-level eval error fails the whole verdict
//     (fail-closed): violations from sibling rules are discarded so a
//     partially-evaluated bundle can never be reported as Compliant.
// =============================================================================

use crate::policy::{PolicyBundle, PolicyInput, PolicyRule};

pub use policy_kit::{PolicyVerdict, Violation};

/// Build a policy-kit bundle from an EIR rule. The rule ID names the kit
/// bundle, so every violation it produces is tagged with the rule ID —
/// exactly the pre-extraction `Violation { rule: rule_id, .. }` shape.
fn kit_bundle(rule: &PolicyRule) -> policy_kit::PolicyBundle {
    policy_kit::PolicyBundle::new(rule.id.clone(), rule.rego_code.clone())
}

/// Serialize the policy input to its JSON document. `None` fields serialize
/// as `null` and are stripped by policy-kit before evaluation (a JSON null
/// is *defined* in Rego and would defeat `not input.x`).
fn input_document(input: &PolicyInput) -> Result<serde_json::Value, String> {
    serde_json::to_value(input).map_err(|e| format!("failed to serialize policy input: {e}"))
}

/// Evaluate a single policy rule's `rego_code` against the input.
pub fn eval_rule(rule: &PolicyRule, input: &PolicyInput) -> PolicyVerdict {
    let input_value = match input_document(input) {
        Ok(value) => value,
        Err(message) => return PolicyVerdict::EvalError(message),
    };

    let mut engine = policy_kit::PolicyEngine::new();
    if let Err(error) = engine.add_bundle(kit_bundle(rule)) {
        return PolicyVerdict::EvalError(format!("failed to compile policy: {error}"));
    }

    engine.evaluate_bundle(&rule.id, &input_value)
}

/// Evaluate every rule in a bundle against the input.
///
/// Fail-closed: if any rule errors, the whole bundle verdict is `EvalError`.
pub fn eval_bundle(bundle: &PolicyBundle, input: &PolicyInput) -> PolicyVerdict {
    let mut violations = Vec::new();

    for rule in &bundle.rules {
        match eval_rule(rule, input) {
            PolicyVerdict::Compliant => {}
            PolicyVerdict::Violations(mut found) => violations.append(&mut found),
            PolicyVerdict::EvalError(message) => {
                return PolicyVerdict::EvalError(format!("{message} (rule {})", rule.id));
            }
        }
    }

    if violations.is_empty() {
        PolicyVerdict::Compliant
    } else {
        PolicyVerdict::Violations(violations)
    }
}

/// Evaluate all built-in policy bundles against the input.
///
/// Returns one verdict per bundle, in bundle order.
pub fn eval_builtins(input: &PolicyInput) -> Vec<(String, PolicyVerdict)> {
    crate::policy::built_in_policies()
        .iter()
        .map(|bundle| (bundle.id.clone(), eval_bundle(bundle, input)))
        .collect()
}

// ---------------------------------------------------------------------------
// Tests — the Dockerfile-rule suites, now exercising the policy-kit adapter
// end to end (these are the same cases that validated the in-tree evaluator).
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    /// A Dockerfile that should pass every built-in bundle: approved
    /// digest-pinned base, USER 65532, HEALTHCHECK, OCI labels, no secrets.
    const COMPLIANT_DOCKERFILE: &str = "\
FROM cgr.dev/chainguard/wolfi-base@sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
COPY app /app
HEALTHCHECK CMD /app/health || exit 1
LABEL org.opencontainers.image.source=https://github.com/example/app
USER 65532
ENTRYPOINT [\"/app\"]
";

    /// Multi-line Dockerfile where the banned `alpine` FROM is NOT on line 1.
    /// Regression test for the missing `(?m)` anchor: the old `(?i)^` pattern
    /// only ever matched line 1, so this slipped through.
    const MULTILINE_ALPINE_DOCKERFILE: &str = "\
# syntax=docker/dockerfile:1
ARG GO_VERSION=1.22
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN go build -o /out/app .
FROM alpine:3.18
COPY --from=build /out/app /app
USER 65532
ENTRYPOINT [\"/app\"]
";

    fn input_for(dockerfile: &str) -> PolicyInput {
        PolicyInput {
            image: "test-image".to_string(),
            dockerfile: Some(dockerfile.to_string()),
            manifest: None,
            sbom: None,
            labels: HashMap::new(),
        }
    }

    fn dockerfile_security_bundle() -> PolicyBundle {
        crate::policy::built_in_policies()
            .into_iter()
            .find(|b| b.id == "dockerfile-security")
            .expect("dockerfile-security bundle exists")
    }

    fn supply_chain_bundle() -> PolicyBundle {
        crate::policy::built_in_policies()
            .into_iter()
            .find(|b| b.id == "supply-chain")
            .expect("supply-chain bundle exists")
    }

    #[test]
    fn test_compliant_dockerfile_is_compliant() {
        let input = input_for(COMPLIANT_DOCKERFILE);
        for (bundle_id, verdict) in eval_builtins(&input) {
            assert_eq!(
                verdict,
                PolicyVerdict::Compliant,
                "bundle {bundle_id} should be compliant"
            );
        }
    }

    #[test]
    fn test_multiline_alpine_from_not_on_first_line_is_flagged() {
        // Anchor regression: alpine FROM appears on line 7, not line 1.
        let input = input_for(MULTILINE_ALPINE_DOCKERFILE);
        let verdict = eval_bundle(&dockerfile_security_bundle(), &input);

        let violations = match &verdict {
            PolicyVerdict::Violations(v) => v,
            other => panic!("expected violations, got {other:?}"),
        };
        assert!(
            violations
                .iter()
                .any(|v| v.rule == "DOCKER-SEC-001" && v.message.contains("Alpine")),
            "alpine FROM on a non-first line must be flagged: {violations:?}"
        );
    }

    #[test]
    fn test_digest_pinning_rule_flags_unpinned_from() {
        let input = input_for(MULTILINE_ALPINE_DOCKERFILE);
        let verdict = eval_bundle(&supply_chain_bundle(), &input);

        let violations = verdict.violations().expect("expected violations");
        assert!(
            violations
                .iter()
                .any(|v| v.rule == "SC-002" && v.message.contains("digest-pinned")),
            "unpinned FROM lines must be flagged: {violations:?}"
        );
    }

    #[test]
    fn test_digest_pinned_from_passes_supply_chain() {
        let input = input_for(COMPLIANT_DOCKERFILE);
        let verdict = eval_bundle(&supply_chain_bundle(), &input);
        assert_eq!(verdict, PolicyVerdict::Compliant);
    }

    #[test]
    fn test_hipaa_int01_allowlist_is_re2_safe_and_fires() {
        // Regression: HIPAA-INT-01 (policies/hipaa.rego) used a negative
        // lookahead — RE2-incompatible, so under rego-eval the rule surfaced
        // as EvalError (fail-closed) instead of ever firing. The rewritten
        // rule enumerates the allowlist with negated startswith checks; this
        // test compiles and evaluates the real standalone policy file.
        let rule = PolicyRule {
            id: "HIPAA-INT-01".to_string(),
            name: "Image integrity".to_string(),
            description: "HIPAA base-image allowlist (standalone policies/hipaa.rego)".to_string(),
            severity: crate::policy::PolicySeverity::High,
            rego_code: include_str!("../policies/hipaa.rego").to_string(),
            remediation: "Use an approved base image".to_string(),
            tags: vec![],
        };
        const INT01_MSG: &str = "Only approved base images allowed";

        // Unapproved base (alpine) → the allowlist rule must fire.
        let verdict = eval_rule(&rule, &input_for("FROM alpine:3.20\nUSER 65532\n"));
        let violations = verdict.violations().expect("unapproved base must violate");
        assert!(
            violations.iter().any(|v| v.message.contains(INT01_MSG)),
            "HIPAA-INT-01 must flag alpine: {violations:?}"
        );

        // Multi-stage: approved build stage, unapproved final stage → fires.
        let multi_stage = "\
FROM cgr.dev/chainguard/wolfi-base AS build
COPY . .
RUN make
FROM alpine:3.20
COPY --from=build /out /app
USER 65532
";
        let verdict = eval_rule(&rule, &input_for(multi_stage));
        let violations = verdict
            .violations()
            .expect("unapproved final stage must violate");
        assert!(
            violations
                .iter()
                .any(|v| v.message.contains(INT01_MSG) && v.message.contains("alpine")),
            "HIPAA-INT-01 must flag the unapproved second stage: {violations:?}"
        );

        // All-approved bases (scratch exactly, cgr.dev, distroless, ubi) →
        // the allowlist rule must stay quiet.
        let approved = "\
FROM scratch
COPY app /app
USER 65532
";
        for dockerfile in [approved, "FROM gcr.io/distroless/static\nUSER 65532\n"] {
            let verdict = eval_rule(&rule, &input_for(dockerfile));
            assert!(
                verdict
                    .violations()
                    .map(|v| v.iter().all(|v| !v.message.contains(INT01_MSG)))
                    .unwrap_or(true),
                "approved base must not violate HIPAA-INT-01: {verdict:?}"
            );
        }
    }

    #[test]
    fn test_eval_error_is_typed_for_unsupported_regex() {
        // Lookahead is RE2-incompatible: the builtin fails at runtime and
        // must surface as EvalError, not as a pass.
        let rule = PolicyRule {
            id: "TEST-EVAL-ERR".to_string(),
            name: "Broken regex".to_string(),
            description: "uses lookahead".to_string(),
            severity: crate::policy::PolicySeverity::High,
            rego_code: r#"
package evergreen.test

deny[msg] {
    input.dockerfile
    regex.match("(?i)^\\s*FROM\\s+(?!scratch)", input.dockerfile)
    msg := "unreachable"
}
"#
            .to_string(),
            remediation: "n/a".to_string(),
            tags: vec![],
        };

        let verdict = eval_rule(&rule, &input_for(COMPLIANT_DOCKERFILE));
        match verdict {
            PolicyVerdict::EvalError(message) => {
                assert!(!message.is_empty());
            }
            other => panic!("expected EvalError, got {other:?}"),
        }
    }

    #[test]
    fn test_bundle_eval_error_is_fail_closed() {
        // A bundle with one broken rule must not surface partial violations
        // (or compliance) — the EvalError wins.
        let bundle = PolicyBundle {
            id: "broken-bundle".to_string(),
            version: "1.0.0".to_string(),
            description: "one good rule, one broken rule".to_string(),
            domain: crate::policy::PolicyDomain::Custom,
            rules: vec![
                PolicyRule {
                    id: "GOOD-001".to_string(),
                    name: "Flags everything".to_string(),
                    description: "always fires".to_string(),
                    severity: crate::policy::PolicySeverity::Low,
                    rego_code: r#"
package evergreen.test.good

deny[msg] {
    input.dockerfile
    msg := "always fires"
}
"#
                    .to_string(),
                    remediation: "n/a".to_string(),
                    tags: vec![],
                },
                PolicyRule {
                    id: "BROKEN-001".to_string(),
                    name: "Broken regex".to_string(),
                    description: "uses lookahead".to_string(),
                    severity: crate::policy::PolicySeverity::Low,
                    rego_code: r#"
package evergreen.test.broken

deny[msg] {
    input.dockerfile
    regex.match("(?P<named>unsupported|lookahead(?!x))", input.dockerfile)
    msg := "unreachable"
}
"#
                    .to_string(),
                    remediation: "n/a".to_string(),
                    tags: vec![],
                },
            ],
            metadata: HashMap::new(),
        };

        let verdict = eval_bundle(&bundle, &input_for(COMPLIANT_DOCKERFILE));
        assert!(
            matches!(verdict, PolicyVerdict::EvalError(ref m) if m.contains("BROKEN-001")),
            "bundle eval must fail closed: {verdict:?}"
        );
    }

    #[test]
    fn test_v0_and_v1_dialects_both_evaluate() {
        // v0 syntax (no `if` keyword) — used by the generated bundles.
        let v0 = PolicyRule {
            id: "DIALECT-V0".to_string(),
            name: "v0".to_string(),
            description: String::new(),
            severity: crate::policy::PolicySeverity::Low,
            rego_code: r#"
package evergreen.test.v0

deny[msg] {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    msg := "v0 fired"
}
"#
            .to_string(),
            remediation: String::new(),
            tags: vec![],
        };
        // v1 syntax (`import rego.v1` + `if`) — used by policies/*.rego.
        let v1 = PolicyRule {
            id: "DIALECT-V1".to_string(),
            name: "v1".to_string(),
            description: String::new(),
            severity: crate::policy::PolicySeverity::Low,
            rego_code: r#"
package evergreen.test.v1

import rego.v1

deny[msg] if {
    input.dockerfile
    contains(input.dockerfile, "FROM")
    msg := "v1 fired"
}
"#
            .to_string(),
            remediation: String::new(),
            tags: vec![],
        };

        for rule in [&v0, &v1] {
            let verdict = eval_rule(rule, &input_for("FROM scratch"));
            assert!(
                matches!(&verdict, PolicyVerdict::Violations(v) if v.len() == 1),
                "{} dialect should evaluate: {verdict:?}",
                rule.id
            );
        }
    }

    #[test]
    fn test_missing_dockerfile_rules_do_not_fire() {
        // Without a dockerfile, dockerfile-scoped rules must stay quiet.
        let input = PolicyInput {
            image: "test-image".to_string(),
            dockerfile: None,
            manifest: None,
            sbom: None,
            labels: HashMap::new(),
        };
        let verdict = eval_bundle(&dockerfile_security_bundle(), &input);
        assert_eq!(verdict, PolicyVerdict::Compliant);
    }
}
