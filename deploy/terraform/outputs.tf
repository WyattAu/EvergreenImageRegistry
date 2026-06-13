output "release_name" {
  description = "Helm release name"
  value       = helm_release.evergreen_images.name
}

output "release_status" {
  description = "Helm release status"
  value       = helm_release.evergreen_images.status
}

output "chart_version" {
  description = "Deployed chart version"
  value       = helm_release.evergreen_images.version
}

output "namespace" {
  description = "Deployed namespace"
  value       = helm_release.evergreen_images.namespace
}
