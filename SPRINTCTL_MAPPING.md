# Sprintctl Mapping — Reuse First

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Sprintctl stores advisory coordination,
> not exclusive execution ownership. Bounded native/host evidence references
> may be registered through the ActionQ federation layer.

## Design principle

Sprintctl is the coordination surface. Do not create a parallel "alignment state" store.

The primary object is:

> **a bounded operational work item with reconstructable evidence**

The planner packet is a temporary projection of that work, not another authoritative artifact.

## Preferred mapping

| Concept | Sprintctl representation |
|---|---|
| Operational intent | Existing task/work-item description/metadata |
| Investigation boundary | Task/work item |
| Larger coordinated run | Sprint, only when genuinely useful |
| Investigation branch | Fresh task/work item plus ordinary relation ref and reframe event (no native parent/child item surface at the inspected revision) |
| Material observation | Existing event |
| Scope expansion request | Existing event |
| Proposed next action | Existing event |
| Checkpoint | Existing event + agent stops |
| Planner decision | Existing event / task update |
| Execution | Separate task/work item when mutation is approved |
| Raw evidence | Native runtime or standard trace/object reference linked from an event; optionally registered through ActionQ federation |
| Decision basis | Current work-item status revision carried in the planner projection |

## Bootstrap behavior

The deterministic bootstrap should create/bind the initial task before the cheap agent begins.

Conceptual sequence:

```bash
# Pseudocode only — map to current Sprintctl commands.
sprintctl task create \
  --intent "Investigate why appservice is degraded" \
  --scope appservice \
  --role explorer
```

Do not implement this literal command if equivalent current commands exist.

## Planner projection

First attempt to compose planner context using existing read commands.

Required information:

```text
work item ID
current status revision
intent
scope
recent material events
proposed next action
checkpoint reason
native trace/object evidence references
```

If this takes multiple existing reads, that is acceptable for the first dogfood.

Only add a projection convenience command if repeated use demonstrates real friction.

## Revision discipline

Reservations remain advisory and grant no write authority. Every planner
projection must carry the work item's current status revision. Every
authoritative item/status/metadata mutation derived from that projection must
submit the same value through Sprintctl's expected-revision compare-and-swap
surface.

Conceptually:

```bash
revision=$(sprintctl item show --id <id> --json | jq -r '.item.status_revision')
# planner input includes basis_revision=$revision
sprintctl item status \
  --id <id> \
  --status <next-status> \
  --actor <actor> \
  --expected-revision "$revision"
```

If the revision is stale, reject the write, reread the item, rebuild the
bounded projection, and obtain a new decision where necessary. Never retry a
stale planner decision against the new revision automatically. Append-only
finding/checkpoint events may retain their observed basis revision, but a
planner-decision event is not authority for a state change unless the related
CAS succeeds. If an intended state mutation has no revision-aware existing
surface, record that as a Phase 0 capability gap rather than writing blind.

## Git boundary

Use Git for durable authored artifacts, not routine operational state.

Appropriate Git outputs:

- remediation plan;
- ADR;
- maintenance procedure;
- incident analysis worth preserving;
- configuration/code/manifests;
- reusable troubleshooting documentation.

Do not produce a Markdown investigation report for every short cluster check.
