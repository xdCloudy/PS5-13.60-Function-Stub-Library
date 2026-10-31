# PS5 3.20 + 13.60 evidence investigation priorities

All records are unapproved. A missing direct source-text match is not proof of export absence.
Full live open-PR overlap and independent ABI checks remain mandatory.

## Classification

| Status | Count |
|---|---:|
| historical_or_unqualified | 9452 |
| priority_candidates | 3680 |
| source_symbol_already_observed | 7706 |

## Highest-volume libraries

| Library | Dual-source | 13.60-only | Total |
|---|---:|---:|---:|
| libSceJsc | 2545 | 2 | 2547 |
| libSceNpCommon | 281 | 348 | 629 |
| libSceMediaFrameworkInterface | 0 | 120 | 120 |
| libSceNKWebKit | 0 | 120 | 120 |
| libSceVnaInternal | 0 | 71 | 71 |
| libSceIcu | 60 | 0 | 60 |
| libSceCustomMusicSysCallWrapper | 0 | 47 | 47 |
| libSceXml | 28 | 0 | 28 |
| libSceVoiceCommand | 0 | 18 | 18 |
| libSceVideoOut | 0 | 10 | 10 |
| libSceMusicCoreInterface | 0 | 6 | 6 |
| libSceFontGs | 0 | 5 | 5 |
| libSceVcodec | 0 | 5 | 5 |
| libSceMediaFrameworkUtil | 0 | 4 | 4 |
| libSceAgc | 0 | 2 | 2 |
| libSceAjmi | 0 | 1 | 1 |
| libSceNgs2 | 0 | 1 | 1 |
| libSceNpEntitlementAccess | 0 | 1 | 1 |
| libSceNpPartner001 | 0 | 1 | 1 |
| libSceOpusDec | 0 | 1 | 1 |
| libScePad | 0 | 1 | 1 |
| libSceRemoteplay | 0 | 1 | 1 |
| libSceSystemGesture | 0 | 1 | 1 |

## Leading individual research targets

