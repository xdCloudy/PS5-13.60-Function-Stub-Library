# Sources and verification

- Local ELF export metadata from research labeled PS5 firmware 13.60. Only normalized
  export identities and sanitized classifications are published; original artifacts
  and their private locations are excluded.
- [PS5 3.20 historical inventory](https://github.com/DNNDHH/PS5-3.20_Libs/tree/b2a77c09cd71c01f34c790cfbe98c751a13262ad).
- [Pinned NID name database](https://github.com/zecoxao/sce_symbols/blob/2883963a0a514ba6e77407a08ef4730a65e88254/aerolib.csv).
- [AnyPS5 NID tooling](https://github.com/boykopovar/AnyPS5) for independent hash computation.
- Public payload SDK symbol names provide corroborating name evidence where a
  concrete firmware export has the same computed NID. They do not prove a PS5 ABI.

Incorrect name/hash pairs are quarantined rather than published as verified names.
Library ownership, export type, name identity, signature knowledge, implementation,
and readiness for an AnyPS5 pull request are separate facts.
No proprietary implementation or binary material is included. Attribution does not
grant rights to firmware, SDKs, or third-party source outside this metadata inventory.
