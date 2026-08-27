# AXIOMS.md — T18 governance axioms

These axioms constrain every conforming implementation. They are stated to be
checkable — each maps to a property the verifier (ZRSV) or an SMT template can
test.

- **A1 — Append-only.** History is never rewritten. A correction is a new
  artifact that references the state it amends. Deletion and mutation of past
  artifacts are representable only as detectable tampering.
- **A2 — Content addressing.** An artifact's identity is the hash of its
  canonical content. Two artifacts with identical canonical bodies are the same
  artifact; no artifact exists apart from its content.
- **A3 — Genesis anchoring.** Every chain has exactly one genesis artifact whose
  parent is the null hash (`0` × 64). Every other artifact has exactly one
  parent, the preceding head.
- **A4 — Verifiability over trust.** Any party, given only the serialized
  chain, can recompute the full state and reach a binary verdict. No trusted
  prover, host, or timestamp is required for verification.
- **A5 — Determinism.** Identical inputs produce identical artifact identities
  on any platform, in any process, at any time. Canonicalization (SPEC §2.1) is
  part of the protocol, not an implementation detail.
- **A6 — Explicit goals.** A governance goal is admissible only if stated as a
  checkable predicate over artifacts — encodable as an SMT query or an
  executable predicate. "The system should be fair" is not a goal;
  "no amendment artifact lacks a prior ratification artifact" is.
