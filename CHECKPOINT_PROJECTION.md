# Checkpoint Projection

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Evidence handles are
> implementation-neutral, content-addressed native/host references, optionally
> registered through a future ActionQ federation surface.

## Goal

Give the planner enough current state to reason well without forwarding the cheap agent's full transcript.

## Required projection

Keep this small:

```yaml
work_item: <id>
intent: "Investigate why appservice is degraded"

scope:
  - appservice

material_findings:
  - text: "Deployment is 3/3 ready"
    evidence: object:sha256:<digest>
  - text: "Logs contain repeated upstream timeout"
    evidence: trace:sha256:<digest>

proposed_next_action:
  text: "Inspect payments-api"

checkpoint:
  reason: SCOPE_EXPANSION

budget:
  operations_used: 7
  operations_limit: 12
```

This is a presentation contract, not necessarily a new serialized artifact.

## Projection rules

1. Derive from existing Sprintctl state/events.
2. Include only material findings.
3. Include content-addressed native/host evidence references where they help
   challenge a claim.
4. Do not include the exploratory transcript by default.
5. Do not summarize raw captures with another LLM just to make the packet.
6. The planner may retrieve raw evidence selectively.

## Raw evidence access

Planner access is native and reference-specific: use the producing runtime's
session/trace read surface or inspect a content-addressed host object. The
reference contract is `trace|object|file:sha256:<digest>`; it conveys identity,
not authority or cross-host availability. Verify the digest before use and do
not place raw output into Sprintctl.

## Failure signal

If planners repeatedly need to reconstruct almost the entire investigation by reopening most captures, the projection is too weak or the explorer findings are not reliable enough.

That is an experiment result, not a reason to immediately add more orchestration.
