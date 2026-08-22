// =============================================================================
// EvergreenDrift CRD Type Definitions
// =============================================================================

package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EvergreenDriftSpec defines the desired state of EvergreenDrift
type EvergreenDriftSpec struct {
	// Check interval in minutes
	// +kubebuilder:default=60
	// +kubebuilder:validation:Minimum=5
	IntervalMinutes int `json:"intervalMinutes,omitempty"`

	// Scope: namespace or cluster
	// +kubebuilder:validation:Enum=namespace;cluster
	// +kubebuilder:default="namespace"
	Scope string `json:"scope,omitempty"`

	// Auto-rollback on drift detection
	// +kubebuilder:default=false
	AutoRollback bool `json:"autoRollback,omitempty"`

	// Alerting configuration
	Alerting AlertingSpec `json:"alerting,omitempty"`

	// Drift thresholds by tier
	Thresholds DriftThresholds `json:"thresholds,omitempty"`
}

// AlertingSpec defines alert targets
type AlertingSpec struct {
	Slack      string `json:"slack,omitempty"`
	PagerDuty  bool   `json:"pagerduty,omitempty"`
	Webhook    string `json:"webhook,omitempty"`
}

// DriftThresholds defines acceptable drift duration by tier
type DriftThresholds struct {
	// Hours before alerting on Tier 1 drift
	// +kubebuilder:default=0
	Critical int `json:"critical,omitempty"`

	// Hours before alerting on Tier 2 drift
	// +kubebuilder:default=3
	Standard int `json:"standard,omitempty"`
}

// EvergreenDriftStatus defines the observed state of EvergreenDrift
type EvergreenDriftStatus struct {
	// Last check timestamp
	LastCheck *metav1.Time `json:"lastCheck,omitempty"`

	// Number of drifts detected
	DriftDetected int `json:"driftDetected,omitempty"`

	// Alert messages
	Alerts []string `json:"alerts,omitempty"`

	// Conditions
	Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Scope",type=string,JSONPath=`.spec.scope`
// +kubebuilder:printcolumn:name="Interval",type=integer,JSONPath=`.spec.intervalMinutes`
// +kubebuilder:printcolumn:name="Drifts",type=integer,JSONPath=`.status.driftDetected`
// +kubebuilder:printcolumn:name="Last Check",type=date,JSONPath=`.status.lastCheck`
// +kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`

// EvergreenDrift is the Schema for the evergrendrifts API
type EvergreenDrift struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   EvergreenDriftSpec   `json:"spec,omitempty"`
	Status EvergreenDriftStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// EvergreenDriftList contains a list of EvergreenDrift
type EvergreenDriftList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []EvergreenDrift `json:"items"`
}

func init() {
	SchemeBuilder.Register(&EvergreenDrift{}, &EvergreenDriftList{})
}