| Library | Symbol | NID | Source class | SDK header hint |
|---|---|---|---|---|
| libSceIcu | ubrk_getAvailable | +Nd4bYkEgRc | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_next | 4Uj1DZGlHTw | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_reset | 5O8bmW45o0U | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_fromUnicode | 6ZIjQAWKeRs | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_isNormalized | 7ETpt3V2fEU | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_getName | 7pCOClUrUmM | dual_3.20_and_13.60 | none |
| libSceIcu | ures_getByKey | 8WDJjbxNvCg | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_preceding | 9hkT1aMC0Rs | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getScript | 9lLmMrDj590 | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_open | AKenFQbXGE0 | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_getRawDecomposition | B8jGs8D+GHY | dual_3.20_and_13.60 | none |
| libSceIcu | ucurr_openISOCurrencies | BFt6nFM3lbc | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getBaseName | CZ0z95gBgXg | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_getNFDInstance | Drupl3SzOhM | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_setFromUCallBack | E0yB1UHl4VI | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_addLikelySubtags | HQ6DCQrAXD4 | dual_3.20_and_13.60 | none |
| libSceIcu | u_tolower | I7A4lT+s9h8 | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_countAvailable | J5lZTL2H6Aw | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_close | JTIHqYZFMQE | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_setSubstChars | Ku0Rs703XaI | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_toUChars | LvSzmTZ0Mss | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_open | NfGO57hqUEw | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_toUnicode | O1eMKYxVlTs | dual_3.20_and_13.60 | none |
| libSceIcu | ublock_getCode | Oi8niAD8r1M | dual_3.20_and_13.60 | none |
| libSceIcu | uscript_hasScript | PWK6yVIGNuY | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getKeywordValue | QYSES3tXUHM | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getCountry | SIZrguvplN4 | dual_3.20_and_13.60 | none |
| libSceIcu | ucurr_getName | T7jc4xaLMKo | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_forLanguageTag | a+8yAm1ZfCE | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_getRuleStatus | av8J5NBkbRE | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_countAvailable | bZT8JIrrg3I | dual_3.20_and_13.60 | none |
| libSceIcu | ures_open | bpD6xUk4QVI | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_first | cL3dlqTcRqk | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_following | dC+0Pz5afr0 | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getLanguage | dxyWDe5AwgY | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_normalize | eMM8e4yA3AU | dual_3.20_and_13.60 | none |
| libSceIcu | u_totitle | f4x1+G7t6eY | dual_3.20_and_13.60 | none |
| libSceIcu | uscript_getScript | fiX2RRLQhak | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_current | fsgqunLD2b8 | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_setFallback | iEe61PaW1pg | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_getNFCInstance | ikNH4c6kdMw | dual_3.20_and_13.60 | none |
| libSceIcu | ucnv_convertEx | lPKKDtEmEgM | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getDefault | m1nD9D9LmP0 | dual_3.20_and_13.60 | none |
| libSceIcu | udata_setFileAccess | mCyTdtewGpk | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_last | n6SEUE4Txvg | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_getNFKDInstance | nyO3x1IgiSI | dual_3.20_and_13.60 | none |
| libSceIcu | utext_openUChars | o9+yMOok2Zs | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_getCharacterOrientation | pMLs993oHk0 | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_setUText | qQMUbG5L6oE | dual_3.20_and_13.60 | none |
| libSceIcu | u_toupper | rpv+luk5Ye0 | dual_3.20_and_13.60 | none |
| libSceIcu | utext_setup | sEKpfqARKPI | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_setKeywordValue | sw98L1MbqpM | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_previous | tGeOQLpMGgA | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_toUnicodeLocaleType | tRTGVdmiGzQ | dual_3.20_and_13.60 | none |
| libSceIcu | unorm2_getNFKCInstance | u7NoGsVfzcU | dual_3.20_and_13.60 | none |
| libSceIcu | udata_setCommonData | wHZwCpZVcGI | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_minimizeSubtags | yb9tILRzD1k | dual_3.20_and_13.60 | none |
| libSceIcu | utext_openConstUnicodeString | yc1XEzBopCw | dual_3.20_and_13.60 | none |
| libSceIcu | ubrk_isBoundary | ypOz3lP3VhE | dual_3.20_and_13.60 | none |
| libSceIcu | uloc_toLanguageTag | zmMWRKwedmw | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC25numberOfOSRExitFuzzChecksEv | 0yriBj5rS3U | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC4Yarr17RegularExpressiondaEPv | 1+Y+ykZkTwg | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC6JSCell12dumpToStreamEPKS0_RN3WTF11PrintStreamE | 13Vdz0yQpSw | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3WTF10hasElapsedERKNS_24TimeWithDynamicClockTypeE | 13eZprwQdRI | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN9Inspector24NetworkBackendDispatcherD2Ev | 15Cz0VyipAQ | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN9Inspector26TimelineFrontendDispatcherdlEPv | 15DNj4tGe8c | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC16CompleteSubspace16allocatorForSlowEm | 15JBN0lRT1s | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC21loadAndEvaluateModuleEPNS_14JSGlobalObjectERKNS_10SourceCodeENS_7JSValueE | 167jPcYThXk | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3WTF6String28numberToStringFixedPrecisionEfjNS_29TrailingZerosTruncatingPolicyE | 16H0tI43iL8 | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN9Inspector24CanvasFrontendDispatcher16recordingStartedERKN3WTF6StringENS_8Protocol9Recording9InitiatorE | 16iE1U5SFuk | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3WTF17charactersToFloatEPKDsmRm | 18MTG+xtvtU | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC16InternalFunction13visitChildrenEPNS_6JSCellERNS_11SlotVisitorE | 18gO8FIVDOg | dual_3.20_and_13.60 | none |
| libSceJsc | _ZNK9Inspector22InspectorDebuggerAgent7enabledEv | 1DD+9cjt3hU | dual_3.20_and_13.60 | none |
| libSceJsc | _ZNK9Inspector18InjectedScriptHost16savedResultAliasEv | 1EYcTwBoE4w | dual_3.20_and_13.60 | none |
| libSceJsc | _ZN3JSC18GCActivityCallback6cancelEv | 1Gm03etxDkU | dual_3.20_and_13.60 | none |

None of these are approved for upstream submission. Public SDK header names
and 3.20 forwarding entries do not establish the correct guest ABI or behaviour.
