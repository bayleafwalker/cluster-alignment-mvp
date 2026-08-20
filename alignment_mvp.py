#!/usr/bin/env python3
"""Executable, dependency-free contracts for the cluster-alignment MVP.

This module is deliberately a projection and validation tool.  It never invokes
Sprintctl, an agent runtime, ActionQ, kubectl, Flux, or a credential provider.
Native runtimes execute turns; operators apply any rendered Sprintctl command.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cluster-alignment-mvp/v1"
CHECKPOINTS = {
    "MUTATION_REQUIRED",
    "SCOPE_EXPANSION",
    "BUDGET_EXHAUSTED",
    "EXPLORER_ESCALATION",
}
DECISIONS = {"CONTINUE", "REFRAME", "STOP"}
EVENT_KINDS = {"finding", "scope-request", "proposed-action", "checkpoint"}
REVISION_RE = re.compile(r"^item:[0-9a-fA-F-]{36}@status:(pending|active|done|blocked)$")
EVIDENCE_RE = re.compile(r"^(trace|object|file):sha256:[0-9a-f]{64}$")


class ContractError(ValueError):
    """A fixture or contract instance is unsafe, ambiguous, or invalid."""


def _read_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError("top-level JSON value must be an object")
    return value


def _dump(value: dict[str, Any]) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be non-empty text")
    return value.strip()


def _require_revision(value: Any, field: str = "status_revision") -> str:
    value = _require_text(value, field)
    if not REVISION_RE.fullmatch(value):
        raise ContractError(f"{field} is not a Sprintctl item status revision")
    return value


def _require_evidence(value: Any) -> str:
    value = _require_text(value, "evidence reference")
    if not EVIDENCE_RE.fullmatch(value):
        raise ContractError(
            "evidence references must be content-addressed trace/object/file SHA-256 handles"
        )
    return value


def deterministic_bootstrap(
    *, intent: str, sprint_id: str, scope: list[str], budget: int = 12
) -> dict[str, Any]:
    """Render, but do not execute, a deterministic Sprintctl bootstrap."""
    intent = _require_text(intent, "intent")
    sprint_id = _require_text(sprint_id, "sprint_id")
    normalized_scope = sorted({_require_text(part, "scope") for part in scope})
    if not normalized_scope:
        raise ContractError("scope must contain at least one target")
    if budget < 1 or budget > 50:
        raise ContractError("budget must be between 1 and 50 observations")
    boundary = {
        "schema": SCHEMA,
        "intent": intent,
        "scope": normalized_scope,
        "role": "explorer",
        "capability_class": "non-mutating-observation",
        "operation_budget": budget,
        "checkpoint_conditions": sorted(CHECKPOINTS),
        "runtime": "product-native",
    }
    canonical = json.dumps(boundary, separators=(",", ":"), sort_keys=True)
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    description = f"alignment-boundary sha256:{digest}\n{canonical}"
    argv = [
        "sprintctl",
        "item",
        "add",
        "--sprint-id",
        sprint_id,
        "--track",
        "cluster-alignment",
        "--title",
        intent,
        "--description",
        description,
        "--json",
    ]
    return {
        "schema": SCHEMA,
        "authority_mutated": False,
        "boundary": boundary,
        "boundary_digest": f"sha256:{digest}",
        "rendered_command": {"argv": argv, "shell": shlex.join(argv)},
        "next_read": ["sprintctl", "item", "show", "--id", "<created-id>", "--json"],
    }


def validate_explorer_output(value: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize one cheap explorer's bounded checkpoint output."""
    if value.get("schema") != SCHEMA:
        raise ContractError(f"schema must be {SCHEMA!r}")
    work_item = _require_text(value.get("work_item"), "work_item")
    basis = _require_revision(value.get("basis_revision"), "basis_revision")
    used = value.get("operations_used")
    limit = value.get("operations_limit")
    if not isinstance(used, int) or not isinstance(limit, int) or not (0 <= used <= limit <= 50):
        raise ContractError("operation counts must satisfy 0 <= used <= limit <= 50")
    checkpoint = value.get("checkpoint")
    if checkpoint not in CHECKPOINTS:
        raise ContractError(f"checkpoint must be one of {sorted(CHECKPOINTS)}")
    if used == limit and checkpoint != "BUDGET_EXHAUSTED":
        raise ContractError("an exhausted budget must checkpoint as BUDGET_EXHAUSTED")

    findings = value.get("material_findings", [])
    if not isinstance(findings, list) or len(findings) > 8:
        raise ContractError("material_findings must be a list of at most 8 entries")
    normalized_findings = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ContractError(f"material_findings[{index}] must be an object")
        evidence = finding.get("evidence", [])
        if not isinstance(evidence, list) or len(evidence) > 2:
            raise ContractError("each finding may carry at most 2 evidence references")
        normalized_findings.append(
            {
                "finding_id": _require_text(finding.get("finding_id"), "finding_id"),
                "text": _require_text(finding.get("text"), "finding text"),
                "severity": finding.get("severity", "info"),
                "evidence": [_require_evidence(ref) for ref in evidence],
            }
        )
    result = {
        "schema": SCHEMA,
        "work_item": work_item,
        "basis_revision": basis,
        "operations_used": used,
        "operations_limit": limit,
        "material_findings": normalized_findings,
        "checkpoint": checkpoint,
    }
    for field in ("proposed_next_action", "scope_request"):
        if value.get(field) is not None:
            result[field] = _require_text(value[field], field)
    return result


