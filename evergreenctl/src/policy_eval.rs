// =============================================================================
// Evergreenctl — Rego Policy Evaluation (regorus)
// =============================================================================
// Real Rego evaluation of policy bundles via the `regorus` interpreter
// (Microsoft's OPA-compatible Rego engine). Gated behind the `rego-eval`
// feature so the default build stays dependency-light.
//
// This replaces the drifting Python shadow evaluator (scripts/rego_evaluate.py)
// as the source of truth for bundle semantics: rules are evaluated exactly as
// written, and any rule the engine cannot compile or evaluate surfaces as a
// typed `EvalError` — never as a silent pass.
//
// Semantics:
//   - `deny[msg]` and `warn[msg]` outputs are collected as violations.
//   - A `default deny = false` that does not fire is not a violation.
//   - Builtins that fail at runtime (e.g. an invalid regex) produce
//     `PolicyVerdict::EvalError` (strict builtin errors, fail-closed).
//   - For bundles, the first rule-level eval error fails the whole verdict
//     (fail-closed): violations from sibling rules are discarded so a
//     partially-evaluated bundle can never be reported as Compliant.
// =============================================================================

use serde::{Deserialize, Serialize};

use crate::policy::{PolicyBundle, PolicyInput, PolicyRule};

/// A single rule violation produced by Rego evaluation.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Violation {
    /// The policy rule ID (e.g. `DOCKER-SEC-001`).
    pub rule: String,
    /// The message produced by the Rego `deny`/`warn` rule.
    pub message: String,
}

/// Verdict of evaluating Rego policy code against an input document.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum PolicyVerdict {
    /// Every rule evaluated and none fired.
    Compliant,
    /// At least one rule fired.
    Violations(Vec<Violation>),
    /// The rules could not be compiled or evaluated. Fail-closed: callers
    /// must treat this as "unknown", never as compliant.
    EvalError(String),
}

impl PolicyVerdict {
    /// True if this verdict is a typed evaluation error.
    pub fn is_eval_error(&self) -> bool {
        matches!(self, PolicyVerdict::EvalError(_))
    }

    /// Violations, if any. `None` for `Compliant` and `EvalError`.
    pub fn violations(&self) -> Option<&[Violation]> {
        match self {
            PolicyVerdict::Violations(v) => Some(v),
            _ => None,
        }
    }
}

impl std::fmt::Display for PolicyVerdict {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PolicyVerdict::Compliant => write!(f, "COMPLIANT"),
            PolicyVerdict::Violations(v) => write!(f, "VIOLATIONS ({})", v.len()),
            PolicyVerdict::EvalError(_) => write!(f, "EVAL_ERROR"),
        }
    }
}

