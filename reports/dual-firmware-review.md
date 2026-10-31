# Dual-firmware AnyPS5 review candidates

Read-only identity/evidence triage. This is NOT approval to generate,
implement, submit, or merge AnyPS5 stubs.

Original 3.20 source: DNNDHH/PS5-3.20_Libs @ b2a77c09cd71c01f34c790cfbe98c751a13262ad
13.60 catalogue: xdCloudy/PS5-13.60-Function-Stub-Library @ 76d3f717f2d2f9847eea3c36ea6e8b56cd8426c2
AnyPS5 comparison snapshot: c3c45d73abd34dca81da6bad87cb6d36ea437a66
Complete upstream open PR snapshot: False

## Classification counts

| Class | Count |
|---|---:|
| already_covered_or_reserved_snapshot | 17595 |
| confirmed_13.60_only | 1170 |
| dual_3.20_and_13.60 | 10216 |
| historical_3.20_only | 9452 |
| not_an_assessed_missing_stub | 271346 |
| unverified_13.60_name | 2011 |

## Sampled review queues

Cross-firmware name matches are NOT ABI, return type or behaviour proof.
3.20-only records must never be silently promoted to 13.60.
All open-PR and main export overlaps must be verified afresh before submission.
Only reviewed records and approval files on trusted main may reach
the pre-existing AnyPS5 draft-PR publisher.

### dual_3.20_and_13.60

| Library | Symbol | NID | Review requirement |
|---|---|---|---|
| libSceIcu | ubrk_getAvailable | +Nd4bYkEgRc | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_next | 4Uj1DZGlHTw | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_reset | 5O8bmW45o0U | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_fromUnicode | 6ZIjQAWKeRs | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_isNormalized | 7ETpt3V2fEU | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_getName | 7pCOClUrUmM | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ures_getByKey | 8WDJjbxNvCg | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_preceding | 9hkT1aMC0Rs | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getScript | 9lLmMrDj590 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_open | AKenFQbXGE0 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_getRawDecomposition | B8jGs8D+GHY | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucurr_openISOCurrencies | BFt6nFM3lbc | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getBaseName | CZ0z95gBgXg | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_getNFDInstance | Drupl3SzOhM | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_setFromUCallBack | E0yB1UHl4VI | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_addLikelySubtags | HQ6DCQrAXD4 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | u_tolower | I7A4lT+s9h8 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_countAvailable | J5lZTL2H6Aw | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_close | JTIHqYZFMQE | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_setSubstChars | Ku0Rs703XaI | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_toUChars | LvSzmTZ0Mss | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_open | NfGO57hqUEw | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_toUnicode | O1eMKYxVlTs | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ublock_getCode | Oi8niAD8r1M | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uscript_hasScript | PWK6yVIGNuY | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getKeywordValue | QYSES3tXUHM | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getCountry | SIZrguvplN4 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucurr_getName | T7jc4xaLMKo | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_forLanguageTag | a+8yAm1ZfCE | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_getRuleStatus | av8J5NBkbRE | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_countAvailable | bZT8JIrrg3I | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ures_open | bpD6xUk4QVI | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_first | cL3dlqTcRqk | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_following | dC+0Pz5afr0 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getLanguage | dxyWDe5AwgY | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_normalize | eMM8e4yA3AU | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | u_totitle | f4x1+G7t6eY | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uscript_getScript | fiX2RRLQhak | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_current | fsgqunLD2b8 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_setFallback | iEe61PaW1pg | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_getNFCInstance | ikNH4c6kdMw | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ucnv_convertEx | lPKKDtEmEgM | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getDefault | m1nD9D9LmP0 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | udata_setFileAccess | mCyTdtewGpk | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_last | n6SEUE4Txvg | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_getNFKDInstance | nyO3x1IgiSI | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | utext_openUChars | o9+yMOok2Zs | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_getCharacterOrientation | pMLs993oHk0 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_setUText | qQMUbG5L6oE | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | u_toupper | rpv+luk5Ye0 | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | utext_setup | sEKpfqARKPI | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_setKeywordValue | sw98L1MbqpM | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_previous | tGeOQLpMGgA | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_toUnicodeLocaleType | tRTGVdmiGzQ | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | unorm2_getNFKCInstance | u7NoGsVfzcU | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | udata_setCommonData | wHZwCpZVcGI | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_minimizeSubtags | yb9tILRzD1k | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | utext_openConstUnicodeString | yc1XEzBopCw | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | ubrk_isBoundary | ypOz3lP3VhE | needs_independent_abi_and_live_overlap_evidence |
| libSceIcu | uloc_toLanguageTag | zmMWRKwedmw | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC25numberOfOSRExitFuzzChecksEv | 0yriBj5rS3U | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC4Yarr17RegularExpressiondaEPv | 1+Y+ykZkTwg | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC6JSCell12dumpToStreamEPKS0_RN3WTF11PrintStreamE | 13Vdz0yQpSw | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3WTF10hasElapsedERKNS_24TimeWithDynamicClockTypeE | 13eZprwQdRI | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN9Inspector24NetworkBackendDispatcherD2Ev | 15Cz0VyipAQ | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN9Inspector26TimelineFrontendDispatcherdlEPv | 15DNj4tGe8c | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC16CompleteSubspace16allocatorForSlowEm | 15JBN0lRT1s | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC21loadAndEvaluateModuleEPNS_14JSGlobalObjectERKNS_10SourceCodeENS_7JSValueE | 167jPcYThXk | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3WTF6String28numberToStringFixedPrecisionEfjNS_29TrailingZerosTruncatingPolicyE | 16H0tI43iL8 | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN9Inspector24CanvasFrontendDispatcher16recordingStartedERKN3WTF6StringENS_8Protocol9Recording9InitiatorE | 16iE1U5SFuk | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3WTF17charactersToFloatEPKDsmRm | 18MTG+xtvtU | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC16InternalFunction13visitChildrenEPNS_6JSCellERNS_11SlotVisitorE | 18gO8FIVDOg | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZNK9Inspector22InspectorDebuggerAgent7enabledEv | 1DD+9cjt3hU | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZNK9Inspector18InjectedScriptHost16savedResultAliasEv | 1EYcTwBoE4w | needs_independent_abi_and_live_overlap_evidence |
| libSceJsc | _ZN3JSC18GCActivityCallback6cancelEv | 1Gm03etxDkU | needs_independent_abi_and_live_overlap_evidence |