def checkpoint_projection(
    item_show: dict[str, Any], explorer_output: dict[str, Any], *, max_events: int = 8
) -> dict[str, Any]:
    """Build a bounded planner projection from Sprintctl-shaped read data."""
    explorer = validate_explorer_output(explorer_output)
    item = item_show.get("item")
    if not isinstance(item, dict):
        raise ContractError("item-show input must contain an item object")
    item_id = item.get("id")
    if str(item_id) != explorer["work_item"].split("#")[-1]:
        raise ContractError("explorer work_item does not match item-show item id")
    status_revision = _require_revision(item.get("status_revision"))
    if status_revision != explorer["basis_revision"]:
        raise ContractError("explorer basis_revision is stale relative to item-show")
    if max_events < 1 or max_events > 20:
        raise ContractError("max_events must be between 1 and 20")

    events = item_show.get("events", [])
    if not isinstance(events, list):
        raise ContractError("item-show events must be a list")
    bounded_events = []
    for event in events[-max_events:]:
        payload = event.get("payload") if isinstance(event, dict) else None
        if not isinstance(payload, dict) or payload.get("kind") not in EVENT_KINDS:
            continue
        event_evidence = payload.get("evidence", [])
        if not isinstance(event_evidence, list) or len(event_evidence) > 2:
            raise ContractError("each projected event may carry at most 2 evidence references")
        bounded_events.append(
            {
                "id": event.get("id"),
                "kind": payload["kind"],
                "summary": _require_text(payload.get("summary"), "event summary"),
                "evidence": [_require_evidence(ref) for ref in event_evidence],
            }
        )
    description = _require_text(item.get("description"), "item description")
    boundary_line = description.splitlines()[0]
    if not re.fullmatch(r"alignment-boundary sha256:[0-9a-f]{64}", boundary_line):
        raise ContractError("item description does not carry a valid alignment boundary digest")
    projection = {
        "schema": SCHEMA,
        "work_item": explorer["work_item"],
        "intent": _require_text(item.get("title"), "item title"),
        "status": _require_text(item.get("status"), "item status"),
        "status_revision": status_revision,
        "basis_revision": status_revision,
        "scope": sorted({_require_text(x, "scope") for x in item_show.get("scope", [])}),
        "boundary_digest": boundary_line,
        "material_findings": explorer["material_findings"],
        "recent_material_events": bounded_events,
        "proposed_next_action": explorer.get("proposed_next_action"),
        "scope_request": explorer.get("scope_request"),
        "checkpoint": explorer["checkpoint"],
        "budget": {
            "operations_used": explorer["operations_used"],
            "operations_limit": explorer["operations_limit"],
        },
        "transcript_included": False,
    }
    encoded = json.dumps(projection, separators=(",", ":"), sort_keys=True).encode()
    if len(encoded) > 16_384:
        raise ContractError("planner projection exceeds the 16 KiB bound")
    projection["projection_bytes"] = len(encoded)
    projection["projection_digest"] = f"sha256:{hashlib.sha256(encoded).hexdigest()}"
    return projection