/// Evaluate a single policy rule's `rego_code` against the input.
pub fn eval_rule(rule: &PolicyRule, input: &PolicyInput) -> PolicyVerdict {
    let input_value = match input_document(input) {
        Ok(value) => value,
        Err(message) => {
            return PolicyVerdict::EvalError(format!("failed to serialize policy input: {message}"))
        }
    };

    let policy_path = format!("{}.rego", rule.id);
    let mut engine = match build_engine(&policy_path, &rule.rego_code) {
        Ok(engine) => engine,
        Err(message) => return PolicyVerdict::EvalError(message),
    };

    engine.set_input(input_value);
    // Strict builtin errors: a failing builtin (e.g. an invalid regex) is an
    // EvalError, never a silently-skipped expression. regorus already defaults
    // to strict; set it explicitly so this stays true across upgrades.
    engine.set_strict_builtin_errors(true);

    match eval_engine(&mut engine) {
        Ok(messages) => verdict_from_messages(&rule.id, messages),
        Err(message) => PolicyVerdict::EvalError(message),
    }
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
// Engine plumbing
// ---------------------------------------------------------------------------

/// Compile a policy source into an engine, auto-detecting Rego dialect.
///
/// regorus defaults to Rego v1, where `deny[msg] { ... }` (no `if` keyword)
/// is a parse error; legacy bundles in this crate use v0 syntax while the
/// standalone `policies/*.rego` files use `import rego.v1`. Try v1 first,
/// then retry v0 — the two dialects are mutually exclusive at parse time.
fn build_engine(policy_path: &str, rego_code: &str) -> Result<regorus::Engine, String> {
    let mut engine = regorus::Engine::new();
    if engine
        .add_policy(policy_path.to_string(), rego_code.to_string())
        .is_ok()
    {
        return Ok(engine);
    }

    let mut engine = regorus::Engine::new();
    engine.set_rego_v0(true);
    engine
        .add_policy(policy_path.to_string(), rego_code.to_string())
        .map_err(|e| format!("failed to compile policy: {e}"))?;
    Ok(engine)
}

/// Build the Rego input document.
///
/// `None` fields are stripped rather than serialized as `null`: in Rego,
/// `null` is a *defined* value, so `not input.sbom` would be false for a
/// stripped `None` and the rule would silently never fire.
fn input_document(input: &PolicyInput) -> Result<regorus::Value, String> {
    let mut json = serde_json::to_value(input).map_err(|e| format!("serialization failed: {e}"))?;
    if let serde_json::Value::Object(ref mut map) = json {
        map.retain(|_, value| !value.is_null());
    }
    let json_str = json.to_string();
    regorus::Value::from_json_str(&json_str).map_err(|e| format!("invalid input document: {e}"))
}

/// Evaluate `data` and collect all `deny`/`warn` outputs.
fn eval_engine(engine: &mut regorus::Engine) -> Result<Vec<String>, String> {
    let results = engine
        .eval_query("data".to_string(), false)
        .map_err(|e| format!("evaluation failed: {e}"))?;

    let expression = results
        .result
        .first()
        .and_then(|r| r.expressions.first())
        .ok_or_else(|| "evaluation returned no expressions".to_string())?;

    let json: serde_json::Value = serde_json::to_value(&expression.value)
        .map_err(|e| format!("result export failed: {e}"))?;

    let mut messages = Vec::new();
    collect_rule_outputs(&json, &mut messages);
    Ok(messages)
}

/// Recursively collect `deny`/`warn` values from a data document.
///
/// Rules live in arbitrary packages, so walk the whole document instead of
/// hard-coding package names.
fn collect_rule_outputs(value: &serde_json::Value, out: &mut Vec<String>) {
    match value {
        serde_json::Value::Object(map) => {
            for (key, val) in map {
                if key == "deny" || key == "warn" {
                    append_rule_output(val, out);
                }
                collect_rule_outputs(val, out);
            }
        }
        serde_json::Value::Array(items) => {
            for item in items {
                collect_rule_outputs(item, out);
            }
        }
        _ => {}
    }
}

/// Extract violation messages from one rule's output document.
fn append_rule_output(value: &serde_json::Value, out: &mut Vec<String>) {
    match value {
        // `default deny = false` that never fired — not a violation.
        serde_json::Value::Bool(false) | serde_json::Value::Null => {}
        serde_json::Value::Bool(true) => out.push("rule fired".to_string()),
        serde_json::Value::String(message) => out.push(message.clone()),
        // Sets and multi-value rules serialize as arrays...
        serde_json::Value::Array(items) => {
            for item in items {
                append_rule_output(item, out);
            }
        }
        serde_json::Value::Object(map) => {
            // ...but regorus serializes a v1 `deny[msg] if { ... }` partial
            // set as `{msg: true}` (the keys are the messages), while v0
            // bundles and `deny contains msg if` produce string arrays.
            // Accept both shapes: a boolean-`true` value means the key IS
            // the message; anything else is a nested document to recurse
            // into.
            for (key, val) in map {
                if val == &serde_json::Value::Bool(true) {
                    out.push(key.clone());
                } else {
                    append_rule_output(val, out);
                }
            }
        }
        other => out.push(other.to_string()),
    }
}

fn verdict_from_messages(rule_id: &str, mut messages: Vec<String>) -> PolicyVerdict {
    if messages.is_empty() {
        return PolicyVerdict::Compliant;
    }
    messages.sort();
    messages.dedup();
    PolicyVerdict::Violations(
        messages
            .into_iter()
            .map(|message| Violation {
                rule: rule_id.to_string(),
                message,
            })
            .collect(),
    )
}

// ---------------------------------------------------------------------------
// Tests
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
