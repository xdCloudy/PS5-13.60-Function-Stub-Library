# Stub preparation and readiness

[Overview](README.md) · [All libraries](LIBRARIES.md) · [Machine-readable counts](readiness.json)

Named export identities are stub candidates, not implemented functions. Shared NIDs across libraries are counted once in the deduplicated totals.

| Measure | Count |
|---|---:|
| Unique named stub identities | 36,353 |
| Named library/export records | 46,517 |
| Qualified unique throwing-stub candidates | 10,718 |
| Alternate library aliases among qualified records | 2,647 |
| Throwing stubs generated locally | 745 |
| Fully validated stubs | 0 |
| Published AnyPS5 stubs | 0 |

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
| [libSceMediaFrameworkInterface](libraries/libscemediaframeworkinterface-971396c6b2.md) | 135 | 135 | 135 |
| [libSceVideoOut](libraries/libscevideoout-54fc22c577.md) | 199 | 133 | 133 |
| [libSceVnaInternal](libraries/libscevnainternal-b1ef6786a5.md) | 84 | 84 | 0 |
| [libSceIcu](libraries/libsceicu-9790ee85e3.md) | 661 | 72 | 0 |
| [libSceVideoStreamingEngine](libraries/libscevideostreamingengine-5abc5612ed.md) | 70 | 58 | 0 |
| [libSceCustomMusicSysCallWrapper](libraries/libscecustommusicsyscallwrapper-8ee0747c02.md) | 54 | 53 | 0 |
| [libSceEsvm](libraries/libsceesvm-84c73245ba.md) | 45 | 45 | 0 |
| [libSceFont](libraries/libscefont-63ba420c2e.md) | 240 | 44 | 0 |
| [libSceXml](libraries/libscexml-eab4e823a4.md) | 183 | 33 | 0 |
| [libSceAvcap2](libraries/libsceavcap2-9035a2a4ef.md) | 39 | 32 | 0 |
| [libSceDataTransfer](libraries/libscedatatransfer-ca1b6655ff.md) | 88 | 28 | 0 |
| [libSceNpWebApi](libraries/libscenpwebapi-30b6435a6f.md) | 56 | 27 | 27 |
| [libSceComposite](libraries/libscecomposite-23841193cf.md) | 101 | 23 | 0 |
| [libSceVoiceCommand](libraries/libscevoicecommand-e18b06a297.md) | 23 | 23 | 0 |
| [libSceEsvmEngine](libraries/libsceesvmengine-c1d3867cc5.md) | 56 | 13 | 0 |
| [libSceAcm](libraries/libsceacm-a3566cc281.md) | 23 | 11 | 0 |
| [libSceLibcInternal](libraries/libscelibcinternal-f9a6d6abff.md) | 2,593 | 11 | 0 |
| [libSceFontGs](libraries/libscefontgs-b42f55c1c1.md) | 8 | 8 | 0 |
| [libSceMbus](libraries/libscembus-c03d5277f5.md) | 128 | 8 | 0 |
| [libSceRnpsAppMgr](libraries/libscernpsappmgr-cd4e6339be.md) | 35 | 8 | 0 |
| [libSceConnectAccountDialog](libraries/libsceconnectaccountdialog-85ece10b67.md) | 7 | 7 | 0 |
| [libSceMusicCoreInterface](libraries/libscemusiccoreinterface-0263dcc276.md) | 7 | 7 | 0 |
| [libSceNpSpeechToText](libraries/libscenpspeechtotext-0a2725dea6.md) | 7 | 7 | 0 |
| [libSceNpTrophy](libraries/libscenptrophy-838da4c283.md) | 104 | 7 | 0 |
| [libSceRazorCpu](libraries/libscerazorcpu-98b3fdc87b.md) | 42 | 7 | 0 |
| [libSceSaveData](libraries/libscesavedata-f92dab8a68.md) | 104 | 7 | 0 |
| [libSceAudioSystem](libraries/libsceaudiosystem-bfe74a18cc.md) | 8 | 6 | 0 |
| [libSceSysCore](libraries/libscesyscore-d26d4fb57b.md) | 78 | 6 | 0 |
| [libSceSystemLogger2](libraries/libscesystemlogger2-2d5a872a6c.md) | 11 | 6 | 0 |
| [libSceSystemLogger2NativeQueueClient](libraries/libscesystemlogger2nativequeueclient-20515566b1.md) | 11 | 6 | 0 |
| [libSceTextToSpeech2](libraries/libscetexttospeech2-b43e9ee18c.md) | 14 | 6 | 0 |
| [libSceBackupRestoreUtil](libraries/libscebackuprestoreutil-78effa9f1f.md) | 21 | 5 | 0 |
| [libSceCustomMusicAudioOut](libraries/libscecustommusicaudioout-b0940f5719.md) | 10 | 5 | 0 |
| [libSceImeBackend](libraries/libsceimebackend-877b15bc21.md) | 27 | 5 | 0 |
| [libSceMediaFrameworkUtil](libraries/libscemediaframeworkutil-c0af9aa86b.md) | 5 | 5 | 0 |
| [libSceNpSessionSignaling](libraries/libscenpsessionsignaling-58c8806476.md) | 31 | 5 | 0 |
| [libSceVcodec](libraries/libscevcodec-942ad05a91.md) | 5 | 5 | 0 |
| [libSceVenc](libraries/libscevenc-34ac5b7cbe.md) | 19 | 5 | 0 |
| [libmdbg_syscore](libraries/libmdbg_syscore-53c596f5b7.md) | 148 | 5 | 0 |
| [libSceMouse](libraries/libscemouse-acdd5b5e23.md) | 23 | 4 | 0 |
| [libSceNpRemotePlaySessionSignaling](libraries/libscenpremoteplaysessionsignaling-4680662e05.md) | 14 | 4 | 0 |
| [libSceSrcUtl](libraries/libscesrcutl-970010b531.md) | 13 | 4 | 0 |
| [libSceSystemTts](libraries/libscesystemtts-8f4923bcd1.md) | 9 | 4 | 0 |
| [libSceAjm](libraries/libsceajm-5217837f40.md) | 46 | 3 | 0 |
| [libSceOpusCeltEnc](libraries/libsceopusceltenc-b31be2adfa.md) | 14 | 3 | 0 |
| [libScePlayGo](libraries/libsceplaygo-8d02b7ecad.md) | 24 | 3 | 0 |
| [libSceRemoteplay](libraries/libsceremoteplay-0c70684750.md) | 48 | 3 | 0 |
| [libSceSystemLogger2Delivery](libraries/libscesystemlogger2delivery-84263dcdd4.md) | 7 | 3 | 0 |
| [libSceAudiodec](libraries/libsceaudiodec-2dbab67864.md) | 22 | 2 | 0 |
| [libSceLoginMgrServer](libraries/libsceloginmgrserver-9d8badaba5.md) | 32 | 2 | 0 |
| [libScePlayReady4](libraries/libsceplayready4-e431478f47.md) | 86 | 2 | 0 |
| [libSceAjmi](libraries/libsceajmi-70f2344c59.md) | 22 | 1 | 0 |
| [libSceAvPlayerStreaming](libraries/libsceavplayerstreaming-27cc7363f9.md) | 34 | 1 | 0 |
| [libSceCamera](libraries/libscecamera-4529c174dc.md) | 122 | 1 | 0 |
| [libSceDipsw](libraries/libscedipsw-f4b41af254.md) | 10 | 1 | 0 |
| [libSceGameUpdate](libraries/libscegameupdate-16da6af946.md) | 8 | 1 | 0 |
| [libSceNgs2](libraries/libscengs2-6275a7016a.md) | 66 | 1 | 0 |
| [libSceNpEntitlementAccess](libraries/libscenpentitlementaccess-ccae344f14.md) | 26 | 1 | 0 |
| [libSceOpusCeltDec](libraries/libsceopusceltdec-c6e554d356.md) | 12 | 1 | 0 |
| [libSceOpusDec](libraries/libsceopusdec-69c895457e.md) | 15 | 1 | 0 |
| [libSceOpusSilkEnc](libraries/libsceopussilkenc-5db8f0bbee.md) | 15 | 1 | 0 |
| [libScePlayReady2](libraries/libsceplayready2-cf140a4c7d.md) | 56 | 1 | 0 |
| [libSceRudp](libraries/libscerudp-733f5190bf.md) | 35 | 1 | 0 |
| [libSceSharePlay](libraries/libsceshareplay-b821361f17.md) | 21 | 1 | 0 |
| [libSceShellUIUtil](libraries/libsceshelluiutil-8fc7bce6b8.md) | 7 | 1 | 0 |
| [libSceSystemGesture](libraries/libscesystemgesture-47eb2be983.md) | 24 | 1 | 0 |
| [libSceTEEClient](libraries/libsceteeclient-bfc96cbf59.md) | 11 | 1 | 0 |
| [libSceUpdateService](libraries/libsceupdateservice-b7f2a7b06c.md) | 49 | 1 | 0 |
| [libSceVdecCore](libraries/libscevdeccore-219f557635.md) | 25 | 1 | 0 |

The qualified-record column retains logical library identities, so shared exports can appear in multiple rows. The global unique-candidate total removes those aliases.

AnyPS5 comparison snapshot: `bb04a4f1ea0175e9e4f149f0359a764d62ff3296`. These are saved comparisons, not live GitHub state.