def stateless_plan(projection: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Return CONTINUE, REFRAME, or STOP without conversation or stored state."""
    basis = _require_revision(projection.get("basis_revision"), "basis_revision")
    if projection.get("status_revision") != basis:
        raise ContractError("projection status_revision and basis_revision must match")
    checkpoint = projection.get("checkpoint")
    if checkpoint not in CHECKPOINTS:
        raise ContractError("unknown checkpoint")
    scope_request = projection.get("scope_request")
    adjacent_values = policy.get("adjacent_scopes", [])
    if not isinstance(adjacent_values, list) or not all(
        isinstance(value, str) and value.strip() for value in adjacent_values
    ):
        raise ContractError("adjacent_scopes must be a list of non-empty strings")
    adjacent = set(adjacent_values)
    next_action = projection.get("proposed_next_action")

    if checkpoint == "MUTATION_REQUIRED":
        decision, reason = "STOP", "mutation requires a separately authorized operator/executor path"
    elif checkpoint == "SCOPE_EXPANSION" and scope_request in adjacent:
        decision, reason = "CONTINUE", "requested scope is inside the pre-reviewed adjacent scope set"
    elif checkpoint in {"SCOPE_EXPANSION", "EXPLORER_ESCALATION"}:
        decision, reason = "REFRAME", "direction or scope requires a fresh bounded investigation"
    elif next_action:
        decision, reason = "CONTINUE", "bounded observational next action remains"
    else:
        decision, reason = "STOP", "no bounded observational next action remains"

    result = {
        "schema": SCHEMA,
        "decision": decision,
        "basis_revision": basis,
        "projection_digest": _require_text(projection.get("projection_digest"), "projection_digest"),
        "reason": reason,
        "authority_mutated": False,
    }
    if decision == "CONTINUE":
        result["objective"] = _require_text(next_action, "proposed_next_action")
        result["scope_add"] = [scope_request] if scope_request else []
    elif decision == "REFRAME":
        result["fresh_explorer"] = True
        result["proposed_child_intent"] = _require_text(
            next_action or f"Reframe investigation around {scope_request}", "reframe intent"
        )
        result["parent_relation_supported"] = False
    if result["decision"] not in DECISIONS:
        raise AssertionError("planner emitted an unsupported decision")
    return result


def compare_runs(split: dict[str, Any], premium: dict[str, Any]) -> dict[str, Any]:
    """Compare sanitized split and premium-only investigation results."""
    def index(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
        findings = run.get("material_findings", [])
        if not isinstance(findings, list):
            raise ContractError("comparison material_findings must be a list")
        indexed: dict[str, dict[str, Any]] = {}
        for finding in findings:
            if not isinstance(finding, dict):
                raise ContractError("comparison findings must be objects")
            finding_id = _require_text(finding.get("finding_id"), "finding_id")
            severity = _require_text(finding.get("severity"), "severity").lower()
            if severity not in {"info", "low", "medium", "high", "critical"}:
                raise ContractError("finding severity must be info, low, medium, high, or critical")
            narrative = _require_text(
                finding.get("summary", finding.get("text")), "finding summary"
            )
            normalized_narrative = " ".join(narrative.casefold().split())
            if len(normalized_narrative.encode("utf-8")) > 512:
                raise ContractError("finding summary exceeds the 512-byte comparison bound")
            if finding_id in indexed:
                raise ContractError(f"duplicate finding_id in comparison run: {finding_id}")
            indexed[finding_id] = {
                **finding,
                "severity": severity,
                "normalized_narrative": normalized_narrative,
            }
        return indexed

    split_index, premium_index = index(split), index(premium)
    union = set(split_index) | set(premium_index)
    shared_ids = set(split_index) & set(premium_index)
    severity_mismatches = sorted(
        key
        for key in shared_ids
        if split_index[key]["severity"] != premium_index[key]["severity"]
    )
    narrative_mismatches = sorted(
        key
        for key in shared_ids
        if split_index[key]["normalized_narrative"]
        != premium_index[key]["normalized_narrative"]
    )
    agreement = shared_ids - set(severity_mismatches) - set(narrative_mismatches)
    critical = {
        key
        for key in union
        if split_index.get(key, {}).get("severity") in {"critical", "high"}
        or premium_index.get(key, {}).get("severity") in {"critical", "high"}
    }
    critical_disagreement = sorted(critical - agreement)
    split_metrics = split.get("metrics", {})
    premium_metrics = premium.get("metrics", {})
    result = {
        "schema": SCHEMA,
        "fixture_classification": "sanitized-local",
        "material_finding_agreement": len(agreement) / len(union) if union else 1.0,
        "id_only_agreement": len(shared_ids) / len(union) if union else 1.0,
        "agreed_finding_ids": sorted(agreement),
        "split_only_finding_ids": sorted(set(split_index) - set(premium_index)),
        "premium_only_finding_ids": sorted(set(premium_index) - set(split_index)),
        "critical_high_disagreement": critical_disagreement,
        "severity_mismatch_finding_ids": severity_mismatches,
        "narrative_mismatch_finding_ids": narrative_mismatches,
        "planner_invocations": split_metrics.get("planner_invocations"),
        "planner_evidence_retrievals": split_metrics.get("planner_evidence_retrievals"),
        "premium_context_units": {
            "split": split_metrics.get("premium_context_units"),
            "premium_only": premium_metrics.get("premium_context_units"),
        },
        "unsafe_attempts": {
            "split": split_metrics.get("unsafe_attempts"),
            "premium_only": premium_metrics.get("unsafe_attempts"),
        },
    }
    left = result["premium_context_units"]["split"]
    right = result["premium_context_units"]["premium_only"]
    result["premium_context_reduction"] = (
        1 - (left / right) if isinstance(left, (int, float)) and right else None
    )
    result["strong_positive_fixture_result"] = (
        not critical_disagreement
        and not severity_mismatches
        and not narrative_mismatches
        and result["material_finding_agreement"] >= 0.8
        and (result["premium_context_reduction"] or 0) > 0
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    boot = sub.add_parser("bootstrap", help="render a deterministic, non-executed bootstrap")
    boot.add_argument("--intent", required=True)
    boot.add_argument("--sprint-id", required=True)
    boot.add_argument("--scope", action="append", required=True)
    boot.add_argument("--budget", type=int, default=12)
    explore = sub.add_parser("validate-explorer")
    explore.add_argument("path")
    project = sub.add_parser("project")
    project.add_argument("item_show")
    project.add_argument("explorer_output")
    project.add_argument("--max-events", type=int, default=8)
    plan = sub.add_parser("plan")
    plan.add_argument("projection")
    plan.add_argument("policy")
    compare = sub.add_parser("compare")
    compare.add_argument("split")
    compare.add_argument("premium")
    args = parser.parse_args(argv)
    try:
        if args.command == "bootstrap":
            result = deterministic_bootstrap(
                intent=args.intent, sprint_id=args.sprint_id, scope=args.scope, budget=args.budget
            )
        elif args.command == "validate-explorer":
            result = validate_explorer_output(_read_json(args.path))
        elif args.command == "project":
            result = checkpoint_projection(
                _read_json(args.item_show), _read_json(args.explorer_output), max_events=args.max_events
            )
        elif args.command == "plan":
            result = stateless_plan(_read_json(args.projection), _read_json(args.policy))
        else:
            result = compare_runs(_read_json(args.split), _read_json(args.premium))
    except (ContractError, json.JSONDecodeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    _dump(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
