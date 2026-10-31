# Coverage matrices

All figures come from the canonical inventory and generated source observations. A known function is not necessarily a working function.

**Last refresh:** 2026-10-31T00:49:18+00:00 (scheduled polling, not instantaneous).

## A. Discovery

| Stage | Count | Meaning |
|---|---:|---|
| Indexed | 314,038 | Known logical library/NID records |
| Confirmed 13 60 | 302,338 | Recorded as exports in the extraction labeled firmware 13.60 |
| Historical only | 11,700 | Known from 3.20 evidence, not established for 13.60 |
| Published named | 47,085 | Records with a published proposed/recovered name |
| Strictly verified names | 39,966 | Name and status pass a strict NID recomputation check |
| Named pending strict check | 7,119 | Named records not passing the strict status/hash gate |
| Unnamed or withheld | 266,953 | No published name associated with the record |
| Publication withheld | 2 | Explicitly withheld by the publication filter |
| Conflicted flagged | 0 | Explicit conflict status in canonical inventory |

## B. Per-library source comparison

3.20 references are registered forwarders, not necessarily 13.60 exports. Open-PR counts are only observed matches; absence is not clearance.

| Library | 13.60 exports | 3.20 references | Named | Strict verified | AnyPS5 main definitions | Open PR matches (partial) | Unnamed |
|---|---:|---:|---:|---:|---:|---:|---:|
| SystemReactiveLinq | 26,351 | 0 | 0 | 0 | 0 | 0 | 26,351 |
| mscorlib | 23,708 | 312 | 375 | 312 | 0 | 0 | 23,335 |
| SystemCore | 19,731 | 0 | 0 | 0 | 0 | 0 | 19,731 |
| libSceNKWebKit | 15,665 | 10,135 | 12,110 | 10,271 | 7,336 | 0 | 6,829 |
| ScePlayStationPUI | 17,872 | 0 | 0 | 0 | 0 | 0 | 17,872 |
| ReactNativePUI | 10,924 | 0 | 0 | 0 | 0 | 0 | 10,924 |
| System | 10,621 | 0 | 0 | 0 | 0 | 0 | 10,621 |
| SystemXml | 8,583 | 0 | 0 | 0 | 0 | 0 | 8,583 |
| SystemData | 8,388 | 0 | 0 | 0 | 0 | 0 | 8,388 |
| SceVshShellUILegacy | 7,981 | 0 | 0 | 0 | 0 | 0 | 7,981 |
| ReactNativeModulesVsh | 6,713 | 0 | 0 | 0 | 0 | 0 | 6,713 |
| SceVshShellUIReactNativeShellApp | 6,391 | 0 | 0 | 0 | 0 | 0 | 6,391 |
| app | 5,612 | 0 | 0 | 0 | 0 | 0 | 5,612 |
| libSceJsc | 4,439 | 3,491 | 4,115 | 3,493 | 84 | 313 | 1,331 |
| SceVshShellUILoginMgr | 4,550 | 0 | 0 | 0 | 0 | 0 | 4,550 |
| ReactivePropertyPlayStation | 4,457 | 0 | 0 | 0 | 0 | 0 | 4,457 |
| NewtonsoftJsonPlayStation | 4,016 | 0 | 0 | 0 | 0 | 0 | 4,016 |
| SceVshShellUIIme | 3,932 | 0 | 0 | 0 | 0 | 0 | 3,932 |
| SceVshShellUICaptureMenu | 3,395 | 0 | 0 | 0 | 0 | 0 | 3,395 |
| SystemRuntimeSerialization | 3,384 | 0 | 0 | 0 | 0 | 0 | 3,384 |
| SceVshShellUIBroadcast | 2,986 | 0 | 0 | 0 | 0 | 0 | 2,986 |
| libSceLibcInternal | 2,688 | 0 | 2,679 | 2,282 | 11 | 0 | 9 |
| SystemServiceModel | 2,674 | 0 | 0 | 0 | 0 | 0 | 2,674 |
| SystemDataServicesClient | 2,636 | 0 | 0 | 0 | 0 | 0 | 2,636 |
| SystemComponentModelComposition | 2,592 | 0 | 0 | 0 | 0 | 0 | 2,592 |
| SceVshShellUIReactNativeApps | 2,343 | 0 | 0 | 0 | 0 | 0 | 2,343 |
| SystemReactiveCore | 2,335 | 0 | 0 | 0 | 0 | 0 | 2,335 |
| SceVshMessagesAccessor | 2,315 | 0 | 0 | 0 | 0 | 0 | 2,315 |
| SceVshShellUIAppSystem | 2,246 | 0 | 0 | 0 | 0 | 0 | 2,246 |
| SceVshShellUISystemModalDialog | 2,235 | 0 | 0 | 0 | 0 | 0 | 2,235 |
| SceVshAccessorDb | 2,219 | 0 | 0 | 0 | 0 | 0 | 2,219 |
| ReactNativeModulesVshTrophy | 2,177 | 0 | 0 | 0 | 0 | 0 | 2,177 |
| SystemServiceModelInternals | 2,044 | 0 | 0 | 0 | 0 | 0 | 2,044 |
| ScePlayStationCore | 1,830 | 0 | 0 | 0 | 0 | 0 | 1,830 |
| SceVshNpTrophyAccessor | 1,791 | 0 | 0 | 0 | 0 | 0 | 1,791 |
| MicrosoftCSharp | 1,739 | 0 | 0 | 0 | 0 | 0 | 1,739 |
| SceVshDiscordAccessor | 1,726 | 0 | 0 | 0 | 0 | 0 | 1,726 |
| libicu | 0 | 1,460 | 1,698 | 1,460 | 0 | 0 | 0 |
| websocketsharp | 1,560 | 0 | 0 | 0 | 0 | 0 | 1,560 |
| libkernel | 1,511 | 0 | 1,357 | 1,147 | 263 | 0 | 154 |
| SceVshUILib | 1,424 | 0 | 0 | 0 | 0 | 0 | 1,424 |
| SystemXmlLinq | 1,327 | 0 | 0 | 0 | 0 | 0 | 1,327 |
| SceVshShellUIBGLayer | 1,311 | 0 | 0 | 0 | 0 | 0 | 1,311 |
| SystemNetHttp | 1,283 | 0 | 0 | 0 | 0 | 0 | 1,283 |
| SceVshUserServiceWrapper | 1,272 | 0 | 0 | 0 | 0 | 0 | 1,272 |
| libSceNpCommon | 1,199 | 652 | 1,187 | 1,026 | 331 | 629 | 12 |
| SceVshShellUIVoiceAndAgent | 1,189 | 0 | 0 | 0 | 0 | 0 | 1,189 |
| SystemWebServices | 1,100 | 0 | 0 | 0 | 0 | 0 | 1,100 |
| libmonosgen | 1,087 | 0 | 937 | 796 | 0 | 0 | 150 |
| ReactNativeModulesVshMedia | 1,058 | 0 | 0 | 0 | 0 | 0 | 1,058 |
| SceVshVoiceAndAgent | 1,050 | 0 | 0 | 0 | 0 | 0 | 1,050 |
| SceVshLx | 1,022 | 0 | 0 | 0 | 0 | 0 | 1,022 |
| ReactNativeVshCommon | 990 | 0 | 0 | 0 | 0 | 0 | 990 |
| SceVshShellUIQuickImageEdit | 981 | 0 | 0 | 0 | 0 | 0 | 981 |
| libmonosgen-2.0 | 0 | 817 | 963 | 817 | 0 | 0 | 0 |
| MonoDataSqlite | 898 | 0 | 0 | 0 | 0 | 0 | 898 |
| libSceIcu | 298 | 556 | 813 | 692 | 0 | 60 | 42 |
| SceVshShellUIVisionRecognition | 822 | 0 | 0 | 0 | 0 | 0 | 822 |
| ReactNativeComponentsVsh | 820 | 0 | 0 | 0 | 0 | 0 | 820 |
| libdiscord | 802 | 0 | 0 | 0 | 0 | 0 | 802 |
| SceVshSQLite | 779 | 0 | 0 | 0 | 0 | 0 | 779 |
| SystemIOCompression | 739 | 0 | 0 | 0 | 0 | 0 | 739 |
| MonoSecurity | 700 | 0 | 0 | 0 | 0 | 0 | 700 |
| libSceUserService | 651 | 386 | 579 | 486 | 17 | 0 | 114 |
| libSceLibreSSl3 | 665 | 421 | 641 | 554 | 0 | 0 | 24 |
| SceVshOrbisContentManager | 594 | 0 | 0 | 0 | 0 | 0 | 594 |
| SceVshShellUIUgc | 591 | 0 | 0 | 0 | 0 | 0 | 591 |
| SceVshShellUICaptureContentUtil | 574 | 0 | 0 | 0 | 0 | 0 | 574 |
| ReactNativeModulesVshWebAppLauncher | 562 | 0 | 0 | 0 | 0 | 0 | 562 |
| libSceFollyShared | 555 | 0 | 128 | 103 | 0 | 0 | 427 |
| SceVshShellUIShareVideoTranscoder | 544 | 0 | 0 | 0 | 0 | 0 | 544 |
| libSceNpManager | 535 | 348 | 413 | 367 | 179 | 0 | 126 |
| SceVshGlsNativeCall | 532 | 0 | 0 | 0 | 0 | 0 | 532 |
| SceVshSysBridge | 532 | 0 | 0 | 0 | 0 | 0 | 532 |
| SceVshShellCoreUtilWrapper | 516 | 0 | 0 | 0 | 0 | 0 | 516 |
| libSceSystemService | 116 | 416 | 509 | 421 | 421 | 0 | 7 |
| ScePlayStationJson | 493 | 0 | 0 | 0 | 0 | 0 | 493 |
| SceVshShellUIProfileCache | 492 | 0 | 0 | 0 | 0 | 0 | 492 |
| libSceLibreSsl3 | 0 | 421 | 488 | 421 | 0 | 0 | 0 |
| ScePlayStationIme | 461 | 0 | 0 | 0 | 0 | 0 | 461 |
| libSceFsInternalForVsh | 431 | 155 | 309 | 266 | 155 | 0 | 137 |
| SceVshShellUILoginMgrWrapper | 444 | 0 | 0 | 0 | 0 | 0 | 444 |
| SceVshProfileCache | 438 | 0 | 0 | 0 | 0 | 0 | 438 |
| SceVshAppInstUtilWrapper | 433 | 0 | 0 | 0 | 0 | 0 | 433 |
| SystemComponentModelDataAnnotations | 432 | 0 | 0 | 0 | 0 | 0 | 432 |
| ReactNativeModulesVshPSNowPlayer | 421 | 0 | 0 | 0 | 0 | 0 | 421 |
| libSceLibreSSL | 414 | 343 | 414 | 357 | 5 | 0 | 0 |
| libwebrtc | 412 | 0 | 352 | 293 | 0 | 0 | 60 |
| SystemNumerics | 411 | 0 | 0 | 0 | 0 | 0 | 411 |
| libSceLibreSsl | 0 | 343 | 399 | 343 | 5 | 0 | 0 |
| SceVshShellUITheme | 396 | 0 | 0 | 0 | 0 | 0 | 396 |
| SceVshShellUIBaseSystem | 392 | 0 | 0 | 0 | 0 | 0 | 392 |
| libNativeExtensions | 386 | 33 | 111 | 91 | 0 | 0 | 281 |
| SceVshShellUISticker | 356 | 0 | 0 | 0 | 0 | 0 | 356 |
| MonoDataTds | 348 | 0 | 0 | 0 | 0 | 0 | 348 |
| libSceFreeType | 344 | 0 | 344 | 283 | 0 | 0 | 0 |
| libSceFreeTypeOl | 0 | 283 | 344 | 283 | 0 | 0 | 0 |
| libSceFreeTypeOt | 0 | 280 | 341 | 280 | 0 | 0 | 0 |
| ScePlayStationOrbis | 337 | 0 | 0 | 0 | 0 | 0 | 337 |
| SceVshTheme | 334 | 0 | 0 | 0 | 0 | 0 | 334 |
| SystemServiceModelWeb | 334 | 0 | 0 | 0 | 0 | 0 | 334 |
| libbdj | 301 | 0 | 255 | 228 | 0 | 0 | 46 |
| SceVshNpManager | 300 | 0 | 0 | 0 | 0 | 0 | 300 |
| libjvm | 295 | 0 | 153 | 126 | 0 | 0 | 142 |
| SceVshShellUIStickerAccessor | 291 | 0 | 0 | 0 | 0 | 0 | 291 |
| SceVshResourceArbitrator | 287 | 0 | 0 | 0 | 0 | 0 | 287 |
| SceVshShellUIQuickVideoEdit | 276 | 0 | 0 | 0 | 0 | 0 | 276 |
| libSceHmd2 | 276 | 4 | 161 | 132 | 67 | 0 | 115 |
| libSceCes | 274 | 0 | 274 | 230 | 0 | 0 | 0 |
| libSceCesCs | 0 | 230 | 273 | 230 | 230 | 0 | 0 |
| ReactNativeComponentsVshPSNowPlayer | 271 | 0 | 0 | 0 | 0 | 0 | 271 |
| SceVshUsbStorageScene | 265 | 0 | 0 | 0 | 0 | 0 | 265 |
| libSceJsi-0.70 | 265 | 0 | 0 | 0 | 0 | 0 | 265 |
| libAacs | 264 | 0 | 13 | 13 | 0 | 0 | 251 |
| SceFacebookCSSLayout | 263 | 0 | 0 | 0 | 0 | 0 | 263 |
| SceVshVideoPlayer | 262 | 0 | 0 | 0 | 0 | 0 | 262 |
| libjava | 262 | 0 | 177 | 146 | 0 | 0 | 85 |
| libSceShellCoreUtil | 260 | 0 | 237 | 193 | 0 | 0 | 23 |
| SceVshDbPreparationWrapper | 249 | 0 | 0 | 0 | 0 | 0 | 249 |
| libSceAgc | 248 | 170 | 243 | 208 | 200 | 0 | 5 |
| SceVshNpWebapi | 246 | 0 | 0 | 0 | 0 | 0 | 246 |
| libSceAgcVsh | 245 | 170 | 239 | 204 | 0 | 0 | 6 |
| libSceFont | 240 | 113 | 240 | 201 | 201 | 0 | 0 |
| libSceVideoOut | 226 | 136 | 199 | 166 | 148 | 1 | 38 |
| libSceNet | 233 | 180 | 223 | 188 | 182 | 0 | 12 |
| libSceMediaFrameworkInterface | 225 | 0 | 139 | 120 | 0 | 107 | 86 |
| libSceGLSlimVSH | 217 | 170 | 208 | 175 | 7 | 0 | 9 |
| libSceJson2 | 215 | 184 | 215 | 184 | 126 | 0 | 0 |
| libSceNKWebKitRequirements | 177 | 109 | 142 | 114 | 0 | 0 | 72 |
| libScePad | 212 | 87 | 194 | 173 | 164 | 0 | 18 |
| libmono-btls-shared | 212 | 0 | 205 | 181 | 0 | 0 | 7 |
| SceVshIme | 211 | 0 | 0 | 0 | 0 | 0 | 211 |
| SceVshNpWebapi2 | 208 | 0 | 0 | 0 | 0 | 0 | 208 |
| SceVshShellUIVoiceChat | 208 | 0 | 0 | 0 | 0 | 0 | 208 |
| SceVshSl2Sl2Client | 204 | 0 | 0 | 0 | 0 | 0 | 204 |
| SceVshAutoMounterWrapper | 197 | 0 | 0 | 0 | 0 | 0 | 197 |
| SceVshDiscPlayer | 197 | 0 | 0 | 0 | 0 | 0 | 197 |
| SceVshMimeType | 197 | 0 | 0 | 0 | 0 | 0 | 197 |
| libScePosix | 197 | 0 | 197 | 164 | 0 | 0 | 0 |
| SceVshSaveDataWrapper | 195 | 0 | 0 | 0 | 0 | 0 | 195 |
| libSceGLSlimServerVSH | 192 | 0 | 190 | 157 | 0 | 0 | 2 |
| libmdbg_syscore | 187 | 123 | 148 | 127 | 127 | 0 | 43 |
| ReactNativeModulesVshMediaPlayerContents | 189 | 0 | 0 | 0 | 0 | 0 | 189 |
| libSceHmd | 178 | 144 | 168 | 145 | 145 | 0 | 18 |
| libSceAppInstUtil | 173 | 88 | 132 | 112 | 112 | 0 | 52 |
| libSceXml | 183 | 156 | 183 | 156 | 128 | 28 | 0 |
| SceVshSystemLoggerWrapper | 182 | 0 | 0 | 0 | 0 | 0 | 182 |
| SceVshNpAsm | 181 | 0 | 0 | 0 | 0 | 0 | 181 |
| libSceAvSetting | 175 | 90 | 128 | 109 | 109 | 0 | 52 |
| SceVshUpdateServiceWrapper | 178 | 0 | 0 | 0 | 0 | 0 | 178 |
| libSceGnmDriver | 168 | 141 | 163 | 141 | 0 | 0 | 12 |
| SceVshAppDbWrapper | 173 | 0 | 0 | 0 | 0 | 0 | 173 |
| libfreetype | 0 | 141 | 169 | 141 | 0 | 0 | 0 |
| libprospero_wrapper | 169 | 0 | 64 | 53 | 0 | 0 | 105 |
| libSceFios2 | 0 | 141 | 168 | 141 | 141 | 0 | 0 |
| SceVshNpRifManager | 166 | 0 | 0 | 0 | 0 | 0 | 166 |
| libcairo | 166 | 141 | 161 | 141 | 0 | 0 | 5 |
| libSceGnmDriverForNeoMode | 0 | 141 | 163 | 141 | 104 | 0 | 0 |
| libSceFacebook.Yoga | 133 | 114 | 138 | 117 | 0 | 0 | 20 |
| libnio | 157 | 0 | 2 | 2 | 0 | 0 | 155 |
| libSceAbstractStorage | 119 | 91 | 110 | 91 | 0 | 0 | 45 |
| libgnmawt | 153 | 0 | 146 | 122 | 0 | 0 | 7 |
| SceVshDbShared | 149 | 0 | 0 | 0 | 0 | 0 | 149 |
| SceVshKernelSysWrapper | 148 | 0 | 0 | 0 | 0 | 0 | 148 |
| libSceMbus | 111 | 102 | 131 | 112 | 112 | 0 | 12 |
| libSceNpTus | 142 | 127 | 142 | 127 | 127 | 0 | 0 |
| libSceAudioOut | 77 | 107 | 132 | 114 | 112 | 0 | 7 |
| libReactNative.Modules.Vsh.WebAppLauncher | 138 | 41 | 135 | 113 | 0 | 0 | 3 |
| libSceAudioOut2 | 138 | 0 | 84 | 79 | 0 | 0 | 54 |
| libSceComposite | 123 | 67 | 101 | 87 | 87 | 0 | 37 |
| libSceFont.native | 0 | 113 | 136 | 113 | 0 | 0 | 0 |
| libSceJxr | 136 | 2 | 136 | 111 | 0 | 0 | 0 |
| libSceAgcDriver | 119 | 82 | 130 | 113 | 103 | 0 | 5 |
| libSceCustomMusicSysCallWrapper | 133 | 1 | 54 | 48 | 1 | 47 | 79 |
| gaikai_player_lib | 132 | 0 | 16 | 15 | 0 | 0 | 116 |
| SceVshOrbisBgft | 127 | 0 | 0 | 0 | 0 | 0 | 127 |
| libSceCamera | 93 | 105 | 122 | 110 | 110 | 0 | 5 |
| libSceSaveData | 123 | 82 | 105 | 89 | 0 | 0 | 18 |
| SceVshNpUds | 122 | 0 | 0 | 0 | 0 | 0 | 122 |
| SystemNetHttpWebRequest | 122 | 0 | 0 | 0 | 0 | 0 | 122 |
| libReactNative.Modules.Vsh | 122 | 60 | 87 | 71 | 0 | 0 | 35 |
| libSceAmpr | 118 | 76 | 118 | 99 | 99 | 0 | 0 |
| libScePsm | 118 | 54 | 65 | 54 | 54 | 0 | 53 |
| libSceHttp | 115 | 91 | 115 | 91 | 90 | 0 | 0 |
| ScePlayStationOrbisSpeech | 113 | 0 | 0 | 0 | 0 | 0 | 113 |
| libSceNpTrophy | 110 | 84 | 104 | 88 | 88 | 0 | 6 |
| SceVshNpTrophy2 | 109 | 0 | 0 | 0 | 0 | 0 | 109 |
| SceVshDataTransfer | 108 | 0 | 0 | 0 | 0 | 0 | 108 |
| SceVshLncUtilWrapper | 107 | 0 | 0 | 0 | 0 | 0 | 107 |
| libhermes-0.11 | 107 | 0 | 0 | 0 | 0 | 0 | 107 |
| SceVshNpTmdb | 105 | 0 | 0 | 0 | 0 | 0 | 105 |
| libSceAbstractYoutube | 76 | 66 | 76 | 66 | 0 | 0 | 27 |
| libScePlayReady4 | 102 | 70 | 89 | 74 | 34 | 0 | 14 |
| libSceNpUtility | 102 | 85 | 100 | 88 | 85 | 0 | 2 |
| libSceBgft | 82 | 74 | 96 | 80 | 80 | 0 | 5 |
| SceVshNpTrophy | 100 | 0 | 0 | 0 | 0 | 0 | 100 |
| libSceAbstractLocal | 70 | 61 | 70 | 61 | 0 | 0 | 30 |
| libSceNetCtl | 57 | 88 | 96 | 89 | 80 | 0 | 3 |
| libSceIpmi | 92 | 79 | 94 | 79 | 46 | 0 | 3 |
| libScePlayReady4L | 96 | 0 | 88 | 73 | 0 | 0 | 8 |
| SceVshPsnUtil | 94 | 0 | 0 | 0 | 0 | 0 | 94 |
| libSceNpWebApi | 94 | 50 | 56 | 50 | 44 | 0 | 38 |
| libSceLncUtil | 93 | 0 | 89 | 70 | 0 | 0 | 4 |
| libSceNpUniversalDataSystem | 61 | 72 | 93 | 80 | 80 | 0 | 0 |
| libcurl | 93 | 75 | 85 | 75 | 0 | 0 | 8 |
| libpng16 | 0 | 76 | 93 | 76 | 0 | 0 | 0 |
| SceVshSysUtilWrapper | 92 | 0 | 0 | 0 | 0 | 0 | 92 |
| libSceAbstractTwitter | 68 | 60 | 68 | 60 | 0 | 0 | 24 |
| libSceVrTracker2 | 92 | 4 | 51 | 42 | 9 | 0 | 41 |
| SceVshOrbisAbstractStorage | 91 | 0 | 0 | 0 | 0 | 0 | 91 |
| libSceDataTransfer | 45 | 51 | 88 | 75 | 75 | 0 | 0 |
| libSceJson | 88 | 74 | 88 | 74 | 0 | 0 | 0 |
| libSceVnaInternal | 88 | 0 | 84 | 71 | 0 | 71 | 4 |
| libSceRegMgr | 86 | 56 | 66 | 59 | 58 | 0 | 21 |
| libSceSysCore | 87 | 64 | 79 | 68 | 68 | 0 | 8 |
| SystemIOCompressionFileSystem | 86 | 0 | 0 | 0 | 0 | 0 | 86 |
| libnet | 84 | 0 | 61 | 57 | 0 | 0 | 23 |
| libSceHidControl | 81 | 18 | 68 | 57 | 57 | 0 | 14 |
| libSceMetadataReaderWriter | 64 | 33 | 39 | 33 | 33 | 0 | 42 |
| SystemTransactions | 79 | 0 | 0 | 0 | 0 | 0 | 79 |
| libSceCompositeExt | 0 | 67 | 78 | 67 | 0 | 0 | 0 |
| libwvoec | 77 | 0 | 0 | 0 | 0 | 0 | 77 |
| libSceVideoStreamingEngine | 74 | 12 | 70 | 58 | 58 | 0 | 4 |
| libReactNative.Modules.Vsh.Media | 66 | 42 | 55 | 45 | 0 | 0 | 18 |
| libSceUpdateService | 70 | 32 | 50 | 40 | 40 | 0 | 23 |
| I18N | 72 | 0 | 0 | 0 | 0 | 0 | 72 |
| libSceAcm | 72 | 9 | 23 | 21 | 21 | 0 | 49 |
| libSceHttp2 | 72 | 44 | 71 | 55 | 54 | 0 | 1 |
| SceVshRemotePlay | 71 | 0 | 0 | 0 | 0 | 0 | 71 |
| libSceVshFreeType | 71 | 0 | 65 | 54 | 0 | 0 | 6 |
| libSceVshPng | 70 | 0 | 67 | 56 | 0 | 0 | 3 |
| libSceNpMatching2 | 69 | 61 | 69 | 61 | 61 | 0 | 0 |
| libSceUsbStorageForShellUI | 69 | 0 | 21 | 18 | 0 | 0 | 48 |
| SceVshVideoRecordingWrapper | 68 | 0 | 0 | 0 | 0 | 0 | 68 |
| SceVshAccessorDbMediaEventListener | 66 | 0 | 0 | 0 | 0 | 0 | 66 |
| libSceNgs2 | 66 | 36 | 66 | 54 | 2 | 0 | 0 |
| SceVshNpGameIntent | 65 | 0 | 0 | 0 | 0 | 0 | 65 |
| libCss | 65 | 0 | 4 | 4 | 0 | 0 | 61 |
| libSceNgs2.native | 0 | 53 | 65 | 53 | 51 | 0 | 0 |
| libSceUlt | 64 | 53 | 64 | 53 | 47 | 0 | 0 |
| libSceUsbd | 63 | 47 | 61 | 47 | 47 | 0 | 2 |
| libSceVisionManager | 63 | 46 | 56 | 46 | 46 | 0 | 7 |
| SceVshRnpsAppMgrWrapper | 62 | 0 | 0 | 0 | 0 | 0 | 62 |
| libSceEsvmEngine | 61 | 16 | 56 | 50 | 50 | 0 | 6 |
| libSceIme | 61 | 41 | 59 | 46 | 44 | 0 | 2 |
| I18NCJK | 59 | 0 | 0 | 0 | 0 | 0 | 59 |
| libSceAvcap2 | 59 | 0 | 42 | 35 | 35 | 0 | 17 |
| libSceSsl | 57 | 41 | 55 | 42 | 41 | 0 | 2 |
| libSceNpTrophy2 | 56 | 39 | 56 | 45 | 45 | 0 | 0 |
| libScePlayReady2 | 52 | 46 | 56 | 47 | 14 | 0 | 0 |
| SceVshRegistry | 54 | 0 | 0 | 0 | 0 | 0 | 54 |
| libSceAjm | 54 | 19 | 46 | 42 | 3 | 0 | 8 |
| libCFWML | 53 | 0 | 0 | 0 | 0 | 0 | 53 |
| libSceWebTransport | 53 | 0 | 0 | 0 | 0 | 0 | 53 |
| libfontconfig | 53 | 41 | 53 | 41 | 0 | 0 | 0 |
| ScePlayStationSpeechSystemTts | 52 | 0 | 0 | 0 | 0 | 0 | 52 |
| SceVshWebBrowser | 52 | 0 | 0 | 0 | 0 | 0 | 52 |
| SceVshShareLibWrapper | 51 | 0 | 0 | 0 | 0 | 0 | 51 |
| SceVshSl2Sl2Common | 51 | 0 | 0 | 0 | 0 | 0 | 51 |
| libSceNpScore | 51 | 0 | 51 | 42 | 0 | 0 | 0 |
| libSceNpScoreRanking | 0 | 42 | 51 | 42 | 42 | 0 | 0 |
| libSceVideoOut_nosubmission | 51 | 0 | 31 | 25 | 0 | 0 | 20 |
| libSceVshHarfBuzz | 51 | 0 | 35 | 32 | 0 | 0 | 16 |
| SceVshBackupRestoreUtil | 50 | 0 | 0 | 0 | 0 | 0 | 50 |
| SceVshPadControllerUpdWrapper | 50 | 0 | 0 | 0 | 0 | 0 | 50 |
| libScePlayReady | 50 | 43 | 50 | 43 | 43 | 0 | 0 |
| libSceAudioIn | 43 | 34 | 48 | 38 | 33 | 0 | 1 |
| libSceRemoteplay | 49 | 32 | 48 | 38 | 37 | 0 | 1 |
| libSceSpSysCallWrapper | 48 | 40 | 48 | 40 | 40 | 0 | 0 |
| libSceVideoRecordingP | 48 | 0 | 43 | 39 | 18 | 0 | 5 |
| libSceGameLiveStreaming | 45 | 42 | 47 | 42 | 42 | 0 | 0 |
| libSceRtc | 47 | 38 | 47 | 38 | 38 | 0 | 0 |
| libSceVideoCoreServerInterface | 47 | 43 | 47 | 43 | 43 | 0 | 0 |
| I18NRare | 46 | 0 | 0 | 0 | 0 | 0 | 46 |
| SceVshMorpheusUpdWrapper | 46 | 0 | 0 | 0 | 0 | 0 | 46 |
| SceVshAccessorDbNotify | 45 | 0 | 0 | 0 | 0 | 0 | 45 |
| libSceAgcDriverPaDebug | 45 | 0 | 23 | 15 | 0 | 0 | 22 |
| libSceEsvm | 45 | 0 | 45 | 39 | 39 | 0 | 0 |
| libSceLoginMgrServer | 45 | 28 | 32 | 30 | 30 | 0 | 13 |
| libSceCdlgUtilServer | 44 | 10 | 11 | 10 | 10 | 0 | 33 |
| libSceNpTusCompat | 44 | 0 | 44 | 41 | 0 | 0 | 0 |
| libSceAjmi | 22 | 19 | 22 | 20 | 0 | 1 | 21 |
| libSceNpWebApi2 | 43 | 36 | 41 | 38 | 36 | 0 | 2 |
| SceVshMyGameList | 42 | 0 | 0 | 0 | 0 | 0 | 42 |
| libSceRazorCpu | 42 | 31 | 42 | 35 | 35 | 0 | 0 |
| libSceAppDbShellCoreClient | 41 | 0 | 0 | 0 | 0 | 0 | 41 |
| libSceAudioPropagation | 41 | 23 | 33 | 27 | 27 | 0 | 8 |
| libSceSaveData_native | 40 | 0 | 39 | 35 | 0 | 0 | 1 |
| libSceDepth | 39 | 35 | 38 | 35 | 35 | 0 | 1 |
| libSceAjm.native | 0 | 35 | 38 | 35 | 35 | 0 | 0 |
| libSceAppContent | 32 | 29 | 38 | 32 | 30 | 0 | 0 |
| libScePosixForWebKit | 38 | 29 | 38 | 31 | 13 | 0 | 0 |
| libSceMusicFrameworkInterface | 37 | 17 | 36 | 28 | 28 | 0 | 1 |
| libSceVoiceChat | 37 | 26 | 34 | 29 | 28 | 0 | 3 |
| libharfbuzz | 0 | 33 | 37 | 33 | 0 | 0 | 0 |
| libkernel_psmkit | 37 | 0 | 37 | 26 | 0 | 0 | 0 |
| SceVshUrlConfigResolver | 36 | 0 | 0 | 0 | 0 | 0 | 36 |
| libCprm | 35 | 0 | 0 | 0 | 0 | 0 | 35 |
| libSceHttpCache | 34 | 21 | 28 | 26 | 25 | 0 | 7 |
| libSceRnpsAppMgr | 30 | 21 | 35 | 28 | 28 | 0 | 0 |
| libSceRudp | 35 | 30 | 35 | 31 | 31 | 0 | 0 |
| libSceVoice | 35 | 31 | 35 | 32 | 31 | 0 | 0 |
| SceVshAccessor | 34 | 0 | 0 | 0 | 0 | 0 | 34 |
| SceVshNpAppInfo | 34 | 0 | 0 | 0 | 0 | 0 | 34 |
| libSceAvPlayerStreaming | 34 | 28 | 34 | 29 | 20 | 0 | 0 |
| libSceCamera2 | 34 | 0 | 34 | 28 | 0 | 0 | 0 |
| libSceCamera2_nosubmission | 34 | 0 | 34 | 28 | 0 | 0 | 0 |
| libSceSaveData.native | 0 | 30 | 34 | 30 | 30 | 0 | 0 |
| libSceVrTracker | 27 | 28 | 30 | 28 | 28 | 0 | 4 |
| libSceVsePlugin | 34 | 0 | 0 | 0 | 0 | 0 | 34 |
| libzip | 34 | 0 | 18 | 14 | 0 | 0 | 16 |
| SceVshPatchCheckerClientWrapper | 33 | 0 | 0 | 0 | 0 | 0 | 33 |
| libSceBemp2sys | 33 | 26 | 31 | 26 | 0 | 0 | 2 |
| libSceSystemStateMgr | 33 | 0 | 28 | 26 | 0 | 0 | 5 |
| SceVshVideoServiceWrapper | 32 | 0 | 0 | 0 | 0 | 0 | 32 |
| libSceAudio3d | 32 | 28 | 32 | 29 | 29 | 0 | 0 |
| libScePlayAreaEditor | 32 | 0 | 0 | 0 | 0 | 0 | 32 |
| libSceNpSessionSignaling | 31 | 21 | 31 | 26 | 26 | 0 | 0 |
| I18NOther | 30 | 0 | 0 | 0 | 0 | 0 | 30 |
| ScePlayStationBclExtensions | 30 | 0 | 0 | 0 | 0 | 0 | 30 |
| SceVshNpPapc | 30 | 0 | 0 | 0 | 0 | 0 | 30 |
| SceVshNpSns | 30 | 0 | 0 | 0 | 0 | 0 | 30 |
| SceVshSl2Sl2Manage | 30 | 0 | 0 | 0 | 0 | 0 | 30 |
| libSceAvPlayer | 30 | 23 | 30 | 24 | 23 | 0 | 0 |
| libSceOpusDec | 30 | 10 | 15 | 11 | 10 | 1 | 15 |
| ReactNativeModulesVshTelemetryNq | 29 | 0 | 0 | 0 | 0 | 0 | 29 |
| libSceAvPlayer.native | 0 | 23 | 29 | 23 | 1 | 0 | 0 |
| libSceVoiceCommand | 29 | 0 | 23 | 18 | 0 | 18 | 6 |
| SceVshNpSessionService | 28 | 0 | 0 | 0 | 0 | 0 | 28 |
| libSceCommonDialog | 28 | 14 | 16 | 14 | 2 | 0 | 12 |
| libSceKeyboard | 22 | 21 | 24 | 23 | 23 | 0 | 4 |
| libSceMbusDebug | 28 | 0 | 28 | 24 | 0 | 0 | 0 |
| libSceVrTracker2_nosubmission | 28 | 0 | 6 | 5 | 0 | 0 | 22 |
| libSceContentSearch | 19 | 17 | 27 | 21 | 21 | 0 | 0 |
| libSceImeBackend | 27 | 0 | 27 | 24 | 24 | 0 | 0 |
| libSceNetCtlApIpcInt | 27 | 0 | 18 | 16 | 0 | 0 | 9 |
| libScePsml | 27 | 0 | 19 | 15 | 0 | 0 | 8 |
| libSceSdma | 27 | 22 | 27 | 22 | 21 | 0 | 0 |
| libSceVdecCore | 27 | 15 | 25 | 18 | 16 | 0 | 2 |
| libSceVenc | 27 | 13 | 19 | 16 | 16 | 0 | 8 |
| SceVshShareServerPostWrapper | 26 | 0 | 0 | 0 | 0 | 0 | 26 |
| libSceNpEntitlementAccess | 25 | 23 | 26 | 25 | 23 | 1 | 0 |
| libSceNpParty | 26 | 19 | 26 | 19 | 19 | 0 | 0 |
| SceVshShellUIUtilWrapper | 25 | 0 | 0 | 0 | 0 | 0 | 25 |
| SceVshVoiceMsgVoiceMsgWrapper | 25 | 0 | 0 | 0 | 0 | 0 | 25 |
| libSceAudioOutServer | 25 | 0 | 2 | 2 | 0 | 0 | 23 |
| libSceGameLiveStreamingCompat | 25 | 0 | 25 | 20 | 0 | 0 | 0 |
| libSceMouse | 25 | 11 | 23 | 19 | 19 | 0 | 2 |
| libSceSharePlay | 25 | 15 | 21 | 17 | 17 | 0 | 4 |
| libSceVshJpeg | 25 | 0 | 25 | 21 | 0 | 0 | 0 |
| SceVshNpServiceChecker | 24 | 0 | 0 | 0 | 0 | 0 | 24 |
| libSceNpSignaling | 24 | 21 | 24 | 21 | 21 | 0 | 0 |
| libSceNpSns | 16 | 19 | 24 | 19 | 17 | 0 | 0 |
| libSceOpusCeltEnc | 24 | 8 | 15 | 11 | 11 | 0 | 9 |
| libScePlayGo | 22 | 15 | 24 | 18 | 18 | 0 | 0 |
| libSceSysUtil | 24 | 21 | 24 | 21 | 21 | 0 | 0 |
| libSceSystemGesture | 24 | 19 | 24 | 20 | 19 | 1 | 0 |
| libSceVdecCore.native | 0 | 17 | 24 | 17 | 2 | 0 | 0 |
| libSceVoiceQoS | 24 | 20 | 23 | 20 | 20 | 0 | 1 |
| SceVshNpIdMapper | 23 | 0 | 0 | 0 | 0 | 0 | 23 |
| SceVshShareVideoTranscoderWrapper | 23 | 0 | 0 | 0 | 0 | 0 | 23 |
| libkernel_jvm | 23 | 0 | 23 | 17 | 0 | 0 | 0 |
| I18NWest | 22 | 0 | 0 | 0 | 0 | 0 | 22 |
| libSceAudiodec | 22 | 8 | 22 | 18 | 7 | 0 | 0 |
| libSceShareUtility | 22 | 18 | 22 | 18 | 18 | 0 | 0 |
| libSceVnaWebsocket | 22 | 0 | 0 | 0 | 0 | 0 | 22 |
| SceVshErrorDialogUtilWrapper | 21 | 0 | 0 | 0 | 0 | 0 | 21 |
| SceVshNpPbtc | 21 | 0 | 0 | 0 | 0 | 0 | 21 |
| libSceAjm_legacy_nosubmission | 21 | 0 | 21 | 19 | 0 | 0 | 0 |
| libSceBackupRestoreUtil | 21 | 14 | 21 | 17 | 17 | 0 | 0 |
| libSceFontFt | 21 | 15 | 21 | 16 | 16 | 0 | 0 |
| libSceIdu | 21 | 7 | 17 | 15 | 15 | 0 | 4 |
| libSceMove | 21 | 16 | 21 | 16 | 16 | 0 | 0 |
| libSceUsbStorage | 11 | 19 | 21 | 19 | 19 | 0 | 0 |
| libSceVideodec2 | 21 | 18 | 21 | 21 | 8 | 0 | 0 |
| libSceAsyncStorageInternal | 20 | 0 | 0 | 0 | 0 | 0 | 20 |
| libSceAudiodec.native | 0 | 17 | 20 | 17 | 11 | 0 | 0 |
| SceVshCsbMgrWrapper | 19 | 0 | 0 | 0 | 0 | 0 | 19 |
| libSceBgsStorage | 19 | 0 | 0 | 0 | 0 | 0 | 19 |
| libSceContentListController | 19 | 0 | 18 | 16 | 16 | 0 | 1 |
| libSceNpGameIntent | 11 | 11 | 19 | 15 | 11 | 0 | 0 |
| libSceShareInternal | 19 | 0 | 12 | 10 | 0 | 0 | 7 |
| libSceSysmodule | 19 | 16 | 16 | 16 | 16 | 0 | 3 |
| SceVshAppContentUtilWrapper | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| SceVshNpCommon | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| SceVshNpServiceChecker2 | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| SceVshSQLiteAux | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| SceVshSysfileUtilWrapper | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| libSceBeisobmf | 18 | 16 | 18 | 16 | 0 | 0 | 0 |
| libSceCustomMusicCore | 0 | 17 | 18 | 17 | 17 | 0 | 0 |
| libSceM4aacEnc | 18 | 14 | 17 | 14 | 14 | 0 | 1 |
| libSceMoveTracker | 18 | 15 | 18 | 15 | 15 | 0 | 0 |
| libSceRemotePlayClientIpc | 18 | 0 | 6 | 6 | 6 | 0 | 12 |
| libSceTtsCoreG3Bc | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| libSceVdecsw | 18 | 14 | 18 | 14 | 14 | 0 | 0 |
| libSceVideoRecording.native | 0 | 17 | 18 | 17 | 0 | 0 | 0 |
| libjli | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| SceVshNpAppLaunchLink | 17 | 0 | 0 | 0 | 0 | 0 | 17 |
| SceVshNpAppLaunchLink2 | 17 | 0 | 0 | 0 | 0 | 0 | 17 |
| libSceBluetoothHid | 17 | 13 | 17 | 13 | 13 | 0 | 0 |
| libSceCompanionHttpd | 17 | 11 | 17 | 11 | 11 | 0 | 0 |
| libSceCoredump | 17 | 0 | 16 | 15 | 0 | 0 | 1 |
| libSceShare | 17 | 0 | 17 | 15 | 15 | 0 | 0 |
| libSceSystemServiceUsbStorage | 17 | 0 | 17 | 14 | 0 | 0 | 0 |
| SceVshNpPreorderMgr | 16 | 0 | 0 | 0 | 0 | 0 | 16 |
| gaikai-player | 0 | 15 | 16 | 15 | 0 | 0 | 0 |
| libSceSystemLogger2 | 16 | 4 | 11 | 9 | 9 | 0 | 5 |
| libSceVshWebP | 16 | 0 | 0 | 0 | 0 | 0 | 16 |
| libSceFiber | 15 | 13 | 15 | 13 | 11 | 0 | 0 |
| libSceOpusSilkEnc | 15 | 11 | 15 | 12 | 12 | 0 | 0 |
| libSceTEEClient | 15 | 10 | 11 | 10 | 0 | 0 | 4 |
| I18NMidEast | 14 | 0 | 0 | 0 | 0 | 0 | 14 |
| SceVshNpIga | 14 | 0 | 0 | 0 | 0 | 0 | 14 |
| libSceAudioSystem | 14 | 2 | 8 | 7 | 7 | 0 | 6 |
| libSceCffMgr | 14 | 0 | 7 | 7 | 7 | 0 | 7 |
| libSceContentExport | 13 | 11 | 14 | 11 | 11 | 0 | 0 |
| libSceGnmDriverPaDebug | 14 | 0 | 11 | 7 | 0 | 0 | 3 |
| libSceImeDialog | 14 | 11 | 14 | 12 | 12 | 0 | 0 |
| libSceNpAuth | 14 | 9 | 14 | 10 | 10 | 0 | 0 |
| libSceNpManagerCompat | 14 | 0 | 14 | 13 | 0 | 0 | 0 |
| libSceNpRemotePlaySessionSignaling | 14 | 8 | 14 | 11 | 11 | 0 | 0 |
| libSceResourceArbitrator | 14 | 0 | 6 | 5 | 5 | 0 | 8 |
| libSceScreenShot | 12 | 11 | 14 | 11 | 10 | 0 | 0 |
| libSceTextToSpeech2 | 14 | 0 | 14 | 13 | 13 | 0 | 0 |
| libSceUgcBgUploaderClient | 14 | 0 | 0 | 0 | 0 | 0 | 14 |
| libSceUgcServiceS3 | 14 | 0 | 4 | 4 | 4 | 0 | 10 |
| libSceVideoRecording | 14 | 13 | 14 | 13 | 0 | 0 | 0 |
| libSceAvSettingDebug | 13 | 0 | 8 | 7 | 0 | 0 | 5 |
| libSceAvcap2mvr | 13 | 0 | 0 | 0 | 0 | 0 | 13 |
| libSceImageUtil | 13 | 0 | 0 | 0 | 0 | 0 | 13 |
| libSceJemspace | 13 | 0 | 13 | 11 | 11 | 0 | 0 |
| libScePatchCheckerClient | 11 | 11 | 12 | 11 | 11 | 0 | 1 |
| libSceShare.native | 0 | 11 | 13 | 11 | 0 | 0 | 0 |
| libSceSrcUtl | 13 | 8 | 13 | 11 | 11 | 0 | 0 |
| libSceVdecShevc | 13 | 7 | 7 | 7 | 7 | 0 | 6 |
| libSceWebBrowserDialog | 13 | 12 | 13 | 12 | 12 | 0 | 0 |
| ScePlayStationIcu | 12 | 0 | 0 | 0 | 0 | 0 | 12 |
| SceVshDbRecoveryUtilityWrapper | 12 | 0 | 0 | 0 | 0 | 0 | 12 |
| SceVshNotificationClient | 12 | 0 | 0 | 0 | 0 | 0 | 12 |
| SceVshPartyCommon | 12 | 0 | 0 | 0 | 0 | 0 | 12 |
| libSceEsvmWidevine | 12 | 0 | 12 | 10 | 0 | 0 | 0 |
| libSceFlexContent | 12 | 0 | 7 | 7 | 7 | 0 | 5 |
| libSceFontGs | 12 | 0 | 8 | 7 | 2 | 0 | 4 |
| libSceNpCommerce | 12 | 9 | 12 | 10 | 10 | 0 | 0 |
| libSceNpWebApiCompat | 12 | 0 | 12 | 11 | 0 | 0 | 0 |
| libSceOpusCeltDec | 12 | 9 | 12 | 9 | 9 | 0 | 0 |
| libSceSystemLogger2NativeQueueClient | 11 | 5 | 11 | 9 | 9 | 0 | 1 |
| libSceTextToSpeech | 12 | 8 | 10 | 8 | 8 | 0 | 2 |
| libSceVideoStreamingEngine_sys | 0 | 12 | 12 | 12 | 0 | 0 | 0 |
| SceVshShellUIRetriever | 11 | 0 | 0 | 0 | 0 | 0 | 11 |
| libSceCsbMgr | 11 | 0 | 10 | 7 | 0 | 0 | 1 |
| libSceDepth2 | 11 | 8 | 10 | 8 | 8 | 0 | 1 |
| libSceGvMp4Parser | 7 | 4 | 5 | 4 | 4 | 0 | 6 |
| libSceJpegParser | 7 | 5 | 5 | 5 | 5 | 0 | 6 |
| libSceMediaFrameworkUtil | 11 | 0 | 5 | 4 | 0 | 4 | 6 |
| libSceNetCtlAp | 11 | 0 | 11 | 9 | 9 | 0 | 0 |
| libSceNpScoreCompat | 11 | 0 | 11 | 9 | 0 | 0 | 0 |
| libSceNpSessionSignalingCrossplay | 11 | 0 | 5 | 5 | 5 | 0 | 6 |
| libSceNpTextToSpeech | 11 | 0 | 5 | 5 | 5 | 0 | 6 |
| libSceSocialScreen | 11 | 11 | 11 | 11 | 11 | 0 | 0 |
| libSceTtsEngine | 11 | 0 | 9 | 8 | 8 | 0 | 2 |
| libSceVdecSvp9 | 11 | 0 | 0 | 0 | 0 | 0 | 11 |
| libSceVdecwrap | 11 | 8 | 11 | 8 | 8 | 0 | 0 |
| libSceWebRtc | 11 | 0 | 1 | 0 | 0 | 0 | 10 |
| libSceWtIpcClient | 11 | 0 | 0 | 0 | 0 | 0 | 11 |
| SceVshMarlinDownloaderWrapper | 10 | 0 | 0 | 0 | 0 | 0 | 10 |
| libSceAppMessaging | 10 | 0 | 8 | 8 | 0 | 0 | 2 |
| libSceCustomMusicAudioOut | 10 | 5 | 10 | 8 | 8 | 0 | 0 |
| libSceDipsw | 10 | 7 | 10 | 8 | 8 | 0 | 0 |
| libSceMsgDialog | 10 | 8 | 10 | 8 | 7 | 0 | 0 |
| libSceMsgDialog.native | 10 | 0 | 10 | 8 | 8 | 0 | 0 |
| libSceRnpsBundle | 10 | 0 | 5 | 4 | 0 | 0 | 5 |
| libSceSaveDataDialog | 10 | 8 | 10 | 8 | 0 | 0 | 0 |
| libSceSaveDataDialog.native | 10 | 8 | 10 | 8 | 8 | 0 | 0 |
| libSceSystemTts | 10 | 5 | 9 | 8 | 8 | 0 | 1 |
| SceVshSystemLoggerUtilWrapper | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| libReactNative.Modules.Vsh.MediaPlayer.Contents | 9 | 4 | 7 | 6 | 0 | 0 | 2 |
| libSceCustomMusicDummy | 9 | 0 | 3 | 2 | 0 | 0 | 6 |
| libSceEditMp4 | 9 | 8 | 9 | 8 | 8 | 0 | 0 |
| libSceGameCustomDataDialog | 9 | 7 | 9 | 7 | 7 | 0 | 0 |
| libSceHmdDistortion | 9 | 0 | 8 | 7 | 0 | 0 | 1 |
| libSceInetStat | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| libSceInvitationDialog | 9 | 9 | 9 | 9 | 6 | 0 | 0 |
| libSceNetBwe | 9 | 0 | 9 | 7 | 0 | 0 | 0 |
| libSceNpEulaDialog | 0 | 8 | 9 | 8 | 8 | 0 | 0 |
| libSceNpFriendListDialog | 9 | 7 | 9 | 7 | 7 | 0 | 0 |
| libScePSNowGkp | 9 | 4 | 9 | 7 | 7 | 0 | 0 |
| libScePsml_mfsr2 | 9 | 0 | 9 | 8 | 0 | 0 | 0 |
| libsceNpEulaDialog | 9 | 8 | 9 | 8 | 8 | 0 | 0 |
| SceVshCloudClient | 8 | 0 | 0 | 0 | 0 | 0 | 8 |
| libSceAudiodecCpu | 8 | 7 | 8 | 7 | 7 | 0 | 0 |
| libSceContentBinder | 8 | 0 | 8 | 8 | 0 | 0 | 0 |
| libSceErrorDialog | 8 | 7 | 8 | 7 | 7 | 0 | 0 |
| libSceGameUpdate | 8 | 6 | 8 | 6 | 6 | 0 | 0 |
| libSceGnmDriverResourceRegistration | 8 | 0 | 3 | 3 | 0 | 0 | 5 |
| libSceMediaAppSharedStorageMc | 8 | 0 | 0 | 0 | 0 | 0 | 8 |
| libSceNpProfileDialog | 8 | 6 | 8 | 6 | 6 | 0 | 0 |
| libSceSulphaDrv | 8 | 6 | 8 | 6 | 6 | 0 | 0 |
| libSceUrlConfigResolver | 7 | 4 | 8 | 7 | 7 | 0 | 0 |
| libSceVcodec | 8 | 0 | 5 | 5 | 0 | 5 | 3 |
| libSceVrHand | 8 | 0 | 8 | 6 | 6 | 0 | 0 |
| libjimage | 8 | 0 | 0 | 0 | 0 | 0 | 8 |
| libkernel_qadisc | 8 | 0 | 6 | 5 | 0 | 0 | 2 |
| SystemNet | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libSceAc3Enc | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libSceAgcDriverDebugWavefronts_nosubmission | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libSceCdlgAdIdClient | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libSceCdlgG2P | 7 | 5 | 7 | 5 | 5 | 0 | 0 |
| libSceCdlgPlayerReview | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceConnectAccountDialog | 7 | 0 | 7 | 6 | 6 | 0 | 0 |
| libSceCoredumpSeqHandlerIf | 7 | 0 | 6 | 5 | 0 | 0 | 1 |
| libSceDbgKeyboard | 7 | 0 | 7 | 6 | 0 | 0 | 0 |
| libSceDtsEnc | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceGifParser | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libSceHmdSetupDialog | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libSceJxrParser | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libSceLibcInternalExt | 7 | 0 | 7 | 5 | 0 | 0 | 0 |
| libSceLoginDialog | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceMusicCoreInterface | 7 | 0 | 7 | 6 | 0 | 6 | 0 |
| libSceNetCtlApDialog | 7 | 5 | 7 | 5 | 5 | 0 | 0 |
| libSceNpAuthAuthorizedAppDialog | 7 | 0 | 7 | 7 | 7 | 0 | 0 |
| libSceNpSnsFacebookDialog | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libSceNpSnsYouTubeDialog | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libSceNpSpeechToText | 7 | 0 | 7 | 7 | 7 | 0 | 0 |
| libScePlayGoDialog | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libScePlayerInvitationDialog | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libScePlayerSelectionDialog | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libScePngParser | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libScePs2EmuMenuDialog | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceReportSeqHandlerIf | 7 | 0 | 5 | 5 | 0 | 0 | 2 |
| libSceShellUIUtil | 7 | 5 | 7 | 5 | 5 | 0 | 0 |
| libSceSigninDialog | 7 | 7 | 7 | 7 | 7 | 0 | 0 |
| libSceSocialScreenDialog | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceSystemLogger2Delivery | 6 | 4 | 7 | 6 | 6 | 0 | 0 |
| libSceSystemServiceActivateHevc | 7 | 0 | 7 | 6 | 0 | 0 | 0 |
| libSceSystemServiceActivateHevcSoft | 7 | 0 | 7 | 5 | 0 | 0 | 0 |
| libSceUsbStorageAux | 7 | 0 | 7 | 7 | 0 | 0 | 0 |
| libSceUsbStorageDialog | 7 | 5 | 7 | 5 | 5 | 0 | 0 |
| libSceVdecShevc.native | 0 | 7 | 7 | 7 | 0 | 0 | 0 |
| libSceVideoOutHdrScopes_nosubmission | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| libSceVideodec | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceVrServiceDialog | 7 | 6 | 7 | 6 | 6 | 0 | 0 |
| libSceVrSetupDialog | 7 | 0 | 7 | 6 | 6 | 0 | 0 |
| libSceWebmParserMdrw | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| SceVshShareNpWrapper | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| libSceAutoMounterClient | 6 | 5 | 6 | 5 | 5 | 0 | 0 |
| libSceCloudMessaging | 6 | 0 | 6 | 6 | 0 | 0 | 0 |
| libSceContentSearchForSf | 6 | 0 | 4 | 2 | 0 | 0 | 2 |
| libSceHmd2Distortion | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| libSceJpegDec | 6 | 6 | 6 | 6 | 6 | 0 | 0 |
| libSceMediaAppSharedStorageMaDbg | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| libSceMouseExtension_nosubmission | 6 | 0 | 6 | 5 | 0 | 0 | 0 |
| libSceNKWeb | 5 | 3 | 3 | 3 | 2 | 0 | 3 |
| libSceNpPartyCompat | 6 | 0 | 6 | 3 | 0 | 0 | 0 |
| libSceNpSessionService | 6 | 0 | 6 | 5 | 0 | 0 | 0 |
| libScePadTracker | 6 | 4 | 6 | 4 | 4 | 0 | 0 |
| libScePngDec | 6 | 4 | 6 | 4 | 4 | 0 | 0 |
| libScePsmlBcSisr | 6 | 0 | 3 | 2 | 0 | 0 | 3 |
| libScePubSubClientShared | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| libSceShareFactoryUtil | 6 | 5 | 6 | 5 | 5 | 0 | 0 |
| libSceSystemServiceActivateMpeg2 | 6 | 0 | 6 | 3 | 0 | 0 | 0 |
| libSceVideoNativeExtEssential | 6 | 4 | 5 | 4 | 4 | 0 | 1 |
| libSceVshBrotli | 6 | 0 | 0 | 0 | 0 | 0 | 6 |
| libSceWkFontConfig | 5 | 6 | 6 | 6 | 5 | 0 | 0 |
| libkernel_sync_on_address2 | 6 | 0 | 6 | 5 | 0 | 0 | 0 |
| libSceAcm_Ref_nosubmission | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| libSceAsyncStorageInternalAux | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| libSceAt9Enc | 5 | 5 | 5 | 5 | 5 | 0 | 0 |
| libSceCompanionUtil | 5 | 4 | 5 | 4 | 4 | 0 | 0 |
| libSceContentExportForSf | 5 | 0 | 5 | 4 | 0 | 0 | 0 |
| libSceDeviceService | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| libSceDiscMap | 5 | 2 | 2 | 2 | 2 | 0 | 3 |
| libSceIpmiDbg | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| libSceMediaAppSharedStorageMa | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| libSceNetCtlV6 | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| libSceNpMatching2Compat | 5 | 0 | 5 | 3 | 0 | 0 | 0 |
| libSceNpPartner001 | 4 | 1 | 5 | 4 | 2 | 1 | 0 |
| libSceNpSignalingCompat | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| libSceVrTrackerGpuTest | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| libSceVrTrackerLiveCapture | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| libSceZlib | 5 | 4 | 5 | 4 | 4 | 0 | 0 |
| libkernel_aod | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| libkernel_exception | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| libkernel_ps2emu | 5 | 0 | 5 | 5 | 0 | 0 | 0 |
| SceVshRemotePlayClientIpcWrapper | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| libSceAcm_Propagation_nosubmission | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| libSceAgcDriverDebugReset_nosubmission | 4 | 0 | 4 | 2 | 0 | 0 | 0 |
| libSceAppContentIro | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libSceContentDelete | 4 | 4 | 4 | 4 | 4 | 0 | 0 |
| libSceConvertKeycode | 4 | 2 | 4 | 2 | 2 | 0 | 0 |
| libSceDseehx | 0 | 3 | 4 | 3 | 3 | 0 | 0 |
| libSceJpegEnc | 4 | 3 | 4 | 3 | 3 | 0 | 0 |
| libSceMat2Enc | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| libSceNetCtlForNpToolkit | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libSceNotification | 4 | 1 | 4 | 3 | 3 | 0 | 0 |
| libSceNpPartnerSubscription | 4 | 0 | 2 | 2 | 2 | 0 | 2 |
| libSceNpSnsTwitch | 4 | 0 | 4 | 3 | 0 | 0 | 0 |
| libSceNpSnsYouTube | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libSceNpUbisoftPlus | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| libScePngEnc | 4 | 4 | 4 | 4 | 4 | 0 | 0 |
| libSceProprietaryVoiceChatHelper | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libScePsmUtil | 4 | 3 | 4 | 3 | 3 | 0 | 0 |
| libSceS3da | 4 | 4 | 4 | 4 | 4 | 0 | 0 |
| libSceShareForSf | 4 | 0 | 2 | 1 | 0 | 0 | 2 |
| libSceShareInternalForShellCore | 4 | 0 | 2 | 0 | 0 | 0 | 2 |
| libSceSystemServicePs2Emu | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libSceVdecSavc | 4 | 4 | 4 | 4 | 4 | 0 | 0 |
| libSceVdecSavc2 | 4 | 4 | 4 | 4 | 4 | 0 | 0 |
| libSceVdecSavc2.native | 0 | 4 | 4 | 4 | 0 | 0 | 0 |
| libSceVideoCoreInterface | 4 | 1 | 4 | 3 | 3 | 0 | 0 |
| libSceVideoDecoderArbitration | 4 | 4 | 4 | 4 | 4 | 0 | 0 |
| libSceVideoOutVrrStatus | 4 | 0 | 4 | 2 | 0 | 0 | 0 |
| libSceVrHand_nosubmission | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libkernel_CFI | 4 | 0 | 4 | 3 | 0 | 0 | 0 |
| libkernel_mtxgen | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libkernel_sysc_se | 4 | 0 | 4 | 4 | 0 | 0 | 0 |
| libverify | 4 | 0 | 4 | 3 | 0 | 0 | 0 |
| ulobjmgr | 4 | 0 | 2 | 2 | 2 | 0 | 2 |
| ScePlayStationPUIPlatform | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| libSceDbgVideoOut | 3 | 0 | 1 | 1 | 0 | 0 | 2 |
| libSceEsvmAppAudioSync | 3 | 0 | 3 | 1 | 0 | 0 | 0 |
| libSceEsvmPlayReady | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceFreeTypeOptOl | 0 | 3 | 3 | 3 | 0 | 0 | 0 |
| libSceHubAppUtil | 3 | 2 | 3 | 2 | 2 | 0 | 0 |
| libSceLoginService | 3 | 1 | 3 | 1 | 1 | 0 | 0 |
| libSceNetDebug | 3 | 0 | 2 | 2 | 0 | 0 | 1 |
| libSceNpAppLauncher | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceNpCommonCompat | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceNpManagerForToolkit | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceNpTcs | 0 | 3 | 3 | 3 | 3 | 0 | 0 |
| libSceNpUtilityCompat | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceNpWebApi2AsyncRestricted | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| libScePsml_nosubmission | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| libSceSysmodule_jvm | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| libSceSystemLogger | 3 | 2 | 3 | 2 | 2 | 0 | 0 |
| libSceSystemServiceAppInfo | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| libSceSystemServiceMicExclusiveMode | 3 | 0 | 1 | 1 | 0 | 0 | 2 |
| libSceSystemServicePlatformPrivacy | 3 | 0 | 3 | 2 | 0 | 0 | 0 |
| libSceSystemServicePsmKit | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceSystemServiceSuspend | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceSystemService_jvm | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceVideoArbitration | 3 | 3 | 3 | 3 | 3 | 0 | 0 |
| libkernel_devtoollog | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| libkernel_pre250mmap | 3 | 0 | 3 | 1 | 0 | 0 | 0 |
| libkernel_unity | 3 | 0 | 3 | 3 | 0 | 0 | 0 |
| libSceAjmWVorbis | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceAppDbShellCoreClientForSystemService | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libSceCoredump_debug | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceCoredump_nosubmission | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceDiscId | 2 | 1 | 2 | 1 | 1 | 0 | 0 |
| libSceGameCustomDataDialogCompat | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceGameLiveStreaming_debug | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceGameLiveStreaming_direct_streaming | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceGnmDebugReset | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceGnmDriverCompat | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceGnmWaitFreeSubmit | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libSceInvitationDialogCompat | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceKbEmulate | 2 | 2 | 2 | 2 | 0 | 0 | 0 |
| libSceNetConnSwitcher | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libSceNpAuthCompat | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceNpFriendListDialogCompat | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceNpPremiumAddcont | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libScePlayGo_nosubmission | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceShareForAcf | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceSisrSys | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceSystemLogger2Game | 2 | 0 | 2 | 2 | 2 | 0 | 0 |
| libSceSystemModalDialog | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceSystemServiceClosedCaption | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceSystemServiceEyeToEyeDistance | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceSystemServicePartyVoice | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceSystemServicePowerControl | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceSystemServiceTelemetry2 | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceSystemServiceTournamentMlg | 2 | 0 | 1 | 1 | 0 | 0 | 1 |
| libSceSystemServiceVoiceRecognition | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceSystemServiceVrApp | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceSystemServiceWebApp | 2 | 0 | 1 | 1 | 0 | 0 | 1 |
| libSceSystemServiceYouTubeAccountLinkStatus | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libSceSystemServiceYouTubeDeviceAuth | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libSceUserServiceForNpToolkit | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceUserServiceForShellCore | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libSceVideoOutLatency | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libSceVideoOutSecondary | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libSceVideoOutServer | 2 | 0 | 1 | 1 | 0 | 0 | 1 |
| libSceVideoOutVrrPeg | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libkernel_avcf | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libkernel_cpumode | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libkernel_low_energy_mode | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libkernel_mmap | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libkernel_module_info | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libkernel_seh | 2 | 0 | 2 | 2 | 0 | 0 | 0 |
| libkernel_sync_on_address | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| libkernel_wt_config | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| libmono-profiler-log | 0 | 1 | 2 | 1 | 0 | 0 | 0 |
| WebAppBundle | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| libBdplus | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libRnpsDevSupport.Dummy | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceAcm_IrGeneration_nosubmission | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceAgcDriverAsyncGraphicsRingEval_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceAppContentBundle | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceAppContentGameTrials | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceAppContentMdid | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceAppContentPft | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceAppContentSc | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceAudioOutDeviceService | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceContentDeleteForSf | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceDbgAudioOut | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceDbgAudioOut2 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceDbgVideoOutSqa | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceEsvmDecoderModeEx | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceGic | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| libSceGnmDebugModuleReset | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceGnmGetGpuCoreClockFrequency | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceHmd2ReprojectionBlankInBackground | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceHmd2ReprojectionMotionVector | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceHmd2ReprojectionMotionVector_nosubmission | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceHmd2ReprojectionPositional | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceHmd2Reprojection_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceHmd2Reprojection_vrremote_nosubmission | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceImeConsecutiveClauseConversionExtensions | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceImeDialogVoiceDictation | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceImeRemotePlayExtensions | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceImeVoiceDictation | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceJpegDec_jvm | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceNKWebCdlgInjectedBundle | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceNetworkProfiler | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceNpAuthAuthorizedApp | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceNpEntitlementAccessGameTrials | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceNpEntitlementAccessPft | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceNpManagerIsPlusMember | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceNpProfileDialogCompat | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceOpenPsId | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libScePngDec_jvm | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libScePsml_lightweight | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libScePsml_quality8K | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libScePsml_set_mfsrversion | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libScePsml_specularAA | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceRandom | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| libSceRemoteplay_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceRnpsNKInjectedBundle | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceSaveData_native_old_format | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceScreenShotDrc | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSharePlayCompat | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceShellCoreRedisModule | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceSystemServiceAppLaunchLink | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceSystemServiceDbg | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceForShellCoreOnly | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServicePadspkRouting | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceSystemServicePowerSaveLevel | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceSystemServiceStorageManagement | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceSystemServiceStore | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceTelemetry | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceTournament | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceUdsApp | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceVideoServiceWebApp | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceVideoToken | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceSystemServiceWebBrowser | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceTelemetryRedisModule | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceUserServiceAudioFocus | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceUserServicePlatformPrivacyWs1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| libSceUserServiceRegisteredUserIdList | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOut8kTrial_nosubmission | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceVideoOutAniso | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutAspectRatio21_9Trial_nosubmission | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceVideoOutAspectRatio32_9Trial_nosubmission | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceVideoOutBaseMode4k | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutExtra | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutHdr | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutLatency_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutOverlay64bpp | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceVideoOutRawEdid | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutSqa_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutSubEx | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVideoOutSwitchBusFor64bpp | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceVideoOutWindow2Pre400 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libSceVideoOutWqhd | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVoice_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVrTrackerDeviceRejection | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceVrTrackerFourDeviceAllowed | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libSceWebBrowserDialogLimited | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| libkernel_avlfmem | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_cpumode_platform | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_dmem_aliasing | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_dmem_aliasing2 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_dmem_aliasing2_for_dev | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_dmem_aliasing3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_module_extension | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_module_extension_nosubmission | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_module_load_check | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libkernel_write_throttling | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| libsceHmdReprojectionMultilayer | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| monoprofilerlog | 1 | 0 | 0 | 0 | 0 | 0 | 1 |

