# Local Proof Evidence

Classification: **host-persistent** source package under
`/projects/dev/cluster-alignment-mvp`. It is not cross-host-replicated or a
durable-authoritative record because the directory has no Git authority.

## Reproduction

From this directory:

```bash
python -m unittest discover -s tests -v
python alignment_mvp.py bootstrap \
  --intent "Investigate why appservice is degraded" \
  --sprint-id appservice#99 --scope appservice
python alignment_mvp.py validate-explorer fixtures/explorer-output.sanitized.json
python alignment_mvp.py project \
  fixtures/sprintctl-item-show.sanitized.json \
  fixtures/explorer-output.sanitized.json
python alignment_mvp.py plan \
  fixtures/checkpoint-projection.expected.json \
  fixtures/planner-policy.sanitized.json
python alignment_mvp.py compare \
  fixtures/split-run.sanitized.json \
  fixtures/premium-only-run.sanitized.json
python scripts/verify_manifest.py
```

## Current result

- 12 dependency-free unit tests pass, including falsifiers for a severity
  downgrade and a materially divergent narrative under the same finding ID.
- Bootstrap output is byte-for-byte deterministic and has
  `authority_mutated=false`.
- Explorer output is capped at 50 observations, 8 findings, and 2 evidence
  references per finding; budget exhaustion has one mandatory checkpoint.
- Projection rejects a stale explorer basis, includes identical
  `status_revision` and `basis_revision`, includes no transcript, and is capped
  at 16 KiB. It also carries an observational `projection_digest`; this detects
  a changed rebuilt packet but is not an authority token.
- Planner emits only `CONTINUE`, `REFRAME`, or `STOP`, carries its basis, and
  mutates no authority. A mutation checkpoint always stops for operator action.
- The sanitized comparison fixture has 100% material agreement across finding
  ID, severity, and bounded normalized narrative; no critical/high
  disagreement; and 72% lower premium context units for the split path (420
  versus 1500). Matching IDs alone cannot produce a strong-positive result.

The comparison is an executable oracle for measurement logic, not empirical
proof that the split approach works on live appservice. Only the separately
authorized dogfood run can establish or falsify that proposition.
