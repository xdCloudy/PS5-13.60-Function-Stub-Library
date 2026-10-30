# Stub preparation and readiness

[Overview](README.md) · [All libraries](LIBRARIES.md) · [Machine-readable counts](readiness.json)

Named export identities are stub candidates, not implemented functions. Shared NIDs across libraries are counted once in the deduplicated totals.

| Measure | Count |
|---|---:|
| Unique named stub identities | 36,691 |
| Named library/export records | 46,859 |
| Qualified unique throwing-stub candidates | 10,750 |
| Alternate library aliases among qualified records | 2,647 |
| Additional system export records needing name/ABI review | 9,989 |
| Throwing stubs generated locally | 963 |
| Stubs passing offline export, declaration, header and conventions gates | 963 |
| Fully validated stubs | 0 |
| Published AnyPS5 stubs | 0 |

## Separate recovery candidate review queue

The [sanitized candidate index](data/recovery-candidates.jsonl) has 742
library/NID identities: 152 already named by the ICU recovery update, 588
unresolved candidates requiring independent corroboration and source review,
and 2 publication-filtered records. This index publishes no candidate names.
It does not change the inventory shards or canonical qualification totals.

If all 588 unresolved candidates were separately approved and integrated,
the *projected* named count would be **46,733 → 47,321** (+588) and the
unique named-NID count **36,565 → 37,150** (+585). These are projections,
not current verified names or automatically qualified AnyPS5 functions.

The retained snapshot counts **10,750** qualified unique candidates, whereas
a read-only audit excluding one unique withheld NID yields **10,749**. This
is an outstanding qualification inconsistency, not rounding. Correcting it
requires a coordinated regeneration of the canonical assessments and reports.

[Full candidate reconciliation](analysis/INTEGRATION-FINDINGS.md).

## What remains before AnyPS5 submission

- Generate the remaining qualified candidates in library-focused batches of at most 150.
- Hold later batches that share source/header/debt insertion sites until their predecessors are integrated.
- Resolve conventions and export-overlap findings; validate declarations and patched binary exports.
- Pass full native builds and tests. Current local validation is blocked by Windows security rejecting test execution and additional runtime test failures.
- Review uncertain ownership, historical-only and managed/AOT records separately. Raw inventory is not an AnyPS5 implementation backlog.

## Library breakdown

