# Example End-to-End Flow

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Each explorer/planner/executor is a
> native runtime invocation; ActionQ may federate its reference but does not
> execute it. Evidence uses content-addressed native/host references.

## Intent

Human:

```text
Investigate why appservice is degraded.
```

## 1. Bootstrap

Existing skill/session bootstrap:

- creates/binds Sprintctl task `OPS-142`;
- records intent;
- scope = `appservice`;
- role = explorer;
- operation budget = 12;
- capability = explorer;
- checkpoint triggers enabled.

Cheap explorer starts with `OPS-142`.

## 2. Exploration

Explorer performs bounded reads through the operator-approved native tools.

Events recorded:

```text
finding:
  appservice deployment 3/3 ready
  evidence=object:sha256:<digest-a>

finding:
  no recent rollout detected
  evidence=object:sha256:<digest-b>

finding:
  repeated upstream timeout in application logs
  evidence=trace:sha256:<digest-c>

proposed-action:
  inspect payments-api

scope-request:
  payments-api

checkpoint:
  SCOPE_EXPANSION
```

Explorer stops.

## 3. Planner invocation

Planner receives a deterministic projection of `OPS-142`.

Planner chooses to inspect:

```text
trace:sha256:<digest-c>
```

Planner finds the proposed direction reasonable and returns:

```text
CONTINUE

objective:
  determine whether payments-api health/errors correlate with appservice timeout window

scope add:
  payments-api

budget:
  8 observations
```

Planner decision is recorded into Sprintctl.

## 4. Continue or fresh session

Because intent remains the same and scope expansion is adjacent, continue the current cheap explorer.

If instead the planner had concluded:

```text
The problem is primarily a payments-api failure and appservice is only a symptom.
```

then record `REFRAME`, create a fresh task such as `OPS-143`, and start a fresh
cheap explorer. Sprintctl has no native parent/child item relation at the
inspected revision, so attach an ordinary reference from the fresh item to
`OPS-142` (for example, a labeled governing or evidence ref) and preserve the
relation in the reframe event rather than claiming native child semantics.
The fresh explorer receives:

- new task;
- confirmed material findings only;
- evidence handles;
- fresh scope;
- no old transcript.

## 5. Mutation request

Explorer later establishes a concrete remediation requiring mutation.

It records:

```text
proposed-action:
  restart deployment/payments-api

checkpoint:
  MUTATION_REQUIRED
```

Explorer stops.

## 6. Planner execution decision

Planner validates evidence and returns `STOP` with reason
`mutation requires a separately authorized operator/executor path`.

The operator may create a separate execution task after an independent
authorization decision. This proof does not create or dispatch it.

## 7. Executor

Spawn or start a fresh bounded executor session with separately constrained capability.

Executor:

- checks preconditions;
- performs authorized mutation;
- verifies rollout;
- records result/evidence;
- stops on unexpected scope expansion.

## 8. Close

Investigation task closes only after execution verification or explicit `STOP`.

No full transcript needs to become durable workflow state.
