variable "release_name" {
  description = "Helm release name"
  type        = string
  default     = "evergreen-images"
}

variable "chart_repository" {
  description = "Helm chart repository URL"
  type        = string
  default     = "https://wyattau.github.io/EvergreenImageRegistry"
}

variable "chart_name" {
  description = "Helm chart name"
  type        = string
  default     = "evergreen-registry"
}

variable "chart_version" {
  description = "Helm chart version"
  type        = string
  default     = "1.0.0"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "evergreen-system"
}

variable "registry" {
  description = "Container registry URL"
  type        = string
  default     = "ghcr.io/wyattau/evergreenimageregistry"
}

variable "image_config" {
  description = "Map of image configurations"
  type = map(object({
    repository = string
    tag        = string
  }))
  default = {}
}

variable "timeout" {
  description = "Helm release timeout in seconds"
  type        = number
  default     = 600
}
