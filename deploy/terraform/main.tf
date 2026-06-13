terraform {
  required_version = ">= 1.0"
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
}

resource "helm_release" "evergreen_images" {
  name       = var.release_name
  repository = var.chart_repository
  chart      = var.chart_name
  version    = var.chart_version
  namespace  = var.namespace

  dynamic "set" {
    for_each = var.image_config
    content {
      name  = "images.${set.key}.repository"
      value = set.value.repository
    }
  }

  dynamic "set" {
    for_each = var.image_config
    content {
      name  = "images.${set.key}.tag"
      value = set.value.tag
    }
  }

  set {
    name  = "global.registry"
    value = var.registry
  }

  timeout         = var.timeout
  cleanup_on_fail = true
  atomic          = true
}
