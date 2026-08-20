# Role Contracts

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). These are native-runtime roles, not
> ActionQ/Vuoro runner roles. Evidence references are implementation-neutral,
> and a Sprintctl reservation never grants the explorer or executor authority.

## Explorer

### Purpose

Perform bounded observational work cheaply.

### Input

- Sprintctl work item ID
- intent
- current scope
- observation capability envelope
- investigation budget
- checkpoint triggers

### Allowed behavior

- inspect resources inside scope;
- inspect logs/events/status through approved tooling;
- use bounded native/host capture and content-addressed retrieval;
- record material findings;
- request scope expansion;
- propose a next action;
- request planner alignment.

### Forbidden behavior before planner alignment

- mutate cluster state;
- exec/attach into workloads;
- port-forward;
- read secrets unless explicitly included in the envelope;
- reconcile Flux;
- change GitOps state;
- use arbitrary privileged network reach;
- broaden scope silently.

### Recording discipline

Record material state transitions/findings, not a transcript.

Good:

```text
finding: appservice replicas 3/3 ready; evidence object:sha256:<digest>
finding: repeated upstream timeout; evidence trace:sha256:<digest>
scope-request: inspect payments-api
checkpoint: SCOPE_EXPANSION
```

Bad:

```text
finding: ran kubectl
finding: output had 42 lines
finding: now thinking
finding: maybe inspect something else
```

### Stop rule

When a checkpoint condition is met, record it and relinquish control.

---

## Planner

### Purpose

Realign the investigation with stronger reasoning.

### Input

- bounded Sprintctl projection;
- checkpoint reason;
- material findings;
- proposed next action;
- content-addressed native/host evidence references.

### Behavior

- challenge the explorer's causal direction;
- inspect raw native/host evidence only when useful;
- decide whether work should continue, reframe, or stop;
- define a bounded next objective.

### Output

Exactly one:

```text
CONTINUE
REFRAME
STOP
```

Optional explanatory prose may accompany the decision, but the operational decision must be unambiguous.

Planner does not own durable workflow state.

For this executable MVP, `MUTATION_REQUIRED` produces `STOP` and an operator
escalation. A later, separately authorized executor tract may interpret that
escalation; the stateless planner never grants mutation authority.

---

## Executor

### Purpose

Perform a bounded mutation after planner alignment.

### Input

- execution work item;
- exact objective;
- allowed mutations;
- allowed targets;
- preconditions;
- verification;
- rollback/stop conditions;
- bounded identity/capability.

### Behavior

- execute only the authorized action boundary;
- verify result;
- record material execution evidence/events;
- stop and re-escalate if execution requires investigation beyond the package.

### Rule

Executor is not an explorer with upgraded privileges. Prefer a fresh session and separately bounded identity.
