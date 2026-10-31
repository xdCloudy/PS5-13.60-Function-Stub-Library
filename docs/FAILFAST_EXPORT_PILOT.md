# Provisional fail-fast export pilot

This opt-in prototype tests the same kind of throwing export used by
AnyPS5 libSceJsc/LegacyExports. It is NOT an approved replacement for the
independent ABI evidence gates in the existing auto-submission pipeline.

The bounded proposal at proposals/anyps5-failfast-pilot.json contains three
names and NIDs, all rechecked against the original public 3.20 forwarders
and confirmed 13.60 identities at execution time. The generator refuses
unverified NIDs, duplicate names, source collisions, already exported NIDs,
unsupported libraries, or a changed source layout.

Generated functions have provisional int() host-side declarations and call
NotImplemented_nid_no_patch(__func__) immediately. No guest arguments are
accessed and there is no normal return or guessed success. This does not
establish the true guest prototype or guarantee that a maintainer will accept
the convention. Do not treat it as verified ABI evidence.

.github/workflows/anyps5-failfast-pilot.yml performs unit tests, upstream
conventions and public header checks, the **official upstream live PR
overlap scanner**, a full Linux build, and CTest. It fails closed if a
scan cannot finish or the original source changes before publication.

A passing first run opens **one draft upstream PR** as xdCloudy using the
existing ANYPS5_SUBMIT_TOKEN; it never merges, rebases or overwrites an
existing contributor branch. Subsequent reruns must not create duplicate PRs.

This intentionally remains limited to three functions and one existing
library until upstream maintainers validate whether ABI-provisional
fail-fast registrations are appropriate. Do not scale the batch limit,
schedule repeated submissions, or call the output ABI-reviewed on this
evidence alone.
