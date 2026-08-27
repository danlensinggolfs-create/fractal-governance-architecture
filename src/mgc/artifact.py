"""Governance artifact — the atomic, content-addressed unit of T18 governance.

Identity = SHA-256 of the canonical JSON body (SPECIFICATION.md section 2.1).
No wall-clock data enters the hashed body, so hashing is deterministic and
platform-independent (axiom A5).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict

#: Null parent of the genesis artifact (axiom A3): 64 hex zeroes.
GENESIS_PARENT = "0" * 64


def canonical_bytes(obj: Dict[str, Any]) -> bytes:
    """Canonical JSON serialization (SPECIFICATION.md section 2.1).

    UTF-8, lexicographically sorted keys, no insignificant whitespace,
    NaN/Infinity rejected. Identical inputs produce identical bytes on any
    platform (axiom A5).
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class GovernanceArtifact:
    """An immutable governance artifact.

    The hash is always derived from the body; it is never stored on the
    artifact itself, so an in-memory artifact cannot disagree with its hash.
    """

    artifact_type: str
    payload: Dict[str, Any]
    parent_hash: str = GENESIS_PARENT

    def body(self) -> Dict[str, Any]:
        """The hashed content: exactly these three fields, nothing else."""
        return {
            "artifact_type": self.artifact_type,
            "parent_hash": self.parent_hash,
            "payload": self.payload,
        }

    @property
    def hash(self) -> str:
        """SHA-256 of the canonical body (axiom A2)."""
        return hashlib.sha256(canonical_bytes(self.body())).hexdigest()

    def to_record(self) -> Dict[str, Any]:
        """Serializable record: body plus the claimed hash."""
        record = self.body()
        record["hash"] = self.hash
        return record

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "GovernanceArtifact":
        """Reconstruct an artifact from a serialized record.

        The record's claimed ``hash`` field is deliberately ignored here;
        comparing claimed vs. recomputed hashes is the verifier's job.
        """
        return cls(
            artifact_type=record["artifact_type"],
            payload=record["payload"],
            parent_hash=record.get("parent_hash", GENESIS_PARENT),
        )
