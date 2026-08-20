import copy
import json
import unittest
from pathlib import Path

import alignment_mvp as mvp


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class BootstrapTests(unittest.TestCase):
    def test_bootstrap_is_deterministic_and_non_mutating(self):
        kwargs = dict(
            intent="Investigate why appservice is degraded",
            sprint_id="appservice#99",
            scope=["appservice"],
            budget=12,
        )
        first = mvp.deterministic_bootstrap(**kwargs)
        second = mvp.deterministic_bootstrap(**kwargs)
        self.assertEqual(first, second)
        self.assertFalse(first["authority_mutated"])
        self.assertEqual(first["rendered_command"]["argv"][:3], ["sprintctl", "item", "add"])
        self.assertNotIn("kubectl", first["rendered_command"]["shell"])
        item_show = load("sprintctl-item-show.sanitized.json")
        self.assertEqual(
            first["rendered_command"]["argv"][-2], item_show["item"]["description"]
        )


class ExplorerTests(unittest.TestCase):
    def test_valid_fixture(self):
        normalized = mvp.validate_explorer_output(load("explorer-output.sanitized.json"))
        self.assertEqual(normalized["checkpoint"], "SCOPE_EXPANSION")

    def test_budget_exhaustion_is_deterministic(self):
        value = load("explorer-output.sanitized.json")
        value["operations_used"] = value["operations_limit"]
        with self.assertRaisesRegex(mvp.ContractError, "BUDGET_EXHAUSTED"):
            mvp.validate_explorer_output(value)

    def test_rejects_unbounded_or_outctl_reference(self):
        value = load("explorer-output.sanitized.json")
        value["material_findings"][0]["evidence"] = ["outctl:cap-183"]
        with self.assertRaisesRegex(mvp.ContractError, "content-addressed"):
            mvp.validate_explorer_output(value)


class ProjectionTests(unittest.TestCase):
    def test_projection_matches_frozen_oracle(self):
        actual = mvp.checkpoint_projection(
            load("sprintctl-item-show.sanitized.json"),
            load("explorer-output.sanitized.json"),
        )
        expected = load("checkpoint-projection.expected.json")
        self.assertEqual(actual, expected)
        self.assertFalse(actual["transcript_included"])
        self.assertEqual(actual["basis_revision"], actual["status_revision"])
        self.assertRegex(actual["projection_digest"], r"^sha256:[0-9a-f]{64}$")
        self.assertLessEqual(actual["projection_bytes"], 16_384)

    def test_stale_explorer_basis_is_rejected(self):
        item_show = load("sprintctl-item-show.sanitized.json")
        item_show["item"]["status"] = "blocked"
        item_show["item"]["status_revision"] = (
            "item:123e4567-e89b-12d3-a456-426614174000@status:blocked"
        )
        with self.assertRaisesRegex(mvp.ContractError, "stale"):
            mvp.checkpoint_projection(item_show, load("explorer-output.sanitized.json"))


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.projection = load("checkpoint-projection.expected.json")
        self.policy = load("planner-policy.sanitized.json")

    def test_continue_for_pre_reviewed_adjacent_scope(self):
        result = mvp.stateless_plan(self.projection, self.policy)
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["basis_revision"], self.projection["status_revision"])
        self.assertEqual(result["projection_digest"], self.projection["projection_digest"])
        self.assertFalse(result["authority_mutated"])

    def test_reframe_for_unreviewed_scope(self):
        result = mvp.stateless_plan(self.projection, {"adjacent_scopes": []})
        self.assertEqual(result["decision"], "REFRAME")
        self.assertFalse(result["parent_relation_supported"])

    def test_mutation_stops_for_operator_escalation(self):
        projection = copy.deepcopy(self.projection)
        projection["checkpoint"] = "MUTATION_REQUIRED"
        result = mvp.stateless_plan(projection, self.policy)
        self.assertEqual(result["decision"], "STOP")


class ComparisonTests(unittest.TestCase):
    def test_sanitized_comparison(self):
        result = mvp.compare_runs(
            load("split-run.sanitized.json"), load("premium-only-run.sanitized.json")
        )
        self.assertEqual(result["material_finding_agreement"], 1.0)
        self.assertEqual(result["critical_high_disagreement"], [])
        self.assertAlmostEqual(result["premium_context_reduction"], 0.72)
        self.assertTrue(result["strong_positive_fixture_result"])

    def test_matching_id_with_downgraded_severity_falsifies_result(self):
        split = load("split-run.sanitized.json")
        premium = load("premium-only-run.sanitized.json")
        split["material_findings"][1]["severity"] = "low"
        result = mvp.compare_runs(split, premium)
        self.assertEqual(result["id_only_agreement"], 1.0)
        self.assertEqual(result["severity_mismatch_finding_ids"], ["upstream-timeout"])
        self.assertLess(result["material_finding_agreement"], 1.0)
        self.assertFalse(result["strong_positive_fixture_result"])

    def test_matching_id_with_divergent_explanation_falsifies_result(self):
        split = load("split-run.sanitized.json")
        premium = load("premium-only-run.sanitized.json")
        split["material_findings"][1]["summary"] = (
            "Timeout is caused by an unrelated client-side rendering delay."
        )
        result = mvp.compare_runs(split, premium)
        self.assertEqual(result["id_only_agreement"], 1.0)
        self.assertEqual(result["narrative_mismatch_finding_ids"], ["upstream-timeout"])
        self.assertLess(result["material_finding_agreement"], 1.0)
        self.assertFalse(result["strong_positive_fixture_result"])


if __name__ == "__main__":
    unittest.main()
