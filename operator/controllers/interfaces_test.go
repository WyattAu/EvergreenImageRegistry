package controllers

import "testing"

func TestDefaultRegistryClientFailsClosed(t *testing.T) {
	client := NewRegistryClient()

	if _, _, err := client.GetLatestTag("example/image", "1.0.0"); err == nil {
		t.Fatal("expected unconfigured registry client to return an error")
	}
	if _, err := client.GetDigest("example/image:1.0.0"); err == nil {
		t.Fatal("expected unconfigured registry client to return an error")
	}
}

func TestDefaultPolicyEngineRejectsAlpine(t *testing.T) {
	engine := NewPolicyEngine()
	pass, violations, err := engine.Validate("alpine", "3.20")
	if err != nil {
		t.Fatalf("Validate returned error: %v", err)
	}
	if pass || len(violations) != 1 || violations[0].RuleID != "DOCKER-SEC-001" {
		t.Fatalf("unexpected validation result: pass=%v violations=%+v", pass, violations)
	}
}

func TestDefaultPolicyEngineAllowsVersionedImage(t *testing.T) {
	engine := NewPolicyEngine()
	pass, violations, err := engine.Validate("redis", "7.2")
	if err != nil {
		t.Fatalf("Validate returned error: %v", err)
	}
	if !pass || len(violations) != 0 {
		t.Fatalf("unexpected validation result: pass=%v violations=%+v", pass, violations)
	}
}
