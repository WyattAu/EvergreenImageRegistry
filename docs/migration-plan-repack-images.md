# Evergreen Image Registry: Repack Image Migration Plan
## Phase 1: Go Binary Extraction (Week 1-2): ~200 images
**Automated migration possible:** Yes; detect `go build` + `CGO_ENABLED=0` in builder, replace final stage with `scratch`.
## Phase 2: Static Binary Extraction (Week 2-3): ~50 images
**Automated migration possible:** Yes; detect `-static` flag or musl target in build commands.
## Phase 3: Language Runtime Migration (Week 3-5): 51 images
**Automated migration possible:** Partial; package name translation via `migrate_debian_to_wolfi.sh`
## Phase 4: Complex App Migration (Week 5-12): ~420 images
**Automated migration possible:** Partial; needs per-image analysis of file dependencies.