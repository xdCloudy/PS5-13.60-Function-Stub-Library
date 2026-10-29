# Privacy and publication policy

Publication uses a strict field allowlist. Raw databases and research files are
never copied into this repository. The allowlist excludes local filesystem paths,
hostnames, local usernames, email addresses, IP addresses, console/account identifiers,
credentials, keys, raw logs, memory addresses, firmware hashes, binary contents,
decompiled functions, disassembly, function bodies, signatures, and source code.

Symbol/library strings are separately checked for path, contact, credential and
host-identity patterns. An unsafe name is withheld while its safe NID record remains.
There are no executable scripts, build files, workflows, packages, or C/C++ stubs.
New publication commits use a generic database identity and a generic noreply address.
The original bootstrap commit uses a public pseudonym and a GitHub noreply address.

Automated checks reduce accidental disclosure; they do not establish export behavior
or make unresolved records eligible for implementation. Corrections should preserve
unknown/conflict states rather than guess missing names or prototypes.
