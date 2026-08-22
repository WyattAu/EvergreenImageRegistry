// =============================================================================
// Evergreen Admission Webhook
// =============================================================================

package webhooks

import (
	"context"
	"fmt"
	"net/http"
	"strings"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	clientgoscheme "k8s.io/client-go/kubernetes/scheme"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"
	"sigs.k8s.io/controller-runtime/pkg/webhook/admission"
)

var scheme = runtime.NewScheme()

func init() {
	_ = clientgoscheme.AddToScheme(scheme)
}

type EvergreenAdmissionWebhook struct {
	Client client.Client
	DryRun bool
}

func (w *EvergreenAdmissionWebhook) Handle(ctx context.Context, req admission.Request) admission.Response {
	logger := log.FromContext(ctx)

	if req.Kind.Kind != "Pod" {
		return admission.Allowed("not a Pod")
	}

	var pod corev1.Pod
	dec := admission.NewDecoder(scheme)
	if err := dec.Decode(req, &pod); err != nil {
		return admission.Errored(http.StatusBadRequest, err)
	}

	if w.isRestrictedNamespace(req.Namespace) {
		logger.Info("restricted namespace", "namespace", req.Namespace)

		for _, container := range append(pod.Spec.InitContainers, pod.Spec.Containers...) {
			if !w.isEIRImage(container.Image) {
				msg := fmt.Sprintf("Image %s not from EIR registry", container.Image)
				if w.DryRun {
					logger.Info("DRY RUN", "would reject", msg)
				} else {
					return admission.Denied(msg)
				}
			}

			if container.Resources.Limits == nil {
				msg := fmt.Sprintf("Container %s must have resource limits", container.Name)
				if w.DryRun {
					logger.Info("DRY RUN", "would reject", msg)
				} else {
					return admission.Denied(msg)
				}
			}
		}
	}

	return admission.Allowed("pod meets EIR policies")
}

func (w *EvergreenAdmissionWebhook) isRestrictedNamespace(namespace string) bool {
	restricted := []string{"production", "staging", "security"}
	for _, ns := range restricted {
		if namespace == ns {
			return true
		}
	}
	return false
}

func (w *EvergreenAdmissionWebhook) isEIRImage(image string) bool {
	return strings.HasPrefix(image, "ghcr.io/wyattau/evergreenimageregistry/")
}
