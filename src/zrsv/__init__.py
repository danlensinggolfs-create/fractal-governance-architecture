"""ZRSV — Zero-trust Reproducible State Verifier (scaffold).

Recomputes a serialized governance chain from genesis with no trusted inputs
(T18 spec, section 4; axiom A4). Every claimed hash is recomputed and every
parent link re-derived. The verdict is binary: pass, or fail with causes.
"""

from .verifier import GoalPredicate, VerificationReport, verify_chain

__all__ = ["GoalPredicate", "VerificationReport", "verify_chain"]

__version__ = "0.1.0"
