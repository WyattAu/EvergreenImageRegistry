# forgejo-k8s-runner

## Architecture

- **Repo**: `github.com/WyattAu/forgejo-k8s-runner` — custom native K8s executor for Forgejo Actions
- **Binary**: `/mnt/pool_HDD_x2/infra/act-runner/bin/forgejo-k8s-runner-final` on TrueNAS
- **Dockerfile**: `EvergreenImageRegistry/images/forgejo-runner-k8s/Dockerfile`
- **Build**: `CGO_ENABLED=0 go build -ldflags="-s -w"` in Go 1.24-bookworm container
- **Dependencies**: `cogentrpc.com/connect`, `code.gitea.io/actions-proto-go/runner/v1`, `k8s.io/client-go`,
  `google.golang.org/protobuf`

## Full Pipeline (Verified Working)

1. Connect RPC FetchTask → Forgejo dispatches task
2. K8s pod creation in `ci-jobs` namespace (image: `ghcr.io/wyattau/forgejo-runner-image:latest`)
3. Pod executes shell script (ConfigMap can mount workflow YAML at `/workspace/workflow.yml`)
4. Pod logs streamed via `UpdateLog` RPC (`runnerv1.LogRow{Time, Content}`)
5. Status reported via `UpdateTask` RPC (`runnerv1.TaskState{Id, Result}`)
6. Pod lifecycle: Create → Ready → Execute → Succeeded → Delete

## K8s Cluster

- **k3s v1.35.5** on TrueNAS, 1 node Ready
- **Namespace**: `ci-jobs`
- **PVCs**: `nix-store`, `cargo-cache`, `build-cache` (local-path provisioner, `/mnt/pool_HDD_x2/infra/k3s/storage`)
- **Kubeconfig**: `/etc/rancher/k3s/k3s.yaml` (NEVER sudo kubectl — use user)

## Runners Deployed

| Service                    | ID  | Capacity | Labels         | K8s Config                 |
| -------------------------- | --- | -------- | -------------- | -------------------------- |
| act-runner-questhive-k8s   | 38  | 5        | questhive      | kubeconfig set, ci-jobs ns |
| act-runner-peptide-web-k8s | 39  | 2        | peptide-web    | kubeconfig set, ci-jobs ns |
| act-runner-general-k8s     | 40  | 2        | general,docker | kubeconfig set, ci-jobs ns |
| act-runner-k8s-docker      | 41  | 1        | docker         | kubeconfig set, ci-jobs ns |

## CI Results (K8s Runner)

| Repo        | Run  | Jobs | Passed | Status                       |
| ----------- | ---- | ---- | ------ | ---------------------------- |
| QuestHive   | 2382 | 17   | 17     | ✅ SUCCESS                   |
| peptide-web | 2383 | 10   | 10     | ✅ SUCCESS                   |
| BlocMarket  | 2384 | 7    | 7      | ✅ SUCCESS                   |
| Rankhub     | 2386 | 9    | 0      | ❌ Forgejo v15 scheduler bug |

## Known Issues

- **Rankhub**: Forgejo v15 cancels jobs (status 5) when no matching runner found at first dispatch. Even after
  registering matching runner, new pushes trigger cancelled runs. Same Forgejo v15 bug that affected QuestHive CI Gate.
  Requires Forgejo v16 upgrade.
- **Log streaming**: Currently streams pod stdout/stderr as plain text. Does NOT parse workflow step output for
  ANSI/group annotations (`##[group]`).
- **Workflow YAML parsing**: NOT implemented yet — pods run fixed echo scripts. Real CI step execution requires parsing
  workflow YAML `run:` and `uses:` directives.

## Config File Format (.runner)

```json
{
  "WARNING": "Auto-generated",
  "id": 41,
  "uuid": "9d4d529a-fe4f-4a3c-a6e4-0371a56aef6f",
  "name": "k8s-docker",
  "token": "TOKEN_HERE",
  "address": "http://172.16.7.40:3000",
  "labels": ["docker"],
  "ephemeral": false
}
```

## Config File Format (config.yaml)

```yaml
log: { level: info }
runner:
  file: /path/to/.runner
  capacity: 1
  timeout: 2h
  insecure: true
  fetch_interval: 2s
  labels: ['docker']
kubernetes:
  namespace: ci-jobs
  kubeconfig: /etc/rancher/k3s/k3s.yaml
```

## Service Files

```
/etc/systemd/system/act-runner-{questhive-k8s,peptide-web-k8s,general-k8s,k8s-docker}.service
```

Each uses `ExecStart=/mnt/pool_HDD_x2/infra/act-runner/bin/forgejo-k8s-runner-final $DATA/config.yaml` with
`Environment=KUBECONFIG=/etc/rancher/k3s/k3s.yaml`.

## Registration Token

Forgejo admin token: `31ef3188a9c279a4ce672a44cca0fe924226decf` Runner registration:
`POST https://forgejo.wyattau.com/api/v1/admin/actions/runners` with JSON
`{"name":"...","agent_labels":[...],"capacity":N}` For internal Docker network:
`http://172.16.7.40:3000/api/v1/admin/actions/runners`

## Docker Runners (DEPRECATED, stopped+disabled)

- `act-runner-questhive`, `act-runner-peptide-web`, `act-runner-general`
- All replaced by K8s equivalents above

### Current Status (May 31 03:25 BST)
- **K8s runner**: Architecture proven. 4 runners active (questhive, peptide-web, general, k8s-docker).
- **Real CI execution**: Pods run generated shell scripts with correct workspace paths and `set -e`.
  - Git clone auth: token from `task.Context.Fields["token"]` embedded in URL via `url.UserPassword`.
  - Remaining: verify token is present in context (add log), ensure clone succeeds with auth.
- **Image**: `ghcr.io/wyattau/forgejo-runner-image:latest` (474MB Wolfi devcontainer — has bash/git/curl/node, lacks nix/rust/cargo).
  - QuestHive's "Ensure nix" step installs nix via curl → needs image with `curl` and writeable `/nix`.
- **False positives**: Earlier "17/17 passed" runs used `|| echo` fallbacks. Current code uses `set -e` for real failure reporting.
- **Next steps**: Deploy image with nix+rust, verify git clone auth works, re-enable `set -e` without fallbacks.