### confirmed_13.60_only

| Library | Symbol | NID | Review requirement |
|---|---|---|---|
| libmdbg_syscore | sceDebugGetAmprCounterInfo | ObMAmE6qMSw | needs_independent_abi_and_live_overlap_evidence |
| libmdbg_syscore | sceMdbgSetResult | TyelACu501E | needs_independent_abi_and_live_overlap_evidence |
| libmdbg_syscore | sceMdbgFinalizeForShellCore | txc1CarzXK8 | needs_independent_abi_and_live_overlap_evidence |
| libmdbg_syscore | sceMdbgReceiveEvent | zgg+ApEodYA | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO1_Clear | +o6KUwnCB+0 | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO1_RenderObject | 0P2PH7lou4g | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO1_Activate | 5pi7bGbV7JM | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO1_Output | 7EGMt3d6RAk | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcm_ConvReverb_SharedIr_2 | PVx9oQUaDdk | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO1_RenderAmbisonicsChannel | ZViifnXeAUc | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO2_Activate | aUfAPcEySHU | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO1_RenderPassthroughObject | eU9FRHNi+xU | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcmChain_Audio3dPO2_RenderDelay | p23f04CznHs | needs_independent_abi_and_live_overlap_evidence |
| libSceAcm | sceAcm_ConvReverb_SharedInput_2 | wM41Cc+ieog | needs_independent_abi_and_live_overlap_evidence |
| libSceAgc | sceAgcGetRegisterDefaultsInternal_0090 | MGEQMJBhdtc | needs_independent_abi_and_live_overlap_evidence |
| libSceAgc | sceAgcGetRegisterDefaults_0090 | ddU6mOWyY40 | needs_independent_abi_and_live_overlap_evidence |
| libSceAjm | sceAjmGetFailedInstance | Ct3WeO240lw | needs_independent_abi_and_live_overlap_evidence |
| libSceAjm | sceAjmInstanceGetSize | QeaZORfh9GA | needs_independent_abi_and_live_overlap_evidence |
| libSceAjm | sceAjmTelemetryGetLog | Wxcje0U9LNE | needs_independent_abi_and_live_overlap_evidence |
| libSceAjmi | sceAjmiBatchWait | JJ9g04D344Q | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilCheckLatestPatch2 | +78trVvdQVs | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilAppGetIrremovableAppList2 | 4s4aW4Rnv08 | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilGetAddons2 | KXhNVXaVPgw | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilAppUnInstall3 | MY+htcCxP0A | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilGetPatchInstallStatus2 | a5SESfNdyL0 | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilAppRequestMoveApps2 | k1ugAupXfzA | needs_independent_abi_and_live_overlap_evidence |
| libSceAppInstUtil | sceAppInstUtilGetContentSize3 | oToUim0TPY4 | needs_independent_abi_and_live_overlap_evidence |
| libSceAudiodec | sceAudiodecUnregisterCodec | BwHzGZkW0Y4 | needs_independent_abi_and_live_overlap_evidence |
| libSceAudioSystem | sceAudioSystemInit | 7EaoqeyirPY | needs_independent_abi_and_live_overlap_evidence |
| libSceAudioSystem | sceAudioSystemProcessResume | I+AmWGX+bqk | needs_independent_abi_and_live_overlap_evidence |
| libSceAudioSystem | sceAudioSystemTerminate | OSvFwsC7tEo | needs_independent_abi_and_live_overlap_evidence |
| libSceAudioSystem | sceAudioSystemProcessRemove | eacQKJ1yA2E | needs_independent_abi_and_live_overlap_evidence |
| libSceAudioSystem | sceAudioSystemProcessAdd | egc9mLq5Pxg | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetFramePitch | 2GC2UnBJHIA | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetMicVolume | 41+5ixaiTj0 | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetAudioOutVolume | 4S4mGtzLmyI | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2OpenVideo | 4jwUgirLFrA | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetNonVclNalUnitStream3 | 8HjqtZXLvek | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2FreeEncoderVideoMemory | 96UQhNnBlxc | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetMicVolume | BPgql5PsMKo | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2AllocateVideoEncoderMemory | CYgd06bO5q0 | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetImagePaste | Cdf6VsJgvaY | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetVideoOutMode | DHFDHdKAr9U | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2QueryVideoEncoderMemorySize | Dht3tcbRoEY | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetChapterPermissionLevel | GBx9f5BmDvU | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetPrivacyImage | ImOtOnPjgio | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetNonVclNalUnitStream | NeKlrUv+lbY | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetSupportInformation | RW88AiwmL+Y | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2LockInputDataBuffer | S4nvYDibKBw | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetNonVclNalUnitStream2 | VAFgNc0Pfp8 | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2RequestKeyFrame | YaXDckFygvw | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetPrivacyGuard | aAbMwQwWHyM | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetInvalidFrame | fLzv9I4mHF0 | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetImagePasteMemory | j7ClJpPRVQI | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2ReadVideo2 | jkv9MlN7gvs | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetAudioOutVolume | mYgFfxPwEjY | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2GetRecProhibit | pEm2jVo44dE | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2ReadVideo | pN0hIQZsMzc | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2SetChapterOpenLevel | r9BQzY0IvxA | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2AllocateVideoEncoderMemory2 | yN0w4tWivqs | needs_independent_abi_and_live_overlap_evidence |
| libSceAvcap2 | sceAvcap2Select | ysFbdZrSCMM | needs_independent_abi_and_live_overlap_evidence |
| libSceAvPlayerStreaming | sceAvPlayerStreamingRegisterVprinf | GdRYP8ZYDMA | needs_independent_abi_and_live_overlap_evidence |
| libSceAvSetting | sceAvControlInit2 | Jhcj4HDIw04 | needs_independent_abi_and_live_overlap_evidence |
| libSceBackupRestoreUtil | sceBackupRestoreUtilGetRestoreTelemetryInfo | P575mX1sITI | needs_independent_abi_and_live_overlap_evidence |
| libSceBackupRestoreUtil | sceBackupRestoreUtilCalcRequiredSize | cpxQ2BLquHM | needs_independent_abi_and_live_overlap_evidence |
| libSceBackupRestoreUtil | sceBackupRestoreUtilGetRestoreFailedTitles | dy0alSl5ReA | needs_independent_abi_and_live_overlap_evidence |
| libSceCamera | sceCameraIsVrCaptureEnable | bpet5OSAr1E | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorGetSecondaryMemorySize | 5x5tC7zLwq4 | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorGetTFRing | 7pmp5rMZAHQ | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorIsVirtualCanvasHandle | Bt2J+lHKAbQ | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorSetMainPortPixelFormat | CM20n3lds+E | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorStopSeeThroughBuffer | GXq6dO8Wif8 | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorSetNativeVrVideoOutMode | IAnyK1lA1eQ | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorWaitEndOfRenderingIfGpuWorking | IUxijmT0S7g | needs_independent_abi_and_live_overlap_evidence |
| libSceComposite | sceCompositorGetMemoryPoolAddress | Kp5aInbKpf4 | needs_independent_abi_and_live_overlap_evidence |

