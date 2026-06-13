# EvergreenImageRegistry - Terraform Module

Deploys EvergreenImageRegistry images to Kubernetes via Helm.

## Quick Start

```hcl
module "evergreen" {
  source = "./deploy/terraform"

  release_name  = "evergreen-images"
  namespace     = "evergreen-system"
  chart_version = "1.0.0"

  image_config = {
    postgres = {
      repository = "ghcr.io/wyattau/evergreenimageregistry/postgres"
      tag        = "16.2.0"
    }
    redis = {
      repository = "ghcr.io/wyattau/evergreenimageregistry/redis"
      tag        = "7.2.4"
    }
    traefik = {
      repository = "ghcr.io/wyattau/evergreenimageregistry/traefik"
      tag        = "3.0.0"
    }
  }
}
```

## Outputs

| Output | Description |
|--------|-------------|
| `release_name` | Helm release name |
| `release_status` | Helm release status |
| `chart_version` | Deployed chart version |
| `namespace` | Deployed namespace |

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `release_name` | `evergreen-images` | Helm release name |
| `chart_repository` | `https://wyattau.github.io/EvergreenImageRegistry` | Helm chart repo URL |
| `chart_name` | `evergreen-registry` | Helm chart name |
| `chart_version` | `1.0.0` | Helm chart version |
| `namespace` | `evergreen-system` | Kubernetes namespace |
| `registry` | `ghcr.io/wyattau/evergreenimageregistry` | Container registry URL |
| `image_config` | `{}` | Map of image configurations |
| `timeout` | `600` | Helm release timeout (seconds) |

## Usage

```bash
terraform init
terraform plan -var="image_config={postgres={repository=\"ghcr.io/wyattau/evergreenimageregistry/postgres\",tag=\"16.2.0\"}}"
terraform apply
```
