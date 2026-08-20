# Implementation Plan

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Inventory native runtime capture and
> ActionQ federation before proposing evidence plumbing. Do not implement an
> ActionQ/Vuoro runner, queue, lease, or Outctl dependency. Sprintctl
> reservations are advisory; any executor TTL belongs to its separate
> capability grant.

## Goal

Ship an MVP that allows a cheap exploratory agent to investigate a bounded cluster problem under non-mutating authority, checkpoint to a stronger planner, and resume or hand off execution without preserving the full exploratory transcript.

## Phase 0 — Capability inventory

Before changing code, inspect current capabilities in:

- Sprintctl task/work item creation
- Sprintctl events
- Sprintctl parent/child relationships or documented ordinary-ref fallback
- Sprintctl status/readiness fields
- Sprintctl status revisions and expected-revision mutation surfaces
- Sprintctl task/event projections or exports
- native runtime trace/session/output references
- standard trace/object storage and selective retrieval
- ActionQ federation reference registration and settlement
- current native-runtime session bootstrap
- current role/skill instruction distribution

Produce a short gap table:

| Need | Existing surface | Sufficient? | Proposed change |
|---|---|---:|---|
| Create bounded work item | ... | yes/no | ... |
| Record finding | ... | yes/no | ... |
| Record checkpoint | ... | yes/no | ... |
| Record planner decision | ... | yes/no | ... |
| Carry current revision and reject a stale planner decision | ... | yes/no | ... |
| Project task + recent events | ... | yes/no | ... |
| Reference native trace/object evidence | ... | yes/no | ... |
| Start a fresh native-runtime explorer | ... | yes/no | ... |
| Start a bounded native-runtime executor | ... | yes/no | ... |

### Hard gate

Do not add a new command, schema, service, or repository until this table identifies an actual missing capability.

---

## Phase 1 — Deterministic bootstrap

Implement the first scenario as a skill or existing session bootstrap.

Input:

```text
Investigate why appservice is degraded.
```

Bootstrap must establish, before the cheap agent begins:

- one bounded Sprintctl work item;
- intent;
- target scope;
- explorer role;
- non-mutating capability class;
- investigation budget;
- checkpoint conditions;
- existing work item ID/session binding if supported.
- current work-item status revision for subsequent decision-bearing writes.

Preferred semantics:

```text
task = investigation boundary
fresh task + ordinary relation ref = reframe or investigation branch
sprint = larger coordinated operational run only when already meaningful
```

Do **not** require the exploratory model to invent its own initial boundary.

---

## Phase 2 — Cheap explorer contract

The explorer receives:

```text
work item ID
intent
scope
allowed observation capabilities
budget
checkpoint conditions
event-recording rules
```

It may:

- inspect permitted resources;
- use approved observation commands with native or standard bounded capture;
- record material findings;
- propose next actions;
- request scope expansion;
- request alignment.

It may not mutate cluster state or gain new capability before planner alignment.

The explorer should not be required to produce formal hypotheses or attach evidence to trivia.

---

## Phase 3 — Checkpoint projection

A checkpoint is:

> a Sprintctl event + relinquishing control.

Do not create a new persistent "alignment packet" entity.

The planner input should be constructed from existing state:

```text
work item
+ current status revision
+ bounded recent events/findings
+ current scope
+ proposed next action
+ checkpoint reason
+ native trace/object evidence references
```

Prefer an existing Sprintctl projection/export.

Only if current output is materially unsuitable, add the smallest read-only projection helper, e.g. conceptually:

```text
sprintctl task show <id> --alignment
```

That helper must derive its output from existing authoritative data. It must not create new workflow state.

---

## Phase 4 — Planner contract

Planner is a stateless reasoning invocation.

Input:

- bounded task projection;
- evidence references;
- checkpoint reason.

Planner may inspect native/host trace or object evidence selectively.

The read-only proof planner returns exactly one operational decision:

```text
CONTINUE
REFRAME
STOP
```

The decision must also return the `basis_revision` from its input. Record its
durable state effect through Sprintctl's expected-revision CAS. If the basis
is stale, reject the write, reconstruct the projection from current state,
and obtain a new planner decision where the changed state could matter. Do not
silently rebase or retry the old decision. A decision event may describe the
attempt and basis, but it does not authorize a state transition whose CAS did
not succeed.

No planner daemon.
No planner queue.
No required planner conversation history.

`MUTATION_REQUIRED` returns `STOP` and an operator escalation capsule. The
broader architecture may still use a separately authorized `EXECUTE` phase,
but it is intentionally not a decision this proof can produce.

---

## Phase 5 — Continuation / fresh session

### CONTINUE

Continue current explorer if:

- intent remains the same;
- causal direction remains materially the same;
- scope expansion is small.

### REFRAME

Create or identify a fresh work item, relate it through an ordinary ref and
the reframe event, and start a fresh explorer if:

- intent materially changes;
- primary investigation direction is invalidated;
- work moves into another subsystem/domain;
- planner explicitly requests fresh context.

Fresh explorer receives only:

```text
new work item
confirmed material findings
planner decision
bounded scope
evidence references
```

Do not copy the previous transcript.

---

## Phase 6 — Execution

Mutation is a separate lifecycle and preferably a separate session.

Planner decision creates or authorizes a bounded execution work item.

The authorization/status mutation must use the work item's current revision
as `expected_revision`. A stale revision returns to alignment; it must not
start an executor. Creating a separate child execution item does not remove
the CAS requirement from any parent status or metadata update.

Executor receives:

- exact objective;
- allowed targets;
- allowed mutation class;
- preconditions;
- verification steps;
- rollback/stop conditions;
- TTL / one-shot identity if supported.

Explorer identity must not simply become executor identity.

Use existing policy/RBAC/OpenBao/cred-broker/dispatch surfaces where available.

---

## Phase 7 — Dogfood

Use one concrete appservice issue.

Sequence:

```text
premium-only baseline
cheap explorer → planner checkpoint → continuation/reframe/execution
```

Capture:

- number of cheap-agent operations;
- number of planner invocations;
- planner evidence retrieval count;
- premium-model tokens/context;
- total tokens/cost if available;
- material finding agreement;
- redirections by planner;
- unsafe or out-of-scope attempts;
- time/interaction overhead;
- whether a fresh session improved or degraded reasoning.

Do not infer success merely from plumbing working.

---

## Deferred by design

Do not implement in MVP:

- generic agent DAGs;
- generic cross-agent mailboxes;
- planner service;
- arbitrary escalation workflows;
- checkpoint DSL;
- automatic semantic checkpoint detection;
- autonomous privilege elevation;
- universal incident schema;
- workflow-specific database;
- new log/evidence store;
- formal hypothesis state machine;
- five privilege tiers;
- separate products for health check / maintenance / alerts / commissioning.
