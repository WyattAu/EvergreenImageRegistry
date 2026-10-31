- `validate_parallel.rs`; 20-constraint engine (C001-C020), no repack exemptions
- `policy.rs`; OPA/Rego policy-as-code engine (13 built-in policies + 3 compliance bundles)
1. **K8s Operator**; Auto-update + drift detection + compliance enforcement + admission webhook
2. **SBOM Dependency Graph**; Cross-image package tracking + transitive CVE propagation
3. **Performance Regression Gate**; Build time baselines with threshold blocking
4. **Policy-as-Code Marketplace**; PCI DSS / HIPAA / FedRAMP Rego bundles + test framework
5. **Runtime Policy Generator**; SBOM → Seccomp/AppArmor/NetworkPolicy/PSS
6. **SBOM Diffing**; Version delta tracking with Prometheus metrics
7. **Automated CIS/STIG + SCAP/XCCDF**; No other registry has this
8. **Multi-Scanner Consensus**; Trivy + Grype for reduced false positives
9. **Multi-Cloud Auth**; AWS IRSA / GCP Workload Identity / Azure Workload Identity
10. **Edge Computing**; ARM32/ARM64 variants + minimal images + offline SBOMs
- Digest pinning: 126/778 (16%); critical tier partially complete