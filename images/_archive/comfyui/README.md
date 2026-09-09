# comfyui (ARCHIVED)

Archived 2026-09-09.

Reason: upstream image `yanirs/comfyui:v0.20.1` is no longer pullable - the Docker Hub
repository returns 404 via the Hub API and the registry endpoint
returns 401 (repository went private or was removed in the Docker Hub
org lockdowns). No successor home found on ghcr.io or quay.io for the
same org/name.

Not deployed anywhere in the SimpleInfrastructureStack.

To revive: locate a maintained upstream (same org often republishes
under a new name or registry), rewrite the FROM, un-archive the
directory.
