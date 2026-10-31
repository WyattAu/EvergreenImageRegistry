1. **Docker Hub credentials expired**; refresh `DOCKERHUB_TOKEN` in GitHub secrets
2. **9/50 images fail to build**; old restored images with broken upstreams
3. **Docker Hub mirror references reverted**; GHCR nested packages can't be set public
4. **~50 images have no runtime smoke test**; built but not verified at runtime