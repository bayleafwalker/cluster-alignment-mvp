# Cluster Alignment MVP — Implementer Package

> **Future-state mapping (2026-08-20):** Read [`ALIGNMENT.md`](ALIGNMENT.md)
> before using this package. Native products execute; ActionQ only federates
> external execution/evidence references; Sprintctl reservations are advisory;
> and evidence uses content-addressed native/host handles without Outctl. The
> experiment's checkpoints, measurements, and falsifying gates are unchanged.

## Purpose

Implement the smallest viable orchestration pattern for supervised cluster operations:

```text
human intent
    ↓
deterministic bootstrap
    ↓
bounded Sprintctl work item + explorer envelope
    ↓
cheap native-runtime explorer
    ├─ Sprintctl findings/events
    └─ bounded trace/object evidence references
    ↓
checkpoint
    ↓
premium native-runtime planner
    ├─ CONTINUE
    ├─ REFRAME
    └─ STOP (including mutation escalation)
```

The MVP exists to test one proposition:

> Can a cheap model perform most non-mutating cluster investigation while a stronger model is invoked only at bounded alignment checkpoints, without materially degrading operational quality?

This is **not** a generic multi-agent orchestration framework.

## Architectural constraints

1. Reuse existing tooling before adding anything.
2. No new persistent service.
3. No new executable by default.
4. No generic workflow engine.
5. No new evidence store.
6. No autonomous privilege elevation.
7. No custom planner state.
8. No new Sprintctl schema unless the current model demonstrably cannot express the MVP.
9. Git remains the durable home for authored operational artifacts and actual configuration/code changes.
10. Native runtime/host trace and object surfaces supply retrievable evidence;
    Sprintctl must not become a log store.

## Existing tools and intended responsibilities

| Tool | Responsibility |
|---|---|
| Git | Durable authored docs, plans, ADRs, procedures, configuration/code changes |
| Sprintctl | Intent, bounded work item, current revision, status, advisory reservation, events, ordinary cross-item refs, checkpoint and planner decision |
| Native runtimes | Execute explorer, planner, and executor turns; expose their native trace/session/output references |
| Standard trace/object storage | Retain bounded or host-local output and selectively retrieve it without introducing a new evidence product |
| Auditctl | Retain durable material findings and their evidence references |
| Existing policy/RBAC | Bound explorer and executor capabilities |
| OpenBao / cred-broker | Optional bounded identity/credential issuance for executor work |
| ActionQ federation | Register external native-runtime execution/evidence references and reconcile or settle outcomes; never spawn or supervise a session |
| Skills / AGENTS instructions | Deterministic bootstrap and role contracts |

## MVP scenario

Implement only:

> **Investigate a concrete cluster issue, escalate at a checkpoint, then continue, reframe, or stop.**

Do not implement health-check, maintenance, commissioning, alert triage, or incident frameworks separately. They should become bootstrap variants later if the core flow works.

## Required implementation order

1. Inventory Sprintctl revision-aware writes, native runtime evidence, standard
   trace/object retrieval, and ActionQ federation capabilities.
2. Prove the current tools can represent the workflow with existing commands.
3. Implement the bootstrap and role instructions using existing surfaces.
4. Add only the smallest missing ergonomic helper if a concrete gap remains.
5. Dogfood against one real appservice investigation.
6. Compare against premium-model-only operation.

## Executable proof

`alignment_mvp.py` is a dependency-free, read-only reference implementation.
It renders but never applies a deterministic bootstrap, validates cheap
explorer output, projects bounded Sprintctl-shaped state, makes a stateless
`CONTINUE | REFRAME | STOP` decision, and compares sanitized split and
premium-only runs. See `EVIDENCE.md` for reproduction and
`OPERATOR_ESCALATION.md` for the deliberately unexecuted appservice dogfood.

See `IMPLEMENTATION_PLAN.md` and `CAPABILITY_INVENTORY.md`.