## C. Readiness stages

| Stage | Count | Interpretation |
|---|---:|---|
| qualified unique nids | 10,749 | Source-backed or canonical classification |
| strict qualified unique nids | 9,158 | Source-backed or canonical classification |
| anyps5 main definition matches | 15,632 | Source-backed or canonical classification |
| anyps5 throwing marker | 12,213 | Source-backed or canonical classification |
| anyps5 nonthrowing body | 3,419 | Source-backed or canonical classification |
| open pr qualified partial | 1,294 | Source-backed or canonical classification |
| snapshot locally prepared stubs | 963 | Saved snapshot, not live |
| snapshot fully validated stubs | 0 | Saved snapshot, not live |
| build verified live | unknown | Not measured; never inferred from source bodies |
| abi verified live | unknown | Not measured; never inferred from source bodies |
| runtime validated live | unknown | Not measured; never inferred from source bodies |
| fully implemented live | unknown | Not measured; never inferred from source bodies |

### AnyPS5 changes since the previous revision

Previous SHA: 9310f48f1599d0b0a73ccdba39ed8bacee861bb7
Added identities: 1,743; removed: 156; changed source classifications: 114.
These values do not verify implementation changes or runtime behaviour.

## D. Ownership classifications

| Scope | Records |
|---|---:|
| existing_firmware_system_library | 15,703 |
| existing_upstream_placeholder_library | 21,799 |
| historical_only | 11,700 |
| managed_or_application_native_image | 252,818 |
| middleware_scope_review | 445 |
| new_system_library_review | 2,592 |
| ownership_pending | 7,322 |
| shell_specific_review | 1,659 |

