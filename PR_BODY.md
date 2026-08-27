# PR: T18 initial specification — MGC chain, ZRSV verifier scaffold, SMT templates

**Title:** `T18: initial specification — MGC chain, ZRSV verifier scaffold, SMT templates`

**Body:**

## Summary

Initial specification of the Fractal Governance Architecture (T18): governance
decisions, axioms, goals, and amendments as content-addressed, tamper-evident
artifacts in an append-only Merkle chain, with a zero-trust verifier and
SMT-LIB templates for machine-checkable governance goals.

## Contents

- `SPECIFICATION.md` — artifact model, canonicalization rules, chain model,
  verification model, SMT interface, release/DOI policy
- `AXIOMS.md` — six checkable axioms (A1 append-only … A6 explicit goals)
- `src/mgc/` — `GovernanceArtifact` (canonical JSON + SHA-256 identity) and
  `MerkleGovernanceChain` (append-only, genesis-anchored); stdlib only
- `src/zrsv/` — Zero-trust Reproducible State Verifier scaffold: recomputes
  serialized chains from genesis (hash self-consistency + parent linkage),
  binary verdict, goal-predicate hook, CLI (`python -m zrsv chain.json`)
- `spec/smt2-templates/` — `stated-goal.smt2` (counterexample search) and
  `implicit-encoding.smt2` (successor transition relation, uninterpreted hash)
- `tests/test_mgc.py` — determinism, tamper detection, chain integrity
  (stdlib `unittest`, no third-party dependencies)

## Test plan

```
python -m unittest discover -s tests -v
```

Covers: hash determinism (incl. key-order invariance and exact canonical
bytes), payload tampering, forged claimed hashes, record reordering, record
deletion, empty-chain rejection, JSON round-trip, goal-predicate scaffold.

## Scope notes

- No ZK proofs in v0.1 — ZRSV denotes the zero-*trust* verification property.
- No timestamps inside hashed bodies (determinism, axiom A5); signed timestamp
  attestations are future work as separate artifacts.

## Post-merge

Per `SPECIFICATION.md` §6 and `ZENODO.md`: after merge, cut signed release
`v0.1.0-genesis`; Zenodo archives that immutable state and mints the DOI.
