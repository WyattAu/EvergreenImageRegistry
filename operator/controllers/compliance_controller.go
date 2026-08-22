// =============================================================================
// Compliance Controller
// =============================================================================

package controllers

import (
	"context"
	"fmt"
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller"
	"sigs.k8s.io/controller-runtime/pkg/log"
	"k8s.io/client-go/tools/record"

	evergreenv1 "github.com/WyattAu/EvergreenImageRegistry/operator/api/v1"
)

type ComplianceReconciler struct {
	client.Client
	Scheme   *runtime.Scheme
	Recorder record.EventRecorder
	Policy   PolicyEngine
}

// +kubebuilder:rbac:groups=evergreenimageregistry.io,resources=evergreenpolicies,verbs=get;list;watch;update;patch
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch

func (r *ComplianceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	var policy evergreenv1.EvergreenPolicy
	if err := r.Get(ctx, req.NamespacedName, &policy); err != nil {
		if errors.IsNotFound(err) {
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	logger.Info("evaluating policy", "name", policy.Name, "scope", policy.Spec.Scope)

	var images []string
	if policy.Spec.Scope == "namespace" {
		images = r.getNamespaceImages(ctx, policy.Namespace)
	} else {
		images = r.getAllImages(ctx)
	}

	var violations []PolicyViolation
	ruleIDs := make([]string, 0, len(policy.Spec.Rules))
	for _, rule := range policy.Spec.Rules {
		ruleIDs = append(ruleIDs, rule.ID)
	}

	for _, img := range images {
		results, err := r.Policy.Evaluate(img, ruleIDs)
		if err != nil {
			logger.Error(err, "evaluation failed", "image", img)
			continue
		}
		for _, result := range results {
			if result.Status == "fail" {
				violations = append(violations, PolicyViolation{
					Image:    img,
					RuleID:   result.RuleID,
					Severity: result.Severity,
					Message:  result.Message,
				})
				msg := fmt.Sprintf("policy %s: %s", result.RuleID, result.Message)
				r.Recorder.Event(&policy, corev1.EventTypeWarning, "Violation", msg)
			}
		}
	}

	policy.Status.LastEvaluated = &metav1.Time{Time: time.Now()}
	policy.Status.TotalImages = len(images)
	policy.Status.Violations = len(violations)
	// Convert internal violations to API violations
	var apiViolations []evergreenv1.PolicyViolation
	for _, v := range violations {
		apiViolations = append(apiViolations, evergreenv1.PolicyViolation{
			Image:    v.Image,
			RuleID:   v.RuleID,
			Severity: v.Severity,
			Message:  v.Message,
		})
	}
	policy.Status.ViolationDetails = apiViolations

	if err := r.Status().Update(ctx, &policy); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{RequeueAfter: time.Hour}, nil
}

func (r *ComplianceReconciler) getNamespaceImages(ctx context.Context, namespace string) []string {
	var deployments appsv1.DeploymentList
	if err := r.List(ctx, &deployments, client.InNamespace(namespace)); err != nil {
		return nil
	}
	images := map[string]bool{}
	for _, dep := range deployments.Items {
		for _, c := range dep.Spec.Template.Spec.Containers {
			images[c.Image] = true
		}
	}
	result := make([]string, 0, len(images))
	for img := range images {
		result = append(result, img)
	}
	return result
}

func (r *ComplianceReconciler) getAllImages(ctx context.Context) []string {
	var deployments appsv1.DeploymentList
	if err := r.List(ctx, &deployments); err != nil {
		return nil
	}
	images := map[string]bool{}
	for _, dep := range deployments.Items {
		for _, c := range dep.Spec.Template.Spec.Containers {
			images[c.Image] = true
		}
	}
	result := make([]string, 0, len(images))
	for img := range images {
		result = append(result, img)
	}
	return result
}

func (r *ComplianceReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&evergreenv1.EvergreenPolicy{}).
		WithOptions(controller.Options{MaxConcurrentReconciles: 2}).
		Complete(r)
}

var _ = types.NamespacedName{}
var _ = appsv1.SchemeGroupVersion
