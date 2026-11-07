# PS5 3.20 + 13.60 evidence investigation priorities

All records are unapproved. A missing direct source-text match is not proof of export absence.
Full live open-PR overlap, provider ownership and build checks remain mandatory.
Exact guest ABI is needed to claim returning behaviour, not to propose an explicitly provisional always-throwing import placeholder.

## Classification

| Status | Count |
|---|---:|
| historical_or_unqualified | 9452 |
| priority_candidates | 698 |
| source_symbol_already_observed | 8409 |
| source_symbol_in_other_provider | 2279 |

## Highest-volume libraries

| Library | Dual-source | 13.60-only | Total |
|---|---:|---:|---:|
| libSceNpCommon | 250 | 347 | 597 |
| libSceNKWebKit | 0 | 82 | 82 |
| libSceMediaFrameworkInterface | 0 | 13 | 13 |
| libSceAgc | 0 | 2 | 2 |
| libSceJsc | 0 | 2 | 2 |
| libSceNgs2 | 0 | 1 | 1 |
| libSceNpEntitlementAccess | 0 | 1 | 1 |

## Leading individual research targets

| Library | Symbol | NID | Source class | SDK header hint |
|---|---|---|---|---|
| libSceNpCommon | _ZThn16_N3sce2np9LocalFile5WriteEPNS0_6HandleEPKvmPm | +3ySpB1buMs | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClient4ctorEv | +EQNga+wsPc | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9WorkQueue4InitEPKcimm | +dGO+GS2ZXQ | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9HttpTrans11SendRequestEPNS0_6HandleEPKvm | +hKyaJJCE+0 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np12WorkerThreadD2Ev | +qB+WcQlMio | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClient7DestroyEv | +xvhXA8Ci4E | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np6ThreadC2Ev | 0f3ylOQJwqE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np4PathD0Ev | 0fwoTW7gqfM | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9LocalFile5WriteEPNS0_6HandleEPKvmPm | 0xL7AwgxphE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient19WaitRequestForAsyncEiij | 1ONFW86TETY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9WorkQueueD1Ev | 1QFKnDJxk3A | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np6Handle7DestroyEv | 1atFu71dFAU | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10CancelLockD2Ev | 1iHBAKrdE90 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np8SelectorD0Ev | 2HkOOhiWK3M | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np10JsonString5CloneEP16SceNpAllocatorEx | 2dAzrh4J0WY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9HttpTrans7DestroyEv | 2e9GLlHTKA4 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClient4dtorEv | 2h59YqPcrdM | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np12HttpTemplate6IsInitEv | 2mrb4euDuGY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np7Callout9IsStartedEv | 3ErXia+y89M | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np20BufferedStreamReader5CloseEv | 3Ku9r8b6gCg | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClientD0Ev | 3LuoWoXJ1WI | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np18HttpConnectionPoolD2Ev | 3MVW8+eWnjs | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9LocalFileD1Ev | 3eoh4hjcYag | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9WorkQueue4StopEv | 4DE+nnCVRPA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np13JsonDocParser5ParseEPKcm | 4nCyBD9jBus | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np18HttpConnectionPoolD0Ev | 5HWP63cOH+w | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np8Selector4InitEPKc | 5WuiSZkU3mg | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np6ThreadD2Ev | 6750DaF5Pas | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClientC1Ev | 6aKYLBS8Di8 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9HttpTrans16SetRequestHeaderEPKcS3_ | 6bYsRATI3tQ | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np8HttpFileD1Ev | 6fomUWNk6Xc | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np4Path11BuildAppendEPcmcPKcm | 6r6ssbPbKc4 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZThn8_N3sce2np10MemoryFileD0Ev | 7bzUdBtIQhE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClient10DisconnectEv | 7dyKpPHU+Yk | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient18EndRequestForAsyncEii | 8TpAxZoLLRw | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10EventQueueD2Ev | 8kUkQPQP7bA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClientD1Ev | 90XdvAqFFn8 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np18HttpConnectionPool6IsInitEv | 9cJ2S8f4Mj4 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10JsonParser4InitEPK7JsonDefPNS1_12EventHandlerE | AGadQiCfKDY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np4Path6SetStrEPKcm | AcG6blobOQE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np10JsonNumber6GetNumEPl | Agsyrf4L8uA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10JsonParserD2Ev | AvvE5A5A6ZA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9JsonValue13GetFieldValueEPKc | BDie4qEtKuA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient17invokeInitServiceEi | BJCXJJCi0Zc | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np8JsonBool7GetBoolEv | Bd7bMuLrAqE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np7CalloutC2EPNS0_14CalloutContextE | Bpay3NjseSU | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np4Path5ClearEv | BqFx1VLEMPk | dual_3.20_and_13.60 | none |
| libSceNpCommon | _sceNpAllocatorFree | BztTl7QeYqE | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np14CalloutContext7DestroyEv | C282U0P6Nwg | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np3ipc17ServiceIpmiClient6IsInitEv | C8SMKrvRkl8 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10JsonParser5ParseEPKcm | CDzSgHA6hWg | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np10JsonNumber5CloneEP16SceNpAllocatorEx | COxqqhvLSyM | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9WorkQueue6IsInitEv | CznMfhTIvVY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10JsonObject5ClearEv | DiHxx2k5zfM | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np9JsonArray5CloneEP16SceNpAllocatorEx | EcboqmwkrMY | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9HttpTrans12RecvResponseEPNS0_6HandleEPvmPm | EhLaOnhdcXo | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10MemoryFile4ReadEPNS0_6HandleEPvmPm | EyhtbPFMWNA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient11findServiceEi | F2xYmg5DiR4 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np8JsonBool7SetBoolEb | FdpYFbq5C3Q | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9JsonValueD2Ev | FfSNfBmn+K8 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9LocalFile4SeekEliPl | Flyyg6hzUOM | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClientC1Ev | FubuBXanVWk | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np7CalloutD0Ev | Fx2UwoQVVmo | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZThn8_N3sce2np9HttpTrans4ReadEPNS0_6HandleEPvmPm | G+v692ul7MA | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient11InitServiceEi | G4FYQtsjOX0 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZNK3sce2np10JsonNumber9GetNumStrEv | GAGrrgl7GAU | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZThn16_N3sce2np9HttpTransD1Ev | GG1Y+vBUkdU | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZThn8_N3sce2np9LocalFileD0Ev | Gh35wbyg4U8 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9HttpTransC2EP16SceNpAllocatorEx | HEeXBdgvJI4 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np9LocalFileC2Ev | HP4jsVYqBKg | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np8WorkItemC2EPKc | HldN461O2Dw | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc17ServiceIpmiClient7DestroyEv | IGngArGbzHo | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np20BufferedStreamReader4ReadEPNS0_6HandleEPvmPm | INZSjlRcuyQ | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np10Cancelable11CheckCancelEPKciS3_ | IwDQAbQxvD0 | dual_3.20_and_13.60 | none |
| libSceNpCommon | _ZN3sce2np3ipc10IpmiClientD2Ev | J1lpiTKAEuk | dual_3.20_and_13.60 | none |

None of these are independently validated as guest ABI. Public SDK header names
and 3.20 forwarding entries do not establish the correct guest ABI or behaviour.
Merged upstream precedents #10068, #9990 and #9695 permit provisional parameterless throwing exports; all still require complete live overlap checks.
