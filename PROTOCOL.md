# Minimal Operational Protocol

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Native runtimes execute each phase;
> ActionQ may federate their external references, and Sprintctl reservations
> are advisory. Evidence uses bounded native/host trace or object references.

## Lifecycle

Only three conceptual phases matter:

```text
EXPLORE
  ↓
ALIGN
  ↓
EXPLORE | EXECUTE | DONE
```

Sprintctl does not need to gain these as new schema states unless existing status semantics genuinely require it.

## Initial checkpoint triggers

Implement only four:

1. `MUTATION_REQUIRED`
2. `SCOPE_EXPANSION`
3. `BUDGET_EXHAUSTED`
4. `EXPLORER_ESCALATION`

Avoid semantic triggers such as "hypothesis invalidated" in the first implementation. The explorer can escalate explicitly and the budget provides a deterministic backstop.

## Suggested default exploration budget

Use one simple configurable limit, preferably already expressible in current tooling/instructions.

Example starting point:

```text
max tool/cluster observation operations: 12
```

Optionally add a wall-clock bound if the current harness already supports it. Do not add a scheduler solely for this.

## Event vocabulary

Prefer existing Sprintctl event mechanisms.

The MVP needs to represent only:

```text
finding
scope-request
proposed-action
checkpoint
planner-decision
```

If Sprintctl already has generic event types, encode these as event metadata/content rather than adding five schema-level event classes.

Formal hypothesis events are optional and deferred.

## Revision and stale-decision rule

The bounded planner projection carries the current Sprintctl work-item status
revision as `basis_revision`. Reservations remain advisory; they are not the
concurrency control. Every authoritative state mutation produced by the
planner uses that revision through Sprintctl's expected-revision CAS.

If CAS reports a stale basis:

1. apply no planner-directed state transition;
2. reread current work state and revision;
3. rebuild the bounded projection; and
4. obtain a new planner decision when the intervening change could affect it.

Never attach the old decision to the new revision automatically. Append-only
observations may record the revision they observed, but a planner-decision
event is not mutation authority when its related CAS failed.

## Evidence references

Material findings may include a native runtime or standard trace/object
reference, optionally registered through ActionQ federation.

Example logical event:

```yaml
kind: finding
work_item: <id>
text: "Repeated upstream timeout in appservice logs"
evidence:
  - trace:sha256:<digest>
```

Evidence is not mandatory for every observation.

## Planner decisions in this proof

### CONTINUE

```yaml
decision: continue
basis_revision: item:<id>@status:<status>
objective: "Determine whether payments-api correlates with the timeout window"
scope_add:
  - payments-api
budget: 8
```

### REFRAME

```yaml
decision: reframe
basis_revision: item:<id>@status:<status>
new_intent: "Investigate payments-api upstream failures"
fresh_explorer: true
```

### STOP

```yaml
decision: stop
basis_revision: item:<id>@status:<status>
reason: "No actionable fault established"
```

`MUTATION_REQUIRED` also returns `STOP` with an operator escalation reason.
That keeps the read-only experiment executable without smuggling an executor
grant into planner output. A separately authorized future executor tract may
retain the broader architecture's `EXECUTE` concept.

These are logical examples, not a mandate for new persisted YAML/JSON objects.
Store the decision using existing Sprintctl primitives first, and reject the
state mutation when `basis_revision` no longer matches.
