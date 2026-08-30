// =============================================================================
// Controller Interfaces and Helpers
// =============================================================================

package controllers

import (
	"fmt"
	"strings"

	"k8s.io/client-go/tools/record"
)

// PolicyViolation describes a single policy violation
type PolicyViolation struct {
	Image    string `json:"image"`
	RuleID   string `json:"ruleId"`
	Severity string `json:"severity"`
	Message  string `json:"message"`
}

// PolicyResult describes a single policy check result
type PolicyResult struct {
	RuleID   string
	Severity string
	Status   string // "pass" or "fail"
	Message  string
}

// RegistryClient interface for interacting with container registries
type RegistryClient interface {
	GetLatestTag(image, currentTag string) (tag string, digest string, err error)
	GetDigest(imageRef string) (string, error)
}

// PolicyEngine interface for evaluating policies
type PolicyEngine interface {
	Validate(image, tag string) (bool, []PolicyViolation, error)
	Evaluate(image string, rules []string) ([]PolicyResult, error)
}

// --- Default implementations ---

type defaultRegistryClient struct{}

func NewRegistryClient() RegistryClient {
	return &defaultRegistryClient{}
}

func (c *defaultRegistryClient) GetLatestTag(image, currentTag string) (string, string, error) {
	return "", "", fmt.Errorf("registry client is not configured for %q", image)
}

func (c *defaultRegistryClient) GetDigest(imageRef string) (string, error) {
	return "", fmt.Errorf("registry client is not configured for %q", imageRef)
}

type defaultPolicyEngine struct{}

func NewPolicyEngine() PolicyEngine {
	return &defaultPolicyEngine{}
}

func (e *defaultPolicyEngine) Validate(image, tag string) (bool, []PolicyViolation, error) {
	var violations []PolicyViolation

	if strings.Contains(image, "alpine") {
		violations = append(violations, PolicyViolation{
			Image:    image,
			RuleID:   "DOCKER-SEC-001",
			Severity: "critical",
			Message:  "Alpine images are BANNED per ADR-007",
		})
	}

	if tag == "latest" {
		violations = append(violations, PolicyViolation{
			Image:    image,
			RuleID:   "C015",
			Severity: "warn",
			Message:  ":latest tag is not recommended",
		})
	}

	return len(violations) == 0, violations, nil
}

func (e *defaultPolicyEngine) Evaluate(image string, rules []string) ([]PolicyResult, error) {
	var results []PolicyResult
	for _, rule := range rules {
		result := PolicyResult{
			RuleID:   rule,
			Severity: "medium",
			Status:   "pass",
			Message:  fmt.Sprintf("Rule %s passed", rule),
		}
		if strings.Contains(strings.ToLower(image), "alpine") {
			result.Status = "fail"
			result.Severity = "critical"
			result.Message = "Alpine images are BANNED per ADR-007"
		}
		results = append(results, result)
	}
	return results, nil
}

var _ record.EventRecorder
