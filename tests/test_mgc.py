"""MGC test suite: determinism, tamper detection, chain integrity.

Stdlib unittest, no third-party dependencies:
    python -m unittest discover -s tests -v
"""

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mgc.artifact import GENESIS_PARENT, GovernanceArtifact, canonical_bytes
from mgc.chain import MerkleGovernanceChain
from zrsv.verifier import verify_chain


def build_sample_chain() -> MerkleGovernanceChain:
    chain = MerkleGovernanceChain()
    chain.append("axiom", {"id": "A1", "text": "History is append-only."})
    chain.append("goal", {"id": "G1", "predicate": "no_self_parent"})
    chain.append("decision", {"id": "D1", "adopts": "G1", "quorum": 3})
    return chain


class TestDeterminism(unittest.TestCase):
    """Axiom A5: identical inputs -> identical identity, always."""

    def test_same_inputs_same_hash(self):
        a = GovernanceArtifact("axiom", {"id": "A1"}, GENESIS_PARENT)
        b = GovernanceArtifact("axiom", {"id": "A1"}, GENESIS_PARENT)
        self.assertEqual(a.hash, b.hash)

    def test_key_insertion_order_irrelevant(self):
        a = GovernanceArtifact("goal", {"x": 1, "y": 2}, GENESIS_PARENT)
        b = GovernanceArtifact("goal", {"y": 2, "x": 1}, GENESIS_PARENT)
        self.assertEqual(a.hash, b.hash)

    def test_canonical_bytes_stable(self):
        obj = {"b": [1, 2], "a": {"z": None, "m": True}}
        self.assertEqual(canonical_bytes(obj), canonical_bytes(dict(reversed(list(obj.items())))))
        self.assertEqual(canonical_bytes(obj), b'{"a":{"m":true,"z":null},"b":[1,2]}')

    def test_full_chain_rebuild_is_identical(self):
        self.assertEqual(build_sample_chain().to_records(), build_sample_chain().to_records())


class TestTamperDetection(unittest.TestCase):
    """Axiom A1/A4: any mutation of history is detected by recomputation."""

    def test_payload_tamper_detected(self):
        records = build_sample_chain().to_records()
        records[1]["payload"]["predicate"] = "self_parent_allowed"  # forged
        report = verify_chain(records)
        self.assertFalse(report.ok)
        self.assertTrue(any("index 1" in e and "hash mismatch" in e for e in report.errors))

    def test_claimed_hash_forgery_detected(self):
        records = build_sample_chain().to_records()
        records[0]["hash"] = "f" * 64  # forged claim, body untouched
        report = verify_chain(records)
        self.assertFalse(report.ok)
        self.assertTrue(any("index 0" in e for e in report.errors))

    def test_deep_copy_tamper_does_not_touch_original(self):
        records = build_sample_chain().to_records()
        snapshot = copy.deepcopy(records)
        records[2]["payload"]["quorum"] = 1
        self.assertTrue(verify_chain(snapshot).ok)
        self.assertFalse(verify_chain(records).ok)


class TestChainIntegrity(unittest.TestCase):
    """Axiom A3: exactly one genesis, unbroken parent linkage."""

    def test_valid_chain_verifies(self):
        report = verify_chain(build_sample_chain().to_records())
        self.assertTrue(report.ok, msg=report.summary())
        self.assertEqual(report.artifacts_checked, 3)

    def test_live_chain_linkage(self):
        ok, errors = build_sample_chain().verify()
        self.assertTrue(ok, msg=str(errors))

    def test_reordering_detected(self):
        records = build_sample_chain().to_records()
        records[1], records[2] = records[2], records[1]
        self.assertFalse(verify_chain(records).ok)

    def test_deletion_detected(self):
        records = build_sample_chain().to_records()
        del records[1]
        self.assertFalse(verify_chain(records).ok)

    def test_genesis_required(self):
        self.assertFalse(verify_chain([]).ok)

    def test_genesis_parent_is_null(self):
        records = build_sample_chain().to_records()
        self.assertEqual(records[0]["parent_hash"], GENESIS_PARENT)

    def test_json_roundtrip_preserves_validity(self):
        records = build_sample_chain().to_records()
        reloaded = json.loads(json.dumps(records))
        self.assertTrue(verify_chain(reloaded).ok)
        self.assertEqual(len(MerkleGovernanceChain.from_records(reloaded)), 3)

    def test_goal_predicate_scaffold(self):
        records = build_sample_chain().to_records()
        goals = {"typed_payloads": lambda r: isinstance(r["payload"], dict)}
        report = verify_chain(records, goals=goals)
        self.assertTrue(report.ok)
        self.assertEqual(report.goal_results, {"typed_payloads": True})


if __name__ == "__main__":
    unittest.main()
