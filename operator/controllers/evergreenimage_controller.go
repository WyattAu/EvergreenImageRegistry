// =============================================================================
// EvergreenImage Reconciler
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
	"k8s.io/client-go/tools/record"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller"
	"sigs.k8s.io/controller-runtime/pkg/log"
	"sigs.k8s.io/controller-runtime/pkg/predicate"

	evergreenv1 "github.com/WyattAu/EvergreenImageRegistry/operator/api/v1"
)

// EvergreenImageReconciler reconciles EvergreenImage objects
type EvergreenImageReconciler struct {
	client.Client
	Scheme   *runtime.Scheme
	Recorder record.EventRecorder
	Registry RegistryClient
	Policy   PolicyEngine
}

// +kubebuilder:rbac:groups=evergreenimageregistry.io,resources=evergreenimages,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=evergreenimageregistry.io,resources=evergreenimages/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;update;patch

func (r *EvergreenImageReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	var image evergreenv1.EvergreenImage
	if err := r.Get(ctx, req.NamespacedName, &image); err != nil {
		if errors.IsNotFound(err) {
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	logger.Info("reconciling", "image", image.Spec.Image, "tag", image.Spec.Tag)

	// Check registry
	latestTag, latestDigest, err := r.Registry.GetLatestTag(image.Spec.Image, image.Spec.Tag)
	if err != nil {
		r.Recorder.Event(&image, corev1.EventTypeWarning, "RegistryError", err.Error())
		return ctrl.Result{RequeueAfter: 5 * time.Minute}, err
	}

	if image.Status.CurrentDigest == latestDigest {
		return ctrl.Result{RequeueAfter: 15 * time.Minute}, nil
	}

	// Validate
	if r.Policy == nil {
		return ctrl.Result{RequeueAfter: 5 * time.Minute}, fmt.Errorf("policy engine is not configured")
	}
	{
		pass, violations, err := r.Policy.Validate(image.Spec.Image, latestTag)
		if err != nil {
			logger.Error(err, "policy validation failed")
			return ctrl.Result{RequeueAfter: 5 * time.Minute}, err
		}
		if !pass {
			msg := fmt.Sprintf("violations: %d", len(violations))
			r.Recorder.Event(&image, corev1.EventTypeWarning, "PolicyViolation", msg)
			return ctrl.Result{RequeueAfter: 30 * time.Minute}, nil
		}
	}

	// Update deployments if auto-update enabled
	if image.Spec.AutoUpdate {
		if err := r.updateDeployments(ctx, &image, image.Spec.Image, latestTag); err != nil {
			return ctrl.Result{}, err
		}
	}

	// Update status
	image.Status.CurrentTag = latestTag
	image.Status.CurrentDigest = latestDigest
	image.Status.LastUpdated = &metav1.Time{Time: time.Now()}
	image.Status.SBOMStatus = "unknown"
	image.Status.ComplianceStatus = "unknown"

	if err := r.Status().Update(ctx, &image); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{RequeueAfter: 15 * time.Minute}, nil
}

func (r *EvergreenImageReconciler) updateDeployments(ctx context.Context, image *evergreenv1.EvergreenImage, imgName, tag string) error {
	logger := log.FromContext(ctx)
	var deployments appsv1.DeploymentList
	if err := r.List(ctx, &deployments, client.InNamespace(image.Namespace)); err != nil {
		return err
	}
	for i := range deployments.Items {
		dep := &deployments.Items[i]
		for j, c := range dep.Spec.Template.Spec.Containers {
			if c.Image == imgName+":"+image.Status.CurrentTag || c.Image == imgName+":"+tag {
				dep.Spec.Template.Spec.Containers[j].Image = imgName + ":" + tag
				if err := r.Update(ctx, dep); err != nil {
					logger.Error(err, "update failed", "name", dep.Name)
					return err
				}
			}
		}
	}
	return nil
}

func (r *EvergreenImageReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&evergreenv1.EvergreenImage{}).
		WithOptions(controller.Options{MaxConcurrentReconciles: 3}).
		WithEventFilter(predicate.GenerationChangedPredicate{}).
		Complete(r)
}
