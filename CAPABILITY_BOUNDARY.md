# Explorer / Executor Capability Boundary

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Native runtimes execute directly;
> Evidence commands below refer to native/host content-addressed inspection.
> A bounded executor grant is distinct from a
> credential-free advisory Sprintctl reservation.

## Principle

"Read-only Kubernetes RBAC" is not a sufficient definition of safe exploration.

The MVP uses two operational capability classes.

## Explorer capability

Explorer must be:

- non-mutating;
- non-interactive;
- scoped;
- unable to obtain arbitrary privileged network reach.

Typical allowed operations:

```text
resource get/list/watch
describe/status
logs
events
Flux status/read operations
approved controller status APIs
native runtime session/trace reads
content-addressed host object inspect/verify
```

Subject to namespace/resource scope.

### Explicitly exclude by default

```text
Secrets or raw credential values
pods/exec
attach
cp
port-forward
arbitrary privileged curl/network probes
database shells
create
patch
apply
edit
delete
scale
rollout restart
cordon/drain
Flux reconcile
Helm upgrade
Git/GitOps changes that will reconcile into the cluster
```

If an ostensibly observational operation exposes high-risk data or interactive capability, it does not belong in the default explorer envelope.

## Executor capability

Executor is granted only the mutation surface required by the approved execution package.

Desired properties where existing tooling supports them:

- target/resource scoped;
- operation scoped;
- short-lived;
- one-shot or bounded-use;
- separately attributable;
- independently reviewable.

Use existing policy/RBAC/OpenBao/cred-broker mechanisms. Do not build an elevation subsystem for this MVP.

## Human supervision

The MVP assumes supervised operation.

Human review may remain the final gate for mutations while policy/runtime enforcement is being hardened.

Do not treat "planner approved" as equivalent to "capability granted".
