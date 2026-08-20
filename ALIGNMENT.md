# Future-State Alignment

This host-local implementer package has not landed in a Git authority. The
experiment remains useful, but its execution/evidence terminology is aligned
to the canonical Vuoro plan at
`../vuoro/docs/plans/2026-08-20-execution-federation-alignment.md`.

## Binding interpretation

- A product-native runtime performs each explorer, planner, or executor turn.
  The package does not require a Vuoro runner, an ActionQ daemon, or a common
  harness adapter.
- ActionQ may federate an external runtime reference, provider handle,
  assurance level, bounded evidence reference, and reconciled outcome. It
  does not claim, lease, queue, spawn, or supervise the native runtime.
- Sprintctl records work, material findings, checkpoints, decisions, and an
  advisory reservation. Reservations may overlap and must surface the
  conflict; they are not exclusive claims, capabilities, leases, or mutation
  proof.
- References to an `outctl` capture in the preserved package mean a bounded,
  selectively retrievable native-runtime or host-local evidence reference.
  Outctl is not a dependency. Raw output may stay host-local; material durable
  findings belong in Auditctl and authored changes in Git.
- A short-lived RBAC or credential grant may still bound executor mutation.
  Its expiry is a capability boundary and is not a Sprintctl reservation TTL.

This mapping changes no checkpoint, planner decision, capability boundary,
measurement, or falsifier. It prevents the experiment from rebuilding the
execution plane that the current architecture deletes.

## Unchanged falsification gates

The exact gates in `ACCEPTANCE_TESTS.md` remain:

1. planner intervention is required so frequently that the cost/context benefit disappears;
2. planner must reopen most raw captures to reconstruct the situation;
3. cheap explorers frequently form harmful investigation direction before checkpoints despite non-mutating scope;
4. recording events materially degrades agent execution;
5. premium-only operation materially outperforms the split model on important findings or operational correctness;
6. outctl evidence references are rarely useful to planners;
7. fresh-session reframing loses critical context often enough that transcript continuity is actually superior;
8. capability bounding requires so much custom machinery that the orchestration savings disappear.

Gate 6 keeps the original name as a stable measurement label. During an
aligned run it tests whether selectively retrievable native/federated evidence
references are useful; it does not require the Outctl implementation.

## Still requires operator authorization

This package authorizes no cluster read, mutation, deployment, or sprint-state
change. A dogfood target and capability envelope must be selected separately,
and every mutation remains a separately authorized executor action.
