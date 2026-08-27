# Fractal Governance Architecture (T18)

Machine-verifiable governance: decisions, axioms, goals, and amendments as
**content-addressed, tamper-evident artifacts** in an append-only Merkle chain,
with a zero-trust verifier scaffold and SMT-LIB templates for goal checking.

- `SPECIFICATION.md` — the T18 architecture (artifact model, chain, verification)
- `AXIOMS.md` — six checkable axioms (A1–A6)
- `src/mgc/` — governance artifact + Merkle Governance Chain (Python, stdlib only)
- `src/zrsv/` — Zero-trust Reproducible State Verifier (scaffold)
- `spec/smt2-templates/` — stated-goal and implicit-encoding SMT-LIB v2 templates
- `tests/` — determinism, tamper-detection, and chain-integrity tests

## Quick start

```bash
# run the test suite (stdlib unittest, no dependencies)
python -m unittest discover -s tests -v

# build a chain and verify it
PYTHONPATH=src python - <<'PY'
import json
from mgc.chain import MerkleGovernanceChain

chain = MerkleGovernanceChain()
chain.append("axiom", {"id": "A1", "text": "History is append-only."})
chain.append("goal",  {"id": "G1", "predicate": "no_self_parent"})
print(json.dumps(chain.to_records(), indent=2))
PY

# verify a serialized chain file
PYTHONPATH=src python -m zrsv chain.json
```

## Status

v0.1 initial specification. See `SPECIFICATION.md` §6 for the release/DOI
policy: a DOI is minted only for merged, signed release states
(`v0.1.0-genesis`), never for editable drafts.

## License

MIT — see `LICENSE`.
