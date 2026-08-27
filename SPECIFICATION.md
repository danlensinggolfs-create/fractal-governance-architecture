# SPECIFICATION.md — Fractal Governance Architecture (T18), v0.1

**Status:** Initial specification (working branch `t18-initial-specification`)
**Codename:** T18 — the working designation for this specification line.

## 1. Purpose

T18 makes governance machine-verifiable. Decisions, axioms, goals, amendments, and
attestations are expressed as **content-addressed artifacts** in an **append-only
Merkle chain**. Any party can recompute the entire governance state from genesis
and detect any tampering, without trusting timestamps, provers, or hosts.

## 2. Artifact model (MGC)

A *governance artifact* is the atomic unit. Fields:

| Field | Type | Description |
|---|---|---|
| `artifact_type` | string | e.g. `axiom`, `goal`, `decision`, `amendment`, `attestation` |
| `payload` | object | Type-specific content (free-form JSON in v0.1) |
| `parent_hash` | hex string | SHA-256 of the previous artifact; genesis uses 64 zeroes |

**Identity = hash of canonical content.** The artifact hash is

```
SHA-256( CANONICAL_JSON({artifact_type, parent_hash, payload}) )
```

### 2.1 Canonicalization rules (deterministic, platform-independent)

- JSON per RFC 8259, encoded UTF-8
- Object keys sorted lexicographically
- No insignificant whitespace (`,` and `:` separators)
- `NaN`/`Infinity` rejected
- No wall-clock timestamps inside the hashed body (see §6, future work)

## 3. Chain model

- Exactly one **genesis** artifact per chain; its `parent_hash` is `0` × 64.
- Every subsequent artifact's `parent_hash` equals the hash of the current head.
- **Append-only:** history is never rewritten; corrections are new artifacts
  (typically `artifact_type: "amendment"`).
- A chain serializes as a JSON list of records, each record being the artifact
  body plus its claimed `hash`.

## 4. Verification model (ZRSV)

**ZRSV — Zero-trust Reproducible State Verifier.** Given a serialized chain,
ZRSV recomputes everything from genesis:

1. **Hash self-consistency** — every claimed `hash` is recomputed from the
   canonical body and compared. Any payload or field tampering is detected.
2. **Parent linkage** — every `parent_hash` must equal the recomputed hash of
   the preceding artifact. Reordering, deletion, or insertion is detected.
3. **Goal predicates (scaffold)** — named, checkable predicates over the chain
   (AXIOMS.md A6). v0.1 provides the hook; SMT-backed predicates use §5.

Exit condition: verification is **binary** — pass, or fail with the index and
cause of the first-class errors found.

## 5. SMT interface (templates)

`spec/smt2-templates/` provides two SMT-LIB v2 templates:

- **stated-goal.smt2** — counterexample search: assert the schema plus the
  *negation* of a governance goal `G`. `SAT` ⇒ `G` is violable and the model is
  a concrete counterexample; `UNSAT` ⇒ `G` holds for all schema-valid artifacts.
- **implicit-encoding.smt2** — transition-relation encoding: `T(a, a')` holds
  iff `a'` is a valid successor of `a`. The hash function is left
  uninterpreted in v0.1; instantiating it (e.g., bit-vector SHA-256) is future work.

## 6. Versioning and DOI policy

A DOI is minted **only for immutable, merged states**: after the initial PR is
merged and a signed `v0.1.0-genesis` release is cut, Zenodo archives that exact
tree. The DOI therefore denotes a fixed point in the Merkle history, not an
editable draft. (This is standard Zenodo–GitHub release archiving, adopted here
as policy.)

## 7. Non-goals (v0.1)

- No zero-knowledge proofs (ZRSV is a deterministic verifier scaffold; the name
  marks the zero-*trust* property, not a ZK construction).
- No distributed consensus or multi-party signing.
- No trusted timestamping inside hashed bodies (candidate: signed timestamp
  attestations as separate artifacts).