## E. Review priorities

Heuristic: remaining assessed qualified records in known system/placeholder scopes, discounting observed main/PR matches. **Not an eligibility certificate.**

| Library | Priority score | Qualified assessed | Unnamed | 3.20 name proposals |
|---|---:|---:|---:|---:|
| libSceJsc | 2,554 | 2,951 | 1,331 | 0 |
| libSceNKWebKit | 1,278 | 8,614 | 6,829 | 0 |
| libSceMediaFrameworkInterface | 13 | 139 | 86 | 0 |
| libSceIcu | 12 | 72 | 42 | 0 |
| libSceSaveData | 8 | 8 | 18 | 0 |
| libSceFontGs | 5 | 8 | 4 | 0 |
| libSceTEEClient | 1 | 1 | 4 | 0 |
| I18N | 0 | 0 | 72 | 0 |
| I18NCJK | 0 | 0 | 59 | 0 |
| I18NMidEast | 0 | 0 | 14 | 0 |
| I18NOther | 0 | 0 | 30 | 0 |
| I18NRare | 0 | 0 | 46 | 0 |
| I18NWest | 0 | 0 | 22 | 0 |
| MicrosoftCSharp | 0 | 0 | 1,739 | 0 |
| MonoDataSqlite | 0 | 0 | 898 | 0 |
| MonoDataTds | 0 | 0 | 348 | 0 |
| MonoSecurity | 0 | 0 | 700 | 0 |
| NewtonsoftJsonPlayStation | 0 | 0 | 4,016 | 0 |
| ReactNativeComponentsVsh | 0 | 0 | 820 | 0 |
| ReactNativeComponentsVshPSNowPlayer | 0 | 0 | 271 | 0 |
| ReactNativeModulesVsh | 0 | 0 | 6,713 | 0 |
| ReactNativeModulesVshMedia | 0 | 0 | 1,058 | 0 |
| ReactNativeModulesVshMediaPlayerContents | 0 | 0 | 189 | 0 |
| ReactNativeModulesVshPSNowPlayer | 0 | 0 | 421 | 0 |
| ReactNativeModulesVshTelemetryNq | 0 | 0 | 29 | 0 |
| ReactNativeModulesVshTrophy | 0 | 0 | 2,177 | 0 |
| ReactNativeModulesVshWebAppLauncher | 0 | 0 | 562 | 0 |
| ReactNativePUI | 0 | 0 | 10,924 | 0 |
| ReactNativeVshCommon | 0 | 0 | 990 | 0 |
| ReactivePropertyPlayStation | 0 | 0 | 4,457 | 0 |
| SceFacebookCSSLayout | 0 | 0 | 263 | 0 |
| ScePlayStationBclExtensions | 0 | 0 | 30 | 0 |
| ScePlayStationCore | 0 | 0 | 1,830 | 0 |
| ScePlayStationIcu | 0 | 0 | 12 | 0 |
| ScePlayStationIme | 0 | 0 | 461 | 0 |
| ScePlayStationJson | 0 | 0 | 493 | 0 |
| ScePlayStationOrbis | 0 | 0 | 337 | 0 |
| ScePlayStationOrbisSpeech | 0 | 0 | 113 | 0 |
| ScePlayStationPUI | 0 | 0 | 17,872 | 0 |
| ScePlayStationPUIPlatform | 0 | 0 | 3 | 0 |

