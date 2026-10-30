# Privacy and publication policy

Publication uses a strict field allowlist. Raw databases and research files are
never copied into this repository. The allowlist excludes local filesystem paths,
hostnames, local usernames, email addresses, IP addresses, console/account identifiers,
credentials, keys, raw logs, memory addresses, firmware hashes, binary contents,
decompiled functions, disassembly, function bodies, signatures, and source code.

Symbol/library strings are separately checked for path, contact, credential and
host-identity patterns. An unsafe name is withheld while its safe NID record remains.
There are no C/C++ function implementations, executable stubs, firmware blobs, SDK files or build outputs. Standard-library-only Python reporting scripts, tests and GitHub Actions workflows are permitted solely to regenerate sanitized metadata and Markdown. Public upstream repository paths may be referenced as evidence; local research paths and raw captures remain excluded.
New publication commits use a generic database identity and a generic noreply address.
The original bootstrap commit uses a public pseudonym and a GitHub noreply address.

Automated checks reduce accidental disclosure; they do not establish export behavior
or make unresolved records eligible for implementation. Corrections should preserve
unknown/conflict states rather than guess missing names or prototypes.

## Publication-filter invariant (clarification)

A matching NID computed from a third-party candidate name must **never**
override `withheld_by_publication_filter`. Keep the sanitized library/NID
identity, omit the withheld name from all public recovery queues and name maps,
and do not count a withheld-name record as qualified merely because the NID
has a hash-matching proposed name. Source and licensing review, firmware scope,
owner evidence and current upstream coverage remain independent publication
and qualification requirements. This section clarifies the existing fail-closed
filter; it authorizes no new public data fields or research artifacts.
