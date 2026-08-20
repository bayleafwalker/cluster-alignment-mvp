# Implementer Checklist

> Apply [`ALIGNMENT.md`](ALIGNMENT.md). References to Outctl inspection mean
> the equivalent bounded native/host evidence surface. Confirm ActionQ is used
> only for federation and Sprintctl only for advisory coordination.

## Before code changes

- [x] Inspect current Sprintctl task/work/event surfaces.
- [x] Inspect parent/child work support (none found; do not fake it).
- [x] Inspect existing task projection/export commands.
- [x] Inspect native/host capture and retrieval surfaces.
- [x] Inspect current skill/session bootstrap mechanisms.
- [x] Inspect native runtime support for fresh explorer/planner sessions.
- [x] Document the read-only capability boundary; live RBAC verification is operator work.
- [x] Produce the capability-gap table in `CAPABILITY_INVENTORY.md`.
- [x] Confirm the only justified helper is read-only and adds no service/schema.

## MVP implementation

- [x] Add a deterministic `investigate issue` bootstrap renderer.
- [x] Render work-item creation/binding before explorer input; execution is operator-owned.
- [x] Define and validate explorer output using `ROLE_CONTRACTS.md`.
- [x] Bound explorer capability according to `CAPABILITY_BOUNDARY.md`.
- [x] Implement only four checkpoint triggers.
- [x] Validate material findings and content-addressed evidence references.
- [x] Build planner input from a sanitized Sprintctl item-show fixture.
- [x] Avoid creating a persistent alignment-packet entity.
- [x] Define planner return contract: `CONTINUE | REFRAME | STOP`.
- [x] Report absent parent/child semantics rather than inventing them.
- [x] Keep every role a fresh product-native invocation with no dispatch daemon.
- [x] Keep executor mutation authority outside this proof.
- [x] Add no privilege elevation.

## Dogfood

- [ ] Choose one real appservice investigation.
- [ ] Run premium-only baseline.
- [ ] Run cheap-explorer + planner flow.
- [ ] Verify native/host evidence retrieval is actually used when needed.
- [ ] Measure planner invocation and premium-context savings.
- [ ] Compare material findings and redirections.
- [ ] Record failures without immediately expanding architecture.

## Completion gate

MVP is complete when the workflow can be exercised end-to-end using mostly existing tooling and there is enough evidence to decide whether the split-model operating pattern is worth continuing.

MVP is **not** complete merely because all orchestration plumbing exists.
