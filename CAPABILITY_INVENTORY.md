# Capability Inventory — 2026-08-20

This inventory is pinned to the local source revisions below. It is a read-only
source inspection, not a live service or cluster observation.

| Repository | Inspected revision |
|---|---|
| Sprintctl | `75fd4a7bc01472f941c923444cabe6451bb1afd0` |
| Agentops | `6b41e6f7b14d7cb9b6e44acced4f05f457b810eb` |
| ActionQ | `8d42934799bdb5706e188ac006a16c0ce8f2514f` |
| Vuoro | `9dc7efa8d3f546851218f49da7653f806d5e8ca4` |
| cred-broker | `a8ad3e02cf27f25e54183ae752e5c01880faaa38` |

| Need | Existing surface | Sufficient? | Proof-package response |
|---|---|---:|---|
| Create bounded work item | `sprintctl item add` with title and description | Yes | `bootstrap` renders deterministic argv and a content-addressed boundary; it never executes it. |
| Record finding/checkpoint/decision | Generic `sprintctl event add --payload` | Yes | Use the five logical event kinds inside payload; add no schema type. |
| Read current work and events | `sprintctl item show --json` returns item, events, claims/reservations context, refs, and dependencies | Yes | Sanitized fixture freezes the consumed shape. |
| Carry current revision | `item.show.item.status_revision` | Partial | Projection requires both `status_revision` and identical `basis_revision`, plus an observational projection digest. The status token does not advance for append-only events. |
| Reject stale status decision | Direct `item status --expected-revision`; served lifecycle carries an immutable basis | Yes for status, not event append | Proof rejects a changed status and supplies a projection digest for coordinator-side evidence comparison. Applying a decision remains owner-side Sprintctl work. |
| Bounded planner projection | Existing output is complete but not alignment-bounded | Partial | Dependency-free read-only projector caps events, findings, evidence references, and encoded size. No new workflow entity. |
| Content-addressed evidence | Native/host trace and object handles are architectural surfaces; Auditctl owns durable material findings | Partial | Contract accepts only `trace|object|file:sha256:<digest>` handles. Raw content stays outside Sprintctl. |
| ActionQ federation registration | Target contract documented; no current federation API was found | No, deferred | Optional future adapter only. The MVP neither imports nor calls ActionQ. |
| Start native explorer/planner | Product runtimes already execute directly | Yes | Role input/output contracts are runtime-neutral JSON; no runner or daemon. |
| Parent/child reframe relation | No current Sprintctl item parent/child surface was found | No | `REFRAME` proposes a fresh item and reports `parent_relation_supported=false`; do not fake the relation. A normal ref may be added by an operator if useful. |
| Bounded executor credential | cred-broker models issuance and receipts; production OpenBao/provider commissioning remains gated | Not required here | `MUTATION_REQUIRED` returns `STOP`. Executor capability and appservice work are operator escalation. |

## Hard-gate conclusion

The only helper justified by the inventory is a read-only bounded projection
and contract validator. No Sprintctl schema, command, service, evidence store,
ActionQ execution path, Outctl dependency, or privilege-elevation mechanism is
added.
