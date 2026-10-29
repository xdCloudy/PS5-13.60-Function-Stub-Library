# Data dictionary

| Field | Meaning |
|---|---|
| library | Logical export-library identity from the inventory. |
| nid | Eleven-character export NID; it is not a console or account identifier. |
| name | Exact recovered symbol name, or null. |
| name_status | Whether the name is hash-verified, unresolved, conflicting, or withheld by the publication filter. |
| firmware_versions | Source inventory versions, limited to 3.20 and 13.60. |
| firmware_13_60_export_confirmed | A defined global/weak function export was observed in the local extraction labeled 13.60. |
| kind | Defined function export or historical forwarding-symbol reference. |
| signature_status | Unknown; this dataset does not publish ABI prototypes. |
| scope | Managed/application image, existing system library, accepted upstream placeholder library, or a specific review category. |
| stub_assessment | Candidate/review/coverage status against a saved AnyPS5 snapshot; never a validation certificate. |
| source_evidence | Sanitized evidence classes, without private paths, addresses, logs, or raw captures. |

The primary identity is the pair library/NID. A NID shared across multiple libraries
is retained under each observed logical owner; consumers must handle aliases and
AnyPS5's global duplicate-export restrictions. Counts by source overlap only when
explicitly stated. JSON Line files are grouped by logical library and firmware scope.
