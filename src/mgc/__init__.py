"""MGC — Merkle Governance Chain.

Content-addressed, tamper-evident governance artifacts (T18 spec, section 2-3).
Standard library only.
"""

from .artifact import GENESIS_PARENT, GovernanceArtifact, canonical_bytes
from .chain import ChainError, MerkleGovernanceChain

__all__ = [
    "GENESIS_PARENT",
    "GovernanceArtifact",
    "canonical_bytes",
    "ChainError",
    "MerkleGovernanceChain",
]

__version__ = "0.1.0"
