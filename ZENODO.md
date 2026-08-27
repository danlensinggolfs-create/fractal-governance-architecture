# ZENODO.md — minting the DOI for the immutable genesis state

Policy (SPECIFICATION.md §6): the DOI denotes an **immutable, merged state** of
this repository — never an editable draft. Zenodo's GitHub integration archives
exactly the tree of a release, which is what makes the DOI part of the
chain-of-record rather than a wrapper around a moving target.

## Steps (manual — require your GitHub/Zenodo accounts)

1. Merge the initial PR (`t18-initial-specification` → `main`).
2. Cut a signed tag and release on the merged commit:
   ```bash
   git checkout main && git pull
   git tag -s v0.1.0-genesis -m "T18 initial specification — genesis state"
   git push origin v0.1.0-genesis
   ```
   Then create the GitHub release from that tag.
3. In Zenodo: link your GitHub account, flip the toggle for this repository
   **before** the release (or trigger a re-sync after).
4. Zenodo mints a DOI for the `v0.1.0-genesis` archive. Metadata comes from
   `.zenodo.json` in this repo — review it before the release.
5. Record the DOI as a governance artifact: append an `attestation` artifact
   to the chain whose payload contains the DOI and the release commit SHA.
   That closes the loop — the DOI names the state, the chain attests the name.