## F. Automation health

| Signal | Value |
|---|---|
| last refresh utc | 2026-10-31T00:49:18+00:00 |
| pr scanned | 1,530 |
| pr total | 1,548 |
| pr complete | 0 |
| pr errors | 17 |
| anyps5 symbol observations | 31,450 |
| anyps5 declarations only | 120 |
| anyps5 explicit alias records | 3,759 |
| anyps5 export registration verified | unknown |
| source 320 files | 275 |
| source 320 registrations | 33,298 |
| source 320 conflicts quarantined | 10,728 |
| source 320 quarantine by reason | {"nid_name_hash_mismatch": 5860} |
| source 320 top quarantine sources | [{'rejected_registrations': 1803, 'source_file': 'libSceNKWebKit.c'}, {'rejected_registrations': 623, 'source_file': 'libSceJsc.c'}, {'rejected_registrations': 336, 'source_file': 'libSceLibcInternal.c'}, {'rejected_registrations': 238, 'source_file': 'libicu.c'}, {'rejected_registrations': 191, 'source_file': 'libkernel_sys.c'}, {'rejected_registrations': 168, 'source_file': 'libkernel.c'}, {'rejected_registrations': 163, 'source_file': 'libkernel_web.c'}, {'rejected_registrations': 146, 'source_file': 'libmonosgen-2.0.c'}, {'rejected_registrations': 105, 'source_file': 'libSceIcu.c'}, {'rejected_registrations': 100, 'source_file': 'libSceNpCommon.c'}, {'rejected_registrations': 88, 'source_file': 'libSceSystemService.c'}, {'rejected_registrations': 70, 'source_file': 'libSceUserService.c'}, {'rejected_registrations': 67, 'source_file': 'libSceLibreSsl3.c'}, {'rejected_registrations': 63, 'source_file': 'mscorlib.dll.c'}, {'rejected_registrations': 61, 'source_file': 'libSceFreeTypeOl.c'}, {'rejected_registrations': 61, 'source_file': 'libSceFreeTypeOt.c'}, {'rejected_registrations': 56, 'source_file': 'libSceLibreSsl.c'}, {'rejected_registrations': 43, 'source_file': 'libSceCesCs.c'}, {'rejected_registrations': 43, 'source_file': 'libSceNpManager.c'}, {'rejected_registrations': 33, 'source_file': 'libSceGLSlimVSH.c'}] |
| source 320 review items | 10,846 |
| source 320 canonical auto changes | 0 |
| source 320 statuses | {"already_indexed_and_named": 28312, "ownership_review_required": 4868, "withheld": 118} |
| anyps5 public source proposals | 11,906 |
| anyps5 withheld names | 33 |
| overlap publication safe | 0 |

