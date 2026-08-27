"""CLI entry point: ``PYTHONPATH=src python -m zrsv chain.json``.

Exit code 0 iff the chain verifies (binary verdict, SPECIFICATION.md section 4).
"""

from __future__ import annotations

import json
import sys

from .verifier import verify_chain


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print("usage: python -m zrsv <chain.json>", file=sys.stderr)
        return 2

    with open(argv[0], "r", encoding="utf-8") as fh:
        records = json.load(fh)

    report = verify_chain(records)
    print(report.summary())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
