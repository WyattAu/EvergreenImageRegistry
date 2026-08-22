// =============================================================================
// Drift Detection Controller
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

type DriftReconciler struct {
	client.Client
	Scheme   *runtime.Scheme
	Recorder record.EventRecorder
	Registry RegistryClient
}

// +kubebuilder:rbac:groups=evergreenimageregistry.io,resources=evergrendrifts,verbs=get;list;watch;update;patch
// +kubebuilder:rbac:groups="",resources=pods,verbs=get;list;watch

func (r *DriftReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	var drift evergreenv1.EvergreenDrift
	if err := r.Get(ctx, req.NamespacedName, &drift); err != nil {
		if errors.IsNotFound(err) {
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	logger.Info("drift check", "namespace", drift.Namespace)

	var pods corev1.PodList
	if err := r.List(ctx, &pods, client.InNamespace(drift.Namespace)); err != nil {
		return ctrl.Result{}, err
	}

	driftCount := 0
	var alerts []string

	for _, pod := range pods.Items {
		for _, container := range pod.Spec.Containers {
			runningDigest := ""
			for _, status := range pod.Status.ContainerStatuses {
				if status.Name == container.Name {
					runningDigest = status.ImageID
					break
				}
			}
			if runningDigest == "" {
				continue
			}

			registryDigest, err := r.Registry.GetDigest(container.Image)
			if err != nil {
				continue
			}

			if runningDigest != registryDigest {
				driftCount++
				msg := fmt.Sprintf("drift: pod=%s img=%s", pod.Name, container.Image)
				alerts = append(alerts, msg)
				r.Recorder.Event(&drift, corev1.EventTypeWarning, "DriftDetected", msg)
			}
		}
	}

	drift.Status.LastCheck = &metav1.Time{Time: time.Now()}
	drift.Status.DriftDetected = driftCount
	drift.Status.Alerts = alerts

	if err := r.Status().Update(ctx, &drift); err != nil {
		return ctrl.Result{}, err
	}

	interval := time.Duration(drift.Spec.IntervalMinutes) * time.Minute
	if interval == 0 {
		interval = time.Hour
	}
	return ctrl.Result{RequeueAfter: interval}, nil
}

func (r *DriftReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&evergreenv1.EvergreenDrift{}).
		WithOptions(controller.Options{MaxConcurrentReconciles: 1}).
		Complete(r)
}

// Suppress unused import warnings
var _ = types.NamespacedName{}
var _ = appsv1.SchemeGroupVersion
