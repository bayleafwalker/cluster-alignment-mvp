# Operator Escalation Capsule — Appservice Dogfood

No command in this capsule has been executed. Appservice dispatch,
orchestration, reconciliation, deployment, and live cluster reads or mutation
belong to the operator.

## Desired end state

Decide whether a cheap product-native explorer plus one stateless premium
planner preserves operational finding quality while materially reducing
premium context, using one real and non-urgent appservice issue.

## Preconditions for the operator

1. Select a concrete issue and Sprintctl sprint/track.
2. Select an explicitly read-only observation envelope excluding Secrets,
   exec/attach/cp/port-forward, arbitrary network probes, GitOps edits, and all
   mutating Kubernetes or Flux commands.
3. Select native runtimes/models for the cheap explorer and premium planner.
4. Choose a sanitized evidence-retention location and identify whether any
   material finding will be published to Auditctl.
5. Decide whether `payments-api` (or the actual adjacent subsystem) is a
   pre-reviewed adjacent scope. This directly changes `CONTINUE` versus
   `REFRAME`.

## Operator-run sequence

1. Run a premium-only read-only baseline and record the metrics defined in
   `ACCEPTANCE_TESTS.md`.
2. Render the deterministic bootstrap with `alignment_mvp.py bootstrap`, review
   it, then apply the rendered Sprintctl command through the operator's normal
   appservice workflow.
3. Invoke the cheap explorer in its product-native runtime with the boundary
   and `ROLE_CONTRACTS.md`. Capture bounded, sanitized evidence references.
4. Export `sprintctl item show --json`, transform the explorer result with
   `alignment_mvp.py project`, and invoke the premium planner in a fresh native
   session.
5. Validate the decision basis against a fresh item read before any Sprintctl
   state change. Rebuild and compare the projection digest as well, because an
   appended event does not change Sprintctl's status revision. If either basis
   changed materially, discard the decision and re-plan.
6. For `CONTINUE`, run another bounded read-only explorer turn. For `REFRAME`,
   create a fresh work item; Sprintctl currently has no native parent relation.
   For `STOP`, close or block through the operator's normal revision-aware path.
7. Treat `MUTATION_REQUIRED` as `STOP` in this MVP. Design and authorize any
   executor as a separate appservice action with separate credential/RBAC
   scope, verification, rollback, and expiry.
8. Run `alignment_mvp.py compare` on sanitized metrics and evaluate every
   falsifier rather than promoting on plumbing success.

## Decisions that genuinely change the result

- **Adjacent scope set:** a requested target inside it permits continued
  observation; outside it forces a fresh investigation. This determines how
  much context is retained and whether scope drift is contained.
- **Evidence retention:** host-local evidence makes this run inspectable only
  on the source host; Auditctl publication makes material findings
  durable-authoritative. Do not conflate the two.
- **Mutation inclusion:** excluding mutation completes the read-only MVP.
  Including it creates a new executor authorization tract and must not reuse
  explorer identity or Sprintctl reservation as authority.
