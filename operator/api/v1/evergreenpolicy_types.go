// =============================================================================
// EvergreenPolicy CRD Type Definitions
// =============================================================================

package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EvergreenPolicySpec defines the desired state of EvergreenPolicy
type EvergreenPolicySpec struct {
	// Policy scope: namespace or cluster
	// +kubebuilder:validation:Enum=namespace;cluster
	// +kubebuilder:default="namespace"
	Scope string `json:"scope,omitempty"`

	// Policy rules to enforce
	Rules []PolicyRule `json:"rules,omitempty"`

	// Exemptions
	Exemptions []PolicyExemption `json:"exemptions,omitempty"`
}

// PolicyRule defines a single policy rule
type PolicyRule struct {
	// Rule ID (e.g., FIPS-001, PCI-DSS-2.2.1)
	ID string `json:"id"`

	// Rule severity
	// +kubebuilder:validation:Enum=critical;high;medium;low;info
	Severity string `json:"severity"`

	// Whether to enforce (block) or just warn
	// +kubebuilder:default=true
	Enforce bool `json:"enforce,omitempty"`

	// Rule-specific configuration
	Config map[string]string `json:"config,omitempty"`
}

// PolicyExemption defines an image exemption from a policy
type PolicyExemption struct {
	// Image name to exempt
	Image string `json:"image"`

	// Reason for exemption
	Reason string `json:"reason"`

	// Expiration date (optional)
	ExpiresAt *metav1.Time `json:"expiresAt,omitempty"`
}

// EvergreenPolicyStatus defines the observed state of EvergreenPolicy
type EvergreenPolicyStatus struct {
	// Last evaluation timestamp
	LastEvaluated *metav1.Time `json:"lastEvaluated,omitempty"`

	// Total images evaluated
	TotalImages int `json:"totalImages,omitempty"`

	// Total violations found
	Violations int `json:"violations,omitempty"`

	// Violation details
	ViolationDetails []PolicyViolation `json:"violationDetails,omitempty"`
}

// PolicyViolation describes a single policy violation
type PolicyViolation struct {
	Image    string `json:"image"`
	RuleID   string `json:"ruleId"`
	Severity string `json:"severity"`
	Message  string `json:"message"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Scope",type=string,JSONPath=`.spec.scope`
// +kubebuilder:printcolumn:name="Rules",type=integer,JSONPath=`.spec.rules`
// +kubebuilder:printcolumn:name="Violations",type=integer,JSONPath=`.status.violations`
// +kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`

// EvergreenPolicy is the Schema for the evergreenpolicies API
type EvergreenPolicy struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   EvergreenPolicySpec   `json:"spec,omitempty"`
	Status EvergreenPolicyStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// EvergreenPolicyList contains a list of EvergreenPolicy
type EvergreenPolicyList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []EvergreenPolicy `json:"items"`
}

func init() {
	SchemeBuilder.Register(&EvergreenPolicy{}, &EvergreenPolicyList{})
}
