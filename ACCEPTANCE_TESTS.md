# MVP Acceptance and Falsification

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). Selective evidence means bounded
> content-addressed native/host evidence; Outctl is not a dependency.

## Functional acceptance

### Bootstrap

- initial Sprintctl work item exists before cheap explorer begins;
- intent and scope are clear;
- explorer capability is non-mutating and non-interactive;
- budget/checkpoint rules are present.

### Exploration

- cheap explorer can perform useful bounded investigation;
- material findings are represented in Sprintctl;
- raw evidence remains in its native runtime or content-addressed host object;
- Sprintctl does not contain copied bulk logs;
- explorer stops at deterministic checkpoint.

### Planner

- planner receives a bounded projection without full transcript;
- planner can selectively retrieve referenced native/host evidence;
- planner returns an unambiguous `CONTINUE`, `REFRAME`, or `STOP`;
- decision is durably reflected using existing Sprintctl state/events.

### Reframe

- materially changed investigation can start in a fresh session;
- new explorer does not require prior full transcript;
- confirmed findings/evidence references are sufficient to continue.

### Execute

- mutation is not performed with explorer capability;
- execution is separately bounded;
- executor verifies outcome;
- unexpected investigation/scope expansion returns to alignment.

---

## Value-proposition measurements

Compare against a premium-model-only cluster investigation.

Capture at minimum:

```text
cheap-agent cluster/tool operations
planner invocation count
planner evidence retrieval count
premium-model input/context consumption
total token/cost if available
material finding agreement (ID, severity, and bounded normalized narrative)
critical/high disagreement
planner redirections
unsafe/out-of-scope attempts
operator intervention count
wall-clock / interaction overhead
```

## Strong positive result

A useful target shape is:

```text
cheap explorer performs most observational work
        ↓
small deterministic checkpoint
        ↓
planner consumes bounded current state
        ↓
planner selectively checks raw evidence
        ↓
planner redirects/approves
        ↓
cheap exploration or bounded executor continues
```

with comparable operational quality and materially lower premium-model context usage.

## Falsification / redesign signals

The design loses support if:

1. planner intervention is required so frequently that the cost/context benefit disappears;
2. planner must reopen most raw captures to reconstruct the situation;
3. cheap explorers frequently form harmful investigation direction before checkpoints despite non-mutating scope;
4. recording events materially degrades agent execution;
5. premium-only operation materially outperforms the split model on important findings or operational correctness;
6. selectively retrievable evidence references are rarely useful to planners;
7. fresh-session reframing loses critical context often enough that transcript continuity is actually superior;
8. capability bounding requires so much custom machinery that the orchestration savings disappear.

Do not convert a failed experiment into a larger framework by default.
