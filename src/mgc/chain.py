"""Merkle Governance Chain — an append-only chain of governance artifacts.

Implements the chain model of SPECIFICATION.md section 3: one genesis,
parent-linked head, append-only growth (axioms A1-A3).
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .artifact import GENESIS_PARENT, GovernanceArtifact


class ChainError(Exception):
    """Raised on structural chain errors (e.g. appending to a sealed chain)."""


class MerkleGovernanceChain:
    """Append-only chain of :class:`GovernanceArtifact` (axiom A1)."""

    def __init__(self) -> None:
        self._artifacts: List[GovernanceArtifact] = []

    def __len__(self) -> int:
        return len(self._artifacts)

    def __iter__(self):
        return iter(self._artifacts)

    @property
    def head_hash(self) -> str:
        """Hash of the current head, or the null parent for an empty chain."""
        if not self._artifacts:
            return GENESIS_PARENT
        return self._artifacts[-1].hash

    def append(self, artifact_type: str, payload: Dict[str, Any]) -> GovernanceArtifact:
        """Append a new artifact linked to the current head. Returns it."""
        artifact = GovernanceArtifact(
            artifact_type=artifact_type,
            payload=payload,
            parent_hash=self.head_hash,
        )
        self._artifacts.append(artifact)
        return artifact

    def to_records(self) -> List[Dict[str, Any]]:
        """Serialize to the wire format: a list of body+hash records."""
        return [a.to_record() for a in self._artifacts]

    @classmethod
    def from_records(cls, records: List[Dict[str, Any]]) -> "MerkleGovernanceChain":
        """Rebuild a chain from serialized records (unverified — use ZRSV)."""
        chain = cls()
        chain._artifacts = [GovernanceArtifact.from_record(r) for r in records]
        return chain

    def verify(self) -> Tuple[bool, List[str]]:
        """Check internal parent linkage of the in-memory chain.

        For verification of *untrusted serialized* chains (claimed hashes,
        tamper detection), use ``zrsv.verify_chain`` instead — that is the
        zero-trust path (axiom A4). This method only re-derives linkage.
        """
        errors: List[str] = []
        expected_parent = GENESIS_PARENT
        for i, artifact in enumerate(self._artifacts):
            if artifact.parent_hash != expected_parent:
                errors.append(
                    "index %d: parent link broken (expected %s, found %s)"
                    % (i, expected_parent[:16] + "...", artifact.parent_hash[:16] + "...")
                )
            expected_parent = artifact.hash
        return (not errors, errors)
