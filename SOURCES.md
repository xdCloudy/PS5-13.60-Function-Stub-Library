# Sources and verification

- Local ELF export metadata from research labeled PS5 firmware 13.60. Only normalized
  export identities and sanitized classifications are published; original artifacts
  and their private locations are excluded.
- [PS5 3.20 historical inventory](https://github.com/DNNDHH/PS5-3.20_Libs/tree/b2a77c09cd71c01f34c790cfbe98c751a13262ad).
- [Pinned NID name database](https://github.com/zecoxao/sce_symbols/blob/2883963a0a514ba6e77407a08ef4730a65e88254/aerolib.csv).
- [Supplemental public symbol dictionaries](https://github.com/zecoxao/sce_symbols/tree/6bfb2a9772d6697b87e94521cd3a88385fbf1f87): `aerolib.csv`, `ps5_names.txt` and `unique.txt`, pinned by commit and exact Git blob. Whole-line names are independently hashed and matched against existing export identities; they do not establish prototypes or firmware availability.
- [AnyPS5 NID tooling](https://github.com/boykopovar/AnyPS5) for independent hash computation.
- Public payload SDK symbol names and C declarations provide corroborating name evidence where a
  concrete firmware export has the same computed NID. They do not prove a PS5 ABI.

Incorrect name/hash pairs are quarantined rather than published as verified names.
Library ownership, export type, name identity, signature knowledge, implementation,
and readiness for an AnyPS5 pull request are separate facts.
No proprietary implementation or binary material is included. Attribution does not
grant rights to firmware, SDKs, or third-party source outside this metadata inventory.

## Unpublished recovery research checkpoint (2026-10-29)

The data-only inventory at commit `bfec40deb4c47a17d7603ee2bc79aa6862c0c56b`
was checked in a separate read-only research workspace. Its manifest lists 858 data
files, including 856 export JSONL shards. The local audit reported 314,038
library/NID identities, no malformed or duplicate identities, and 46,581
published name/NID bindings passing recomputation. The original export-file
bytes and local audit ledger are **not** included in this repository, so this
report is not an independently reproducible complete rebuild.

An additional pinned candidate source is
[`claimore22/ps5rs`](https://github.com/claimore22/ps5rs/tree/5f252a658ff470bcb2b6cd15205fd8ca64ae4477),
particularly `data/nids.csv`. Its repository identifies its licence as GPL-2.0
and acknowledges community symbol-catalogue sources. A local hash-checked
intersection produced **742 candidate name/NID matches** against currently
unnamed or withheld library identities: **740 normal review proposals** and
**2 deliberately withheld-name records**, which must remain withheld.
These are *research proposals*, not accepted published symbol bindings.
Their per-row provenance, redistribution rights, firmware applicability and
library ownership have not been independently approved. No external catalogue
is copied here and no candidate names are published by this checkpoint.

A cross-library join against the existing 46,581 verified named observations
found **zero unnamed identities sharing a NID with an already verified name**.
Future recovery therefore requires new source evidence or new researched names,
not unverified alias propagation. A matching NID alone does not establish
prototype, export origin, owner or AnyPS5 readiness.