### Actual progress trend

| Observed at (UTC) | Indexed | Strictly verified names | AnyPS5 main source matches | Open PR heads scanned |
|---|---:|---:|---:|---:|
| 2026-10-30T07:23:47+00:00 | 314,038 | 39,966 | 7,753 | 540 |
| 2026-10-30T07:28:37+00:00 | 314,038 | 39,966 | 7,753 | 1,076 |
| 2026-10-30T13:00:07+00:00 | 314,038 | 39,966 | 15,544 | 1,388 |
| 2026-10-30T19:57:11+00:00 | 314,038 | 39,966 | 15,583 | 1,610 |
| 2026-10-31T00:49:18+00:00 | 314,038 | 39,966 | 15,632 | 1,530 |

### Coverage denominators

- **indexed_records:** 314038
- **verified_name_rate:** strictly rehashed named / all indexed library+NID records
- **anyps5_main:** matched definitions / indexed library+NID records, not functionality
- **pr_scan:** current open PR heads successfully scanned / all currently open PRs
- **library_320:** registered 3.20 forwarder bindings observed in source, not 13.60 exports

### Limitations

- If open-PR scanning was skipped, its per-library counts are null (unknown), not zero.
- An absent PR match is unknown while PR scanning is incomplete.
- The 3.20-only source is not evidence of a firmware 13.60 export.
- Source definitions are not proof of registration, ABI, build or runtime verification.
- Live implementation correctness is not measured; null means unknown.
- Priority score indicates triage value, not safe stub-generation eligibility.
