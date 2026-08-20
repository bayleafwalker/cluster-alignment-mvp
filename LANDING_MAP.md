# Proposed Landing Map

The package is not a Git repository and no existing repository unambiguously
owns this experiment. The current output therefore remains **host-persistent**,
not cross-host-replicated or durable-authoritative.

Recommended landing after operator ownership selection:

| Artifact | Proposed authority | Rationale |
|---|---|---|
| `alignment_mvp.py`, fixtures, and tests | New incubating experiment repository, or an explicitly approved Agentops experiment subtree | Runtime-neutral proof code is not Sprintctl product behavior and must not make Agentops a runtime owner by accident. |
| Reusable role/bootstrap instructions after dogfood | Agentops dispatch templates | Agentops owns shared skills and role distribution. |
| A proven generic alignment projection convenience | Sprintctl, only after repeated dogfood friction | Sprintctl owns work reads and revisions; current proof does not justify a product command yet. |
| Future external execution/evidence registration adapter | ActionQ federation implementation | ActionQ owns federation, acceptance, and reconciliation, not native runtime execution. |
| Appservice runtime/RBAC/runbook changes | Appservice, operator-owned tract | Deployment and live cluster operations remain out of scope here. |
| Material empirical findings | Auditctl | Durable-authoritative observation channel. |

Do not land the proof into ActionQ runner packages, recreate Outctl, or add a
Vuoro execution service.
