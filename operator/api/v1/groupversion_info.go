// =============================================================================
// GroupVersion Info — Defines SchemeBuilder for CRD registration
// =============================================================================
// This is the standard kubebuilder pattern for CRD type registration.
// Without this, the operator cannot compile.
// =============================================================================

package v1

import (
	"k8s.io/apimachinery/pkg/runtime/schema"
	"sigs.k8s.io/controller-runtime/pkg/scheme"
)

var (
	// GroupVersion is group version used to register these objects
	GroupVersion = schema.GroupVersion{Group: "evergreenimageregistry.io", Version: "v1"}

	// SchemeBuilder is used to add go types to the GroupVersionResource scheme
	SchemeBuilder = &scheme.Builder{GroupVersion: GroupVersion}

	// AddToScheme adds the types in this group-version to the given scheme.
	AddToScheme = SchemeBuilder.AddToScheme
)
