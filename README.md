# PS5 13.60 Function Stub Library

**A searchable catalogue of PlayStation 5 function identities — not a collection of working implementations.**

The project records which function identifiers (NIDs) have been observed, which
names can be linked to them, and where related work exists in
[AnyPS5](https://github.com/boykopovar/AnyPS5). It makes missing information
visible so researchers can avoid repeating the same discovery work.

## Explore the project

**[Interactive coverage dashboard](https://xdcloudy.github.io/PS5-13.60-Function-Stub-Library/)** ·
[Complete coverage matrices](reports/coverage-matrices.md) ·
[Browse all libraries](LIBRARIES.md) ·
[Readiness summary](READINESS.md)

The dashboard is generated from JSON by GitHub Actions. GitHub Pages must be
enabled in repository settings before the public site can be opened.
For an always-readable alternative, use the Markdown matrices above.

## What has been recorded?

The last committed inventory baseline contains:

| Inventory scope | Identities |
|---|---:|
| Firmware extraction labelled **13.60** | **302,338** |
| Older **3.20-only** identities (not confirmed in 13.60) | **11,700** |
| **Total** library/NID records | **314,038** |
| Records with a published name | **47,085** |

Those are inventory totals, **not** implementation percentages. The current
[coverage matrices](reports/coverage-matrices.md) distinguish published names
from strictly reverified names, recent AnyPS5 source matches and open-PR
observations. The repository has 791 tracked libraries; many are application
or middleware libraries, not eligible AnyPS5 system libraries.

### A few terms in plain English

| Term | What it means |
|---|---|
| **Indexed** | A function identity (a library and NID) is recorded. |
| **Named** | A name is attached to the identity. It may still need independent review. |
| **Verified** | The published name passes the applicable status and NID recomputation checks. This does **not** verify its parameter types. |
| **Stubbed** | AnyPS5 contains a placeholder. A throwing stub does not provide the actual functionality. |
| **Implemented** | A source body exists. Correctness still needs build, ABI and runtime validation. |
| **Historical-only** | Seen in older 3.20 evidence, not confirmed as an export in 13.60. |

## What remains unknown?

Most indexed records do not yet have a published name. Some named records fail
the stricter local verification gate. Open AnyPS5 PR scanning may be incomplete.
Neither a recovered name nor a nonthrowing body proves correct ABI or runtime
behaviour. The [dashboard](reports/coverage-matrices.md) shows each stage
separately; it does not invent a single universal completion percentage.

## How does this help AnyPS5?

Researchers can look up names and NIDs before adding duplicate stubs, see
candidate libraries, and find work already present in AnyPS5 main or open PRs.
PR evidence is a *provisional reservation* until the current heads have been
fully checked. Shared NIDs across distinct libraries are preserved, not deleted.

**Nothing in this catalogue automatically grants permission to generate a
function stub.** Unknown ABI signatures, uncertain library ownership and
application/middleware exports remain held for review.

## How is it updated?

The existing GitHub Actions workflow checks AnyPS5 every **three hours**,
records the upstream revision and progressively scans open PRs. It also
reconciles the public [3.20 forwarding database](https://github.com/DNNDHH/PS5-3.20_Libs)
by its actual function-to-NID registrations. A repeat import with identical
source and inventory inputs does not rewrite its source report.

The generator produces Markdown matrices, machine-readable JSON, a searchable
static dashboard and review queues. Third-party names are *not* automatically
promoted into immutable canonical data without applicable approval gates.

[Automation guide](AUTOMATION.md) · [Data dictionary](DATA_DICTIONARY.md) ·
[Source limitations](SOURCES.md) · [Publication policy](DATA_POLICY.md)

## Contribute

You can help by correcting an independently evidenced name, classifying a
library, reporting a conflicting NID or validating an eligible ABI signature.
Start with the [contribution guide](CONTRIBUTING.md). Developers can use the
[maintenance guide](MAINTAINER.md) and
[upstream synchronisation details](UPSTREAM_SYNC.md).

## Where is the data?

The canonical records are under [data/firmware-13.60](data/firmware-13.60)
and [data/historical-3.20-only](data/historical-3.20-only). The
[manifest](manifest.json) records counts and file hashes, while the
[verified-name map](data/verified-name-map.jsonl) contains reviewed name
bindings. Derived progress lives under [reports](reports).

This is a **data-only** repository. No firmware, binaries, forwarding C source,
function bodies, private captures, proprietary SDK files or personal research
paths are included.
