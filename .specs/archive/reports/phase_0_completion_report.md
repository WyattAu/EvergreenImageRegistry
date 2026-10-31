- `.specs/08_roadmap/master_plan.toml`; Topologically-sorted execution plan with 47 tasks across 7 phases
- `.specs/08_roadmap/phase_0_plan.md`; Detailed Phase 0 execution specification (7 sections)
- `.adrs/ADR-001-healthcheck-strategy.md`; HEALTHCHECK fix strategy (ACCEPTED)
- `.adrs/ADR-002-checksum-verification.md`; SHA256 verification strategy (ACCEPTED)
- `.adrs/ADR-003-debian-multistage.md`; Multi-stage conversion strategy (ACCEPTED)
**Changes:** | Fix | Description | |-----|-------------| | Typo fix | `/temp/*.tar` → `/tmp/*.tar` (eliminated -
- [ ] Multi-stage conversion complete (partial; database images deferred)
2. **Focus Phase 1** on checksum verification; this is the highest-risk remaining item
3. **Consider a Dockerfile generator**; with 223 images, manual maintenance is unsustainable. A TOML-to-Dockerfile
4. **Prioritize database image conversion**; these 87 images are the weakest security posture