"""ZRSV verifier core (scaffold).

Zero-trust (axiom A4): nothing in the input is believed. Claimed hashes are
recomputed from canonical bodies; parent links are re-derived from genesis.
Goal predicates (axiom A6) are a scaffold extension point — v0.1 accepts
Python callables; SMT-backed predicates use spec/smt2-templates/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from mgc.artifact import GENESIS_PARENT, GovernanceArtifact

#: A checkable governance goal (axiom A6): record -> bool.
GoalPredicate = Callable[[Dict[str, Any]], bool]


@dataclass
class VerificationReport:
    ok: bool
    artifacts_checked: int
    errors: List[str] = field(default_factory=list)
    goal_results: Dict[str, bool] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [
            "ZRSV verification: %s" % ("PASS" if self.ok else "FAIL"),
            "artifacts checked: %d" % self.artifacts_checked,
        ]
        lines.extend("error: %s" % e for e in self.errors)
        lines.extend(
            "goal %s: %s" % (name, "holds" if holds else "VIOLATED")
            for name, holds in self.goal_results.items()
        )
        return "\n".join(lines)


def verify_chain(
    records: List[Dict[str, Any]],
    goals: Optional[Dict[str, GoalPredicate]] = None,
) -> VerificationReport:
    """Verify a serialized chain from genesis. Pure recomputation, no trust."""
    errors: List[str] = []

    if not records:
        return VerificationReport(
            ok=False,
            artifacts_checked=0,
            errors=["empty chain: no genesis artifact (axiom A3)"],
        )

    expected_parent = GENESIS_PARENT
    for i, record in enumerate(records):
        artifact = GovernanceArtifact.from_record(record)
        recomputed = artifact.hash
        claimed = record.get("hash")

        if claimed != recomputed:
            errors.append(
                "index %d: hash mismatch — claimed %s, recomputed %s"
                % (i, str(claimed)[:16] + "...", recomputed[:16] + "...")
            )
        if artifact.parent_hash != expected_parent:
            errors.append(
                "index %d: broken parent link — expected %s, found %s"
                % (
                    i,
                    expected_parent[:16] + "...",
                    artifact.parent_hash[:16] + "...",
                )
            )
        # The NEXT artifact must point at the recomputed hash, never the
        # claimed one — a forged claimed hash must not propagate.
        expected_parent = recomputed

    goal_results: Dict[str, bool] = {}
    if goals:
        for name, predicate in goals.items():
            goal_results[name] = all(predicate(r) for r in records)

    return VerificationReport(
        ok=not errors and all(goal_results.values()),
        artifacts_checked=len(records),
        errors=errors,
        goal_results=goal_results,
    )
