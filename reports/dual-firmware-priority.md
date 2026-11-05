# PS5 3.20 + 13.60 evidence investigation priorities

All records are unapproved. A missing direct source-text match is not proof of export absence.
Full live open-PR overlap, provider ownership and build checks remain mandatory.
Exact guest ABI is needed to claim returning behaviour, not to propose an explicitly provisional always-throwing import placeholder.

## Classification

| Status | Count |
|---|---:|
| historical_or_unqualified | 9452 |
| priority_candidates | 792 |
| source_symbol_already_observed | 8318 |
| source_symbol_in_other_provider | 2276 |

## Highest-volume libraries

| Library | Dual-source | 13.60-only | Total |
|---|---:|---:|---:|
| libSceNpCommon | 281 | 348 | 629 |
| libSceNKWebKit | 0 | 82 | 82 |
| libSceIcu | 60 | 0 | 60 |
| libSceMediaFrameworkInterface | 0 | 13 | 13 |
| libSceAgc | 0 | 2 | 2 |
| libSceJsc | 0 | 2 | 2 |
| libSceNgs2 | 0 | 1 | 1 |
| libSceNpEntitlementAccess | 0 | 1 | 1 |
| libScePad | 0 | 1 | 1 |
| libSceRemoteplay | 0 | 1 | 1 |

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
| libSceNpCommon | _ZThn16_N3sce2np9LocalFile5WriteEPNS0_6HandleEPKvmPm | +3ySpB1buMs | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClient4ctorEv | +EQNga+wsPc | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9WorkQueue4InitEPKcimm | +dGO+GS2ZXQ | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9HttpTrans11SendRequestEPNS0_6HandleEPKvm | +hKyaJJCE+0 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np12WorkerThreadD2Ev | +qB+WcQlMio | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClient7DestroyEv | +xvhXA8Ci4E | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9EventFlag5ClearEm | 03UlDLFsTfw | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np6ThreadC2Ev | 0f3ylOQJwqE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np4PathD0Ev | 0fwoTW7gqfM | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9LocalFile5WriteEPNS0_6HandleEPKvmPm | 0xL7AwgxphE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient19WaitRequestForAsyncEiij | 1ONFW86TETY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9WorkQueueD1Ev | 1QFKnDJxk3A | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np4Cond6IsInitEv | 1YezZ6DJXgY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np6Handle7DestroyEv | 1atFu71dFAU | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10CancelLockD2Ev | 1iHBAKrdE90 | dual_3.20_and_13.60 | none |

None of these are independently validated as guest ABI. Public SDK header names
and 3.20 forwarding entries do not establish the correct guest ABI or behaviour.
Merged upstream precedents #10068, #9990 and #9695 permit provisional parameterless throwing exports; all still require complete live overlap checks.
