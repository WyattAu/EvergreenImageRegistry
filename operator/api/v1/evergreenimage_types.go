// =============================================================================
// EvergreenImage CRD Type Definitions
// =============================================================================
// Kubebuilder markers for CRD generation, RBAC, and webhook configuration.
// =============================================================================

package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EvergreenImageSpec defines the desired state of EvergreenImage
type EvergreenImageSpec struct {
	// Image reference (e.g., ghcr.io/wyattau/evergreenimageregistry/redis)
	// +kubebuilder:validation:Required
	Image string `json:"image"`

	// Image tag to track
	// +kubebuilder:default="latest"
	Tag string `json:"tag,omitempty"`

	// Enable automatic updates on new versions
	// +kubebuilder:default=false
	AutoUpdate bool `json:"autoUpdate,omitempty"`

	// Kubernetes update strategy
	// +kubebuilder:validation:Enum=rolling;recreate
	// +kubebuilder:default="rolling"
	UpdateStrategy string `json:"updateStrategy,omitempty"`

	// Compliance requirements
	Compliance ComplianceSpec `json:"compliance,omitempty"`

	// Notification configuration
	Notifications NotificationsSpec `json:"notifications,omitempty"`
}

// ComplianceSpec defines compliance requirements for the image
type ComplianceSpec struct {
	// Require valid SBOM
	// +kubebuilder:default=true
	RequireSBOM bool `json:"requireSBOM,omitempty"`

	// Require VEX document
	// +kubebuilder:default=false
	RequireVEX bool `json:"requireVEX,omitempty"`

	// Require FIPS compliance
	// +kubebuilder:default=false
	FIPSRequired bool `json:"fipsRequired,omitempty"`
}

// NotificationsSpec defines notification targets
type NotificationsSpec struct {
	// Slack channel for notifications
	Slack string `json:"slack,omitempty"`

	// Enable PagerDuty alerts
	// +kubebuilder:default=false
	PagerDuty bool `json:"pagerduty,omitempty"`
}

// EvergreenImageStatus defines the observed state of EvergreenImage
type EvergreenImageStatus struct {
	// Current image tag
	CurrentTag string `json:"currentTag,omitempty"`

	// Current image digest
	CurrentDigest string `json:"currentDigest,omitempty"`

	// Last update timestamp
	LastUpdated *metav1.Time `json:"lastUpdated,omitempty"`

	// SBOM status
	// +kubebuilder:validation:Enum=valid;missing;stale
	SBOMStatus string `json:"sbomStatus,omitempty"`

	// Compliance status
	// +kubebuilder:validation:Enum=passing;failing;unknown
	ComplianceStatus string `json:"complianceStatus,omitempty"`

	// Conditions
	Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Image",type=string,JSONPath=`.spec.image`
// +kubebuilder:printcolumn:name="Tag",type=string,JSONPath=`.spec.tag`
// +kubebuilder:printcolumn:name="Auto Update",type=boolean,JSONPath=`.spec.autoUpdate`
// +kubebuilder:printcolumn:name="SBOM",type=string,JSONPath=`.status.sbomStatus`
// +kubebuilder:printcolumn:name="Compliance",type=string,JSONPath=`.status.complianceStatus`
// +kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`

// EvergreenImage is the Schema for the evergreenimages API
type EvergreenImage struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   EvergreenImageSpec   `json:"spec,omitempty"`
	Status EvergreenImageStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// EvergreenImageList contains a list of EvergreenImage
type EvergreenImageList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []EvergreenImage `json:"items"`
}

func init() {
	SchemeBuilder.Register(&EvergreenImage{}, &EvergreenImageList{})
}
