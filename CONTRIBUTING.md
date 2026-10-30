# Contributing to the function catalogue

You do not need to develop an emulator to help.

## Useful contributions

- **Name recovery:** provide the public source, exact function name, NID and logical library.
- **Conflict reports:** identify mismatching names, incorrect ownership or invalid provenance.
- **Classification:** explain whether an export belongs to a system library, application, middleware or shell.
- **ABI validation:** provide separately reviewed, public prototype evidence when relevant to AnyPS5.

Start with the [coverage dashboard](reports/coverage-matrices.md) and
[review queues](reports/source-320-review.jsonl).
A missing name is a request for evidence, not an invitation to guess.

## Submitting a correction

Open an issue or PR describing the exact (library, NID), the cited public
source revision, what has been independently checked, what remains unknown,
and why the change should be published. Do not claim a 3.20-only observation
is a 13.60 export.

Never upload firmware, binaries, proprietary SDK headers, console memory,
keys, passwords, private logs or copies of upstream forwarding C files.

Reviewed names must pass the repository's NID algorithm. Function parameters,
return types, implementation correctness and firmware version remain separate
verification gates.

## Updating reports

For report or documentation changes, run:

~~~sh
python -m unittest discover -s tests -v
python tools/build_coverage.py
~~~

The generated Markdown and JSON must agree. If an upstream scan was incomplete,
keep that status visible. Do not fill a missing value with zero.

[Beginner overview](README.md) · [Technical fields](DATA_DICTIONARY.md) ·
[Data policy](DATA_POLICY.md)