| Library | Named records | Qualified records | Generated stubs |
|---|---:|---:|---:|
| [libSceNKWebKit](libraries/libscenkwebkit-30d4baac63.md) | 12,110 | 8,615 | 150 |
| [libSceJsc](libraries/libscejsc-80e21a2f59.md) | 4,115 | 2,952 | 150 |
| [libSceNpCommon](libraries/libscenpcommon-fc2fdcf151.md) | 1,187 | 782 | 150 |
| [libSceMediaFrameworkInterface](libraries/libscemediaframeworkinterface-971396c6b2.md) | 139 | 139 | 139 |
| [libSceVideoOut](libraries/libscevideoout-54fc22c577.md) | 199 | 133 | 133 |
| [libSceVnaInternal](libraries/libscevnainternal-b1ef6786a5.md) | 84 | 84 | 84 |
| [libSceIcu](libraries/libsceicu-9790ee85e3.md) | 813 | 72 | 72 |
| [libSceVideoStreamingEngine](libraries/libscevideostreamingengine-5abc5612ed.md) | 70 | 58 | 58 |
| [libSceCustomMusicSysCallWrapper](libraries/libscecustommusicsyscallwrapper-8ee0747c02.md) | 54 | 53 | 0 |
| [libSceEsvm](libraries/libsceesvm-84c73245ba.md) | 45 | 45 | 0 |
| [libSceFont](libraries/libscefont-63ba420c2e.md) | 240 | 44 | 0 |
| [libSceAvcap2](libraries/libsceavcap2-9035a2a4ef.md) | 42 | 35 | 0 |
| [libSceXml](libraries/libscexml-eab4e823a4.md) | 183 | 33 | 0 |
| [libSceDataTransfer](libraries/libscedatatransfer-ca1b6655ff.md) | 88 | 28 | 0 |
| [libSceNpWebApi](libraries/libscenpwebapi-30b6435a6f.md) | 56 | 27 | 27 |
| [libSceComposite](libraries/libscecomposite-23841193cf.md) | 101 | 23 | 0 |
| [libSceVoiceCommand](libraries/libscevoicecommand-e18b06a297.md) | 23 | 23 | 0 |
| [libSceEsvmEngine](libraries/libsceesvmengine-c1d3867cc5.md) | 56 | 13 | 0 |
| [libSceAcm](libraries/libsceacm-a3566cc281.md) | 23 | 11 | 0 |
| [libSceLibcInternal](libraries/libscelibcinternal-f9a6d6abff.md) | 2,593 | 11 | 0 |
| [libSceMbus](libraries/libscembus-c03d5277f5.md) | 131 | 11 | 0 |
| [libSceAppInstUtil](libraries/libsceappinstutil-783ade3c34.md) | 132 | 8 | 0 |
| [libSceFontGs](libraries/libscefontgs-b42f55c1c1.md) | 8 | 8 | 0 |
| [libSceRnpsAppMgr](libraries/libscernpsappmgr-cd4e6339be.md) | 35 | 8 | 0 |
| [libSceSaveData](libraries/libscesavedata-f92dab8a68.md) | 105 | 8 | 0 |
| [libSceConnectAccountDialog](libraries/libsceconnectaccountdialog-85ece10b67.md) | 7 | 7 | 0 |
| [libSceMusicCoreInterface](libraries/libscemusiccoreinterface-0263dcc276.md) | 7 | 7 | 0 |
| [libSceNpSpeechToText](libraries/libscenpspeechtotext-0a2725dea6.md) | 7 | 7 | 0 |
| [libSceNpTrophy](libraries/libscenptrophy-838da4c283.md) | 104 | 7 | 0 |
| [libSceRazorCpu](libraries/libscerazorcpu-98b3fdc87b.md) | 42 | 7 | 0 |
| [libSceSysCore](libraries/libscesyscore-d26d4fb57b.md) | 79 | 7 | 0 |
| [libSceAudioSystem](libraries/libsceaudiosystem-bfe74a18cc.md) | 8 | 6 | 0 |
| [libSceSystemLogger2](libraries/libscesystemlogger2-2d5a872a6c.md) | 11 | 6 | 0 |
| [libSceSystemLogger2NativeQueueClient](libraries/libscesystemlogger2nativequeueclient-20515566b1.md) | 11 | 6 | 0 |
| [libSceTextToSpeech2](libraries/libscetexttospeech2-b43e9ee18c.md) | 14 | 6 | 0 |
| [libSceBackupRestoreUtil](libraries/libscebackuprestoreutil-78effa9f1f.md) | 21 | 5 | 0 |
| [libSceCustomMusicAudioOut](libraries/libscecustommusicaudioout-b0940f5719.md) | 10 | 5 | 0 |
| [libSceImeBackend](libraries/libsceimebackend-877b15bc21.md) | 27 | 5 | 0 |
| [libSceMediaFrameworkUtil](libraries/libscemediaframeworkutil-c0af9aa86b.md) | 5 | 5 | 0 |
| [libSceNpSessionSignaling](libraries/libscenpsessionsignaling-58c8806476.md) | 31 | 5 | 0 |
| [libScePlayReady4](libraries/libsceplayready4-e431478f47.md) | 89 | 5 | 0 |
| [libSceVcodec](libraries/libscevcodec-942ad05a91.md) | 5 | 5 | 0 |
| [libSceVenc](libraries/libscevenc-34ac5b7cbe.md) | 19 | 5 | 0 |
| [libmdbg_syscore](libraries/libmdbg_syscore-53c596f5b7.md) | 148 | 5 | 0 |
| [libSceMouse](libraries/libscemouse-acdd5b5e23.md) | 23 | 4 | 0 |
| [libSceNpRemotePlaySessionSignaling](libraries/libscenpremoteplaysessionsignaling-4680662e05.md) | 14 | 4 | 0 |
| [libSceOpusCeltEnc](libraries/libsceopusceltenc-b31be2adfa.md) | 15 | 4 | 0 |
| [libScePad](libraries/libscepad-190bd602e9.md) | 194 | 4 | 0 |
| [libSceSrcUtl](libraries/libscesrcutl-970010b531.md) | 13 | 4 | 0 |
| [libSceSystemTts](libraries/libscesystemtts-8f4923bcd1.md) | 9 | 4 | 0 |
| [libSceAjm](libraries/libsceajm-5217837f40.md) | 46 | 3 | 0 |
| [libScePlayGo](libraries/libsceplaygo-8d02b7ecad.md) | 24 | 3 | 0 |
| [libSceRemoteplay](libraries/libsceremoteplay-0c70684750.md) | 48 | 3 | 0 |
| [libSceSystemLogger2Delivery](libraries/libscesystemlogger2delivery-84263dcdd4.md) | 7 | 3 | 0 |
| [libSceAgc](libraries/libsceagc-3be1b8ac02.md) | 243 | 2 | 0 |
| [libSceAudiodec](libraries/libsceaudiodec-2dbab67864.md) | 22 | 2 | 0 |
| [libSceLoginMgrServer](libraries/libsceloginmgrserver-9d8badaba5.md) | 32 | 2 | 0 |
| [libSceAjmi](libraries/libsceajmi-70f2344c59.md) | 22 | 1 | 0 |
| [libSceAvPlayerStreaming](libraries/libsceavplayerstreaming-27cc7363f9.md) | 34 | 1 | 0 |
| [libSceAvSetting](libraries/libsceavsetting-620714af3c.md) | 128 | 1 | 0 |
| [libSceCamera](libraries/libscecamera-4529c174dc.md) | 122 | 1 | 0 |
| [libSceDipsw](libraries/libscedipsw-f4b41af254.md) | 10 | 1 | 0 |
| [libSceGameUpdate](libraries/libscegameupdate-16da6af946.md) | 8 | 1 | 0 |
| [libSceNgs2](libraries/libscengs2-6275a7016a.md) | 66 | 1 | 0 |
| [libSceNpEntitlementAccess](libraries/libscenpentitlementaccess-ccae344f14.md) | 26 | 1 | 0 |
| [libSceNpPartner001](libraries/libscenppartner001-b5ae22d388.md) | 5 | 1 | 0 |
| [libSceOpusCeltDec](libraries/libsceopusceltdec-c6e554d356.md) | 12 | 1 | 0 |
| [libSceOpusDec](libraries/libsceopusdec-69c895457e.md) | 15 | 1 | 0 |
| [libSceOpusSilkEnc](libraries/libsceopussilkenc-5db8f0bbee.md) | 15 | 1 | 0 |
| [libScePlayReady2](libraries/libsceplayready2-cf140a4c7d.md) | 56 | 1 | 0 |
| [libSceRudp](libraries/libscerudp-733f5190bf.md) | 35 | 1 | 0 |
| [libSceSharePlay](libraries/libsceshareplay-b821361f17.md) | 21 | 1 | 0 |
| [libSceShellUIUtil](libraries/libsceshelluiutil-8fc7bce6b8.md) | 7 | 1 | 0 |
| [libSceSystemGesture](libraries/libscesystemgesture-47eb2be983.md) | 24 | 1 | 0 |
| [libSceTEEClient](libraries/libsceteeclient-bfc96cbf59.md) | 11 | 1 | 0 |
| [libSceUpdateService](libraries/libsceupdateservice-b7f2a7b06c.md) | 50 | 1 | 0 |
| [libSceVdecCore](libraries/libscevdeccore-219f557635.md) | 25 | 1 | 0 |