### historical_3.20_only

| Library | Symbol | NID | Review requirement |
|---|---|---|---|
| gaikai-player | _ZN2GK9PlayerPSN13initializeLibEb | 4zord7MtPtw | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN5resetEv | 79UCYGe6xtQ | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSNaSERKS0_ | EHxdFvoxzCM | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSNC2ERKS0_ | EmrfDsAor7Q | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN17cancelRequestGameEv | EzAwc3tWi+o | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN4stopEv | J1Tu68RHMaA | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN15requestClientIdEv | LpxdSc7EQM4 | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN14testConnectionEv | NOL3hrPcMVU | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSND0Ev | Y7B0vc8885c | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN11setSettingsEPKcb | ZME71iqnOSo | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSNC1ERKS0_ | dZUSSMQ9SwI | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSND1Ev | iDTIi7G3YxU | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN11requestGameEb | q9kzJ0gemWs | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN15cancelStartGameEv | ue3o0cfflkM | historical_only_not_13.60_eligible |
| gaikai-player | _ZN2GK9PlayerPSN11shutdownLibEv | vsOZMpVlVUo | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Decompose | ++lgV9pRsO4 | historical_only_not_13.60_eligible |
| libfreetype | FT_Face_CheckTrueTypePatents | +G9vZcqBAfY | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_PS_Font_Private | +yNEa4OFH1M | historical_only_not_13.60_eligible |
| libfreetype | FT_Load_Sfnt_Table | 09vKaCuNyqI | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Transform | 0Lv6K1d47jg | historical_only_not_13.60_eligible |
| libfreetype | FT_List_Finalize | 0SFUOd2K6n0 | historical_only_not_13.60_eligible |
| libfreetype | FT_Glyph_Stroke | 0rKmI1ZbMAc | historical_only_not_13.60_eligible |
| libfreetype | FT_Bitmap_Copy | 1GL9pCFuiHQ | historical_only_not_13.60_eligible |
| libfreetype | FT_Done_Library | 1XCz6Gk0Lt4 | historical_only_not_13.60_eligible |
| libfreetype | FT_Vector_Length | 1jmC2QcpRl0 | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_Renderer | 1wFNGIk3FR0 | historical_only_not_13.60_eligible |
| libfreetype | FT_Attach_File | 21vkVuOP2lk | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_CMap_Language_ID | 2UZg+FAym4c | historical_only_not_13.60_eligible |
| libfreetype | FT_Stroker_Export | 2rcvKZfm5rI | historical_only_not_13.60_eligible |
| libfreetype | FT_Vector_From_Polar | 2rmvbvOCyjY | historical_only_not_13.60_eligible |
| libfreetype | FT_Vector_Unit | 3WpTQrvGUcU | historical_only_not_13.60_eligible |
| libfreetype | FT_TrueTypeGX_Validate | 4+SScYDT5Pg | historical_only_not_13.60_eligible |
| libfreetype | FT_New_Memory_Face | 40Wa2neSLM0 | historical_only_not_13.60_eligible |
| libfreetype | FT_TrueTypeGX_Free | 4xG87W9dTSg | historical_only_not_13.60_eligible |
| libfreetype | FT_Remove_Module | 5ipBcLYVc2k | historical_only_not_13.60_eligible |
| libfreetype | FT_Library_Version | 5qqbXOGlHw4 | historical_only_not_13.60_eligible |
| libfreetype | FT_Stroker_CubicTo | 6+yXRlVrjbc | historical_only_not_13.60_eligible |
| libfreetype | FT_Vector_Rotate | 6wJwUIVwAxg | historical_only_not_13.60_eligible |
| libfreetype | FT_GlyphSlot_Embolden | 73vg+nRH68g | historical_only_not_13.60_eligible |
| libfreetype | FT_MulFix | 774ZHX0Z3Cc | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Translate | 7HoSJ30RWXk | historical_only_not_13.60_eligible |
| libfreetype | FT_List_Insert | 7VnJtqQSwUU | historical_only_not_13.60_eligible |
| libfreetype | FT_Stroker_ExportBorder | 7cIS2cFG3PE | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Get_CBox | 8ZxmGwESvSQ | historical_only_not_13.60_eligible |
| libfreetype | FT_Property_Get | 8fAMdZCnewA | historical_only_not_13.60_eligible |
| libfreetype | FT_CeilFix | 92e4jZiW9Tc | historical_only_not_13.60_eligible |
| libfreetype | FT_Face_GetVariantSelectors | 9Lm2mfsSmws | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Render | 9km02mPqPJE | historical_only_not_13.60_eligible |
| libfreetype | FT_Glyph_Transform | AVEEb57HhUw | historical_only_not_13.60_eligible |
| libfreetype | FT_Stroker_Set | B3uU5aDZn94 | historical_only_not_13.60_eligible |
| libfreetype | FT_Glyph_StrokeBorder | BBRhYfYBDgU | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_EmboldenXY | BgUMBGvhATU | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Copy | Bhm8Injl0KA | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Done | BqGJsJcFYaM | historical_only_not_13.60_eligible |
| libfreetype | FT_Outline_Check | C4a3dGgs+Cc | historical_only_not_13.60_eligible |
| libfreetype | FT_Set_Charmap | Caez01BS2mE | historical_only_not_13.60_eligible |
| libfreetype | FT_Set_MM_Design_Coordinates | DAmwG6U7YIc | historical_only_not_13.60_eligible |
| libfreetype | FT_Glyph_Copy | Dr3F3qrSQ2c | historical_only_not_13.60_eligible |
| libfreetype | FT_Activate_Size | EBvr2CZnjVo | historical_only_not_13.60_eligible |
| libfreetype | FT_FloorFix | EqN+ED6P2FA | historical_only_not_13.60_eligible |
| libfreetype | FT_Face_SetUnpatentedHinting | EruGr0TR1CU | historical_only_not_13.60_eligible |
| libfreetype | FT_Select_Charmap | G4v5vCrrp40 | historical_only_not_13.60_eligible |
| libfreetype | FT_Init_FreeType | GNsiLzm4SH8 | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_Postscript_Name | GVnNjpJWCXM | historical_only_not_13.60_eligible |
| libfreetype | FT_Library_SetLcdFilterWeights | GiuNQjoj4fs | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_FSType_Flags | H4eyE4ez7O4 | historical_only_not_13.60_eligible |
| libfreetype | FT_Vector_Polarize | HMcNe70D9TI | historical_only_not_13.60_eligible |
| libfreetype | FT_Reference_Face | HkSJXCHCQCU | historical_only_not_13.60_eligible |
| libfreetype | FT_Bitmap_Init | I6LQd5tyt0w | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_PS_Font_Value | Ik17GQynFpw | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_PS_Font_Info | JQyLCevN3aM | historical_only_not_13.60_eligible |
| libfreetype | FT_Sin | L1uHkWTazkI | historical_only_not_13.60_eligible |
| libfreetype | FT_Get_Kerning | LPtlB241JSg | historical_only_not_13.60_eligible |
| libfreetype | FT_Select_Size | LlM3ydj7W1s | historical_only_not_13.60_eligible |
| libfreetype | FT_Add_Module | LonHHN98tMI | historical_only_not_13.60_eligible |