The qualified-record column retains logical library identities, so shared exports can appear in multiple rows. The global unique-candidate total removes those aliases.

AnyPS5 comparison snapshot: `bb04a4f1ea0175e9e4f149f0359a764d62ff3296`. These are saved comparisons, not live GitHub state.

## Read-only candidate-count audit (2026-10-29)

The totals above and in `readiness.json` are **saved published-snapshot counts**,
not fresh checks against live AnyPS5. In a separate full-inventory read-only
audit, applying the requirement that every qualified record have a published,
hash-verified name yielded **13,395 candidate library/NID records / 10,749
unique NIDs**, rather than the saved **13,397 / 10,750**. The difference is
two deliberately withheld-name records, in `libSceNKWebKit` and `libSceJsc`,
sharing NID `eUw-w9kwIhg`. Their names must remain withheld and these records
must not be considered currently qualified.

This is a documented validation finding, **not a regeneration** of the canonical
dataset or readiness files. A later coordinated update must fix the underlying
assessments and regenerate every affected library page, manifest, summary and
readiness artifact together. No runtime ABI tests, current-main coverage
reconciliation or exhaustive open-PR reservation audit was performed as part
of this read-only candidate-count check.

## ICU name-only recovery (2026-10-29)

152 previously unresolved observed `libSceIcu` 13.60 exports now have verified name/NID bindings, independently checked against the fixed PS5 hashing algorithm, pinned catalogue entries and public ICU C API headers. This brings named export records to 46,733 and distinct named NIDs to 36,565. No ABI, implementation, throwing-stub qualification or live AnyPS5 coverage claim is inferred. The retained readiness PNG represents an earlier saved snapshot.
