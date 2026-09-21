# Codebase map

Revision and caveats: see [ARCHITECTURE.md](ARCHITECTURE.md). Generated from the recovered source on 2026-09-15.

Each subsystem contains a JSON array with the requested stable field names. Python class/function names and line numbers are parsed from source without importing application modules; JavaScript function extraction covers named function declarations, not every arrow callback. Call edges, reads/writes and responsibilities are curated for architectural navigation. Symbols listed are definitions, not proof every path runs in the default deployment. UNKNOWN runtime validation and external services remain as described in the architecture report.

## Repository inventory

```json
[
  {
    "directory": "frontend",
    "tracked_files": 473,
    "top_level_directories": [
      ".claude",
      ".github",
      "assets",
      "build",
      "docs",
      "scripts",
      "server",
      "src"
    ],
    "commit": "4114336ee0cf1a8a04c20a96f4a92f30fe059c66"
  },
  {
    "directory": "backend/core_api",
    "tracked_files": 360,
    "top_level_directories": [
      ".github",
      "cowork",
      "docs",
      "tests"
    ],
    "commit": "cb075bdf79242d865f5e8809cedfa1debb63e519"
  },
  {
    "directory": "backend/core_agent",
    "tracked_files": 252,
    "top_level_directories": [
      ".github",
      "anton",
      "assets",
      "docs",
      "tests"
    ],
    "commit": "6b83930e510a984aa822a2cc46a2143a4e94343f"
  },
  {
    "directory": "backend/data-vault",
    "tracked_files": 1675,
    "top_level_directories": [
      ".devcontainer",
      ".github",
      "assets",
      "docker",
      "docs",
      "mindsdb",
      "mindsdb hacktoberfest",
      "requirements",
      "scripts",
      "tests"
    ],
    "commit": "37ccd07febc9c4a20bd5c1fcd4f677efac553dc9"
  }
]
```

## Frontend

```json
[
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/main.tsx",
    "Responsibility": "Desktop React entry; bridge guard, theme bootstrap, mount App",
    "Important classes": [],
    "Important functions": [],
    "Calls": [
      "App"
    ],
    "Called by": [
      "Electron renderer"
    ],
    "Data read": [
      "localStorage",
      "preload bridge"
    ],
    "Data written": [
      "DOM"
    ],
    "External dependencies": [
      "React",
      "react-dom"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/web-main.tsx",
    "Responsibility": "Browser entry and hostname-dependent Keycloak authentication",
    "Important classes": [],
    "Important functions": [
      {
        "name": "saveMindsToken",
        "line": 61
      },
      {
        "name": "handleKeycloakEvent",
        "line": 69
      }
    ],
    "Calls": [
      "saveMindsToken",
      "scheduleWebTokenRefresh",
      "App"
    ],
    "Called by": [
      "web index HTML"
    ],
    "Data read": [
      "hostname",
      "identity token",
      "localStorage"
    ],
    "Data written": [
      "provider settings",
      "DOM"
    ],
    "External dependencies": [
      "React",
      "Keycloak"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/App.tsx",
    "Responsibility": "Onboarding gate state machine",
    "Important classes": [],
    "Important functions": [
      {
        "name": "hasLocalTermsConsent",
        "line": 34
      },
      {
        "name": "rememberTermsConsent",
        "line": 43
      },
      {
        "name": "rememberCoworker",
        "line": 47
      },
      {
        "name": "recallCoworker",
        "line": 51
      },
      {
        "name": "devForcedPage",
        "line": 63
      },
      {
        "name": "App",
        "line": 74
      },
      {
        "name": "init",
        "line": 86
      }
    ],
    "Calls": [
      "host",
      "CoworkApp"
    ],
    "Called by": [
      "main.tsx",
      "web-main.tsx"
    ],
    "Data read": [
      "host configuration",
      "terms and coworker preferences"
    ],
    "Data written": [
      "localStorage",
      "gate state"
    ],
    "External dependencies": [
      "React"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/cowork/App.jsx",
    "Responsibility": "Workspace navigation, tasks, chat stream state and connector forms",
    "Important classes": [],
    "Important functions": [
      {
        "name": "describeConnectFormState",
        "line": 88
      },
      {
        "name": "isPendingFileAttachment",
        "line": 112
      },
      {
        "name": "isAntonConfigError",
        "line": 116
      },
      {
        "name": "normalizeAntonError",
        "line": 126
      },
      {
        "name": "resolveComposerAttachmentsForSend",
        "line": 134
      },
      {
        "name": "normalizeComposerDisabledConnections",
        "line": 155
      },
      {
        "name": "pickContinuePrompt",
        "line": 193
      },
      {
        "name": "stripStreaming",
        "line": 197
      },
      {
        "name": "openStreamedForm",
        "line": 211
      },
      {
        "name": "reconcileTaskMessages",
        "line": 250
      },
      {
        "name": "removeThinkingPlaceholder",
        "line": 336
      },
      {
        "name": "withThinkingPlaceholder",
        "line": 340
      },
      {
        "name": "markActivityDone",
        "line": 390
      },
      {
        "name": "humanizeToken",
        "line": 398
      },
      {
        "name": "describeActivity",
        "line": 405
      },
      {
        "name": "readConvTurns",
        "line": 447
      },
      {
        "name": "writeConvTurns",
        "line": 459
      },
      {
        "name": "migrateLegacyArtifacts",
        "line": 467
      },
      {
        "name": "reduceServerEvents",
        "line": 489
      },
      {
        "name": "hydrateMessagesFromServerEvents",
        "line": 505
      },
      {
        "name": "persistTurnState",
        "line": 526
      },
      {
        "name": "mergeConvTurns",
        "line": 557
      },
      {
        "name": "mergeTasksFromServer",
        "line": 593
      },
      {
        "name": "appendActivity",
        "line": 646
      },
      {
        "name": "App",
        "line": 665
      },
      {
        "name": "AppCore",
        "line": 669
      }
    ],
    "Calls": [
      "handleSendFromHome",
      "handleSendInTask",
      "streamMessage",
      "reduceStream"
    ],
    "Called by": [
      "CoworkApp"
    ],
    "Data read": [
      "API records",
      "local turn cache"
    ],
    "Data written": [
      "React state",
      "localStorage",
      "API mutations"
    ],
    "External dependencies": [
      "React"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/cowork/api.js",
    "Responsibility": "HTTP API client, streamed-response parsing and data transforms",
    "Important classes": [],
    "Important functions": [
      {
        "name": "req",
        "line": 23
      },
      {
        "name": "rootReq",
        "line": 47
      },
      {
        "name": "dedupe",
        "line": 77
      },
      {
        "name": "responseError",
        "line": 91
      },
      {
        "name": "fetchHealth",
        "line": 103
      },
      {
        "name": "_humanTime",
        "line": 117
      },
      {
        "name": "_hydrateAssistantEvents",
        "line": 134
      },
      {
        "name": "_conversationToTask",
        "line": 154
      },
      {
        "name": "fetchSessions",
        "line": 196
      },
      {
        "name": "fetchSession",
        "line": 226
      },
      {
        "name": "allocateConversationId",
        "line": 246
      },
      {
        "name": "_streamResponse",
        "line": 267
      },
      {
        "name": "streamNewSession",
        "line": 363
      },
      {
        "name": "fetchInFlightStatus",
        "line": 374
      },
      {
        "name": "fetchInFlightList",
        "line": 388
      },
      {
        "name": "tailInFlight",
        "line": 397
      },
      {
        "name": "streamMessage",
        "line": 484
      },
      {
        "name": "fetchProjects",
        "line": 500
      },
      {
        "name": "createProject",
        "line": 510
      },
      {
        "name": "renameProject",
        "line": 518
      },
      {
        "name": "revealProjectInFinder",
        "line": 539
      },
      {
        "name": "cancelScratchpad",
        "line": 553
      },
      {
        "name": "cancelResponse",
        "line": 575
      },
      {
        "name": "unpublishArtifact",
        "line": 589
      },
      {
        "name": "deleteArtifact",
        "line": 605
      },
      {
        "name": "deleteProject",
        "line": 618
      },
      {
        "name": "isProjectInstructionsPath",
        "line": 654
      },
      {
        "name": "isUnderContextDir",
        "line": 660
      },
      {
        "name": "isUnderAntonDir",
        "line": 666
      },
      {
        "name": "fetchProjectInstructions",
        "line": 679
      },
      {
        "name": "listProjectFiles",
        "line": 686
      },
      {
        "name": "readProjectFile",
        "line": 698
      },
      {
        "name": "mountProjectFilePreview",
        "line": 709
      },
      {
        "name": "projectFileDownloadUrl",
        "line": 719
      },
      {
        "name": "writeProjectFile",
        "line": 724
      },
      {
        "name": "uploadProjectFiles",
        "line": 739
      },
      {
        "name": "deleteProjectFile",
        "line": 757
      },
      {
        "name": "fetchActiveProject",
        "line": 772
      },
      {
        "name": "setActiveProject",
        "line": 784
      },
      {
        "name": "fetchArtifacts",
        "line": 810
      },
      {
        "name": "previewArtifact",
        "line": 830
      },
      {
        "name": "mountArtifactPreview",
        "line": 841
      },
      {
        "name": "openArtifact",
        "line": 880
      },
      {
        "name": "artifactServeUrl",
        "line": 891
      },
      {
        "name": "openArtifactFile",
        "line": 903
      },
      {
        "name": "revealArtifact",
        "line": 915
      },
      {
        "name": "fetchRecommendedModels",
        "line": 937
      },
      {
        "name": "fetchSettings",
        "line": 945
      },
      {
        "name": "updateSettings",
        "line": 976
      },
      {
        "name": "validateSettings",
        "line": 1021
      },
      {
        "name": "testProviders",
        "line": 1025
      },
      {
        "name": "revealSettingKey",
        "line": 1034
      },
      {
        "name": "fetchIntegrations",
        "line": 1043
      },
      {
        "name": "startGoogleDriveAuth",
        "line": 1051
      },
      {
        "name": "startGoogleCalendarAuth",
        "line": 1055
      },
      {
        "name": "startGmailAuth",
        "line": 1059
      },
      {
        "name": "startGoogleAdsAuth",
        "line": 1063
      },
      {
        "name": "startGoogleAnalyticsAuth",
        "line": 1067
      },
      {
        "name": "startGcpAuth",
        "line": 1071
      },
      {
        "name": "fetchMemory",
        "line": 1076
      },
      {
        "name": "saveMemory",
        "line": 1084
      },
      {
        "name": "deleteMemory",
        "line": 1088
      },
      {
        "name": "fetchSkills",
        "line": 1094
      },
      {
        "name": "saveSkill",
        "line": 1098
      },
      {
        "name": "deleteSkill",
        "line": 1102
      },
      {
        "name": "fetchDatasources",
        "line": 1106
      },
      {
        "name": "saveDatasource",
        "line": 1117
      },
      {
        "name": "validateDatasource",
        "line": 1122
      },
      {
        "name": "deleteDatasource",
        "line": 1127
      },
      {
        "name": "fetchSavedConnection",
        "line": 1143
      },
      {
        "name": "fetchConnectors",
        "line": 1165
      },
      {
        "name": "fetchConnector",
        "line": 1174
      },
      {
        "name": "matchConnector",
        "line": 1178
      },
      {
        "name": "saveConnector",
        "line": 1189
      },
      {
        "name": "startConnectorOAuth",
        "line": 1218
      },
      {
        "name": "pollConnectorOAuth",
        "line": 1230
      },
      {
        "name": "fetchPublishable",
        "line": 1234
      },
      {
        "name": "streamDataVaultSubmission",
        "line": 1252
      },
      {
        "name": "submitDataVaultForm",
        "line": 1344
      },
      {
        "name": "publishArtifact",
        "line": 1368
      },
      {
        "name": "publishTargetPath",
        "line": 1379
      },
      {
        "name": "fetchBrowseStatus",
        "line": 1384
      },
      {
        "name": "fetchChannelPlugins",
        "line": 1393
      },
      {
        "name": "fetchChannelStatus",
        "line": 1402
      },
      {
        "name": "fetchChannelInstallations",
        "line": 1410
      },
      {
        "name": "fetchChannelAgent",
        "line": 1421
      },
      {
        "name": "setChannelAgent",
        "line": 1429
      },
      {
        "name": "fetchChannelConfig",
        "line": 1433
      },
      {
        "name": "saveChannelConfig",
        "line": 1437
      },
      {
        "name": "deleteChannelConfig",
        "line": 1444
      },
      {
        "name": "reloadChannel",
        "line": 1449
      },
      {
        "name": "setupChannel",
        "line": 1455
      },
      {
        "name": "teardownChannel",
        "line": 1459
      },
      {
        "name": "fetchChannelBindings",
        "line": 1465
      },
      {
        "name": "createChannelBinding",
        "line": 1475
      },
      {
        "name": "updateChannelBinding",
        "line": 1479
      },
      {
        "name": "deleteChannelBinding",
        "line": 1486
      },
      {
        "name": "uploadAttachments",
        "line": 1493
      },
      {
        "name": "fetchAttachments",
        "line": 1510
      },
      {
        "name": "deleteAttachment",
        "line": 1528
      },
      {
        "name": "attachmentRawUrl",
        "line": 1547
      },
      {
        "name": "moveAttachmentToProject",
        "line": 1557
      },
      {
        "name": "searchCowork",
        "line": 1569
      },
      {
        "name": "fetchPins",
        "line": 1574
      },
      {
        "name": "pinTask",
        "line": 1582
      },
      {
        "name": "unpinTask",
        "line": 1586
      },
      {
        "name": "renameConversation",
        "line": 1594
      },
      {
        "name": "patchConversation",
        "line": 1602
      },
      {
        "name": "deleteConversationTurn",
        "line": 1614
      },
      {
        "name": "deleteConversation",
        "line": 1631
      },
      {
        "name": "moveConversation",
        "line": 1650
      },
      {
        "name": "recordTaskVisit",
        "line": 1657
      },
      {
        "name": "fetchSchedules",
        "line": 1663
      },
      {
        "name": "createSchedule",
        "line": 1671
      },
      {
        "name": "updateSchedule",
        "line": 1675
      },
      {
        "name": "deleteSchedule",
        "line": 1679
      },
      {
        "name": "pauseSchedule",
        "line": 1683
      },
      {
        "name": "resumeSchedule",
        "line": 1687
      },
      {
        "name": "runScheduleNow",
        "line": 1691
      },
      {
        "name": "fetchScheduleRuns",
        "line": 1695
      }
    ],
    "Calls": [
      "_streamResponse",
      "streamMessage",
      "streamNewSession",
      "streamDataVaultSubmission"
    ],
    "Called by": [
      "cowork App and components"
    ],
    "Data read": [
      "HTTP JSON and SSE"
    ],
    "Data written": [
      "API requests"
    ],
    "External dependencies": [
      "fetch",
      "AbortController"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/cowork/lib/responseStreamAdapter.js",
    "Responsibility": "Reduce live/replayed response events to UI state",
    "Important classes": [],
    "Important functions": [
      {
        "name": "initialStreamState",
        "line": 30
      },
      {
        "name": "patchLastScratchpadStep",
        "line": 61
      },
      {
        "name": "patchScratchpadStepById",
        "line": 75
      },
      {
        "name": "closeOpenInspectableSteps",
        "line": 90
      },
      {
        "name": "closeOpenScratchpadStep",
        "line": 108
      },
      {
        "name": "closeReasoningStep",
        "line": 120
      },
      {
        "name": "toolCallLabel",
        "line": 131
      },
      {
        "name": "truncateLabel",
        "line": 143
      },
      {
        "name": "safeJsonParse",
        "line": 151
      },
      {
        "name": "extractJsonString",
        "line": 159
      },
      {
        "name": "bestEffortField",
        "line": 171
      },
      {
        "name": "reduceStream",
        "line": 187
      },
      {
        "name": "reduceAll",
        "line": 571
      },
      {
        "name": "parseSSEChunk",
        "line": 582
      }
    ],
    "Calls": [
      "initialStreamState",
      "reduceStream"
    ],
    "Called by": [
      "api.js",
      "App.jsx"
    ],
    "Data read": [
      "response events"
    ],
    "Data written": [
      "text/activity/tool state"
    ],
    "External dependencies": [
      "JavaScript"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/platform/host.ts",
    "Responsibility": "Host abstraction over desktop IPC and browser fallbacks",
    "Important classes": [],
    "Important functions": [
      {
        "name": "getPlatform",
        "line": 30
      },
      {
        "name": "isMac",
        "line": 38
      },
      {
        "name": "getApiOrigin",
        "line": 47
      },
      {
        "name": "isLocalApiOrigin",
        "line": 64
      },
      {
        "name": "getOAuthRedirectUri",
        "line": 81
      },
      {
        "name": "serverInfo",
        "line": 99
      },
      {
        "name": "serverStart",
        "line": 117
      },
      {
        "name": "serverStop",
        "line": 124
      },
      {
        "name": "serverDiagnostics",
        "line": 141
      },
      {
        "name": "openExternal",
        "line": 158
      },
      {
        "name": "openPath",
        "line": 166
      },
      {
        "name": "showItemInFolder",
        "line": 173
      },
      {
        "name": "getPathForFile",
        "line": 185
      },
      {
        "name": "getUIVersion",
        "line": 198
      },
      {
        "name": "fetchJson",
        "line": 216
      },
      {
        "name": "readSettings",
        "line": 229
      },
      {
        "name": "saveSettings",
        "line": 236
      },
      {
        "name": "restartServer",
        "line": 244
      },
      {
        "name": "checkInstall",
        "line": 257
      },
      {
        "name": "checkConfigured",
        "line": 264
      },
      {
        "name": "validateProvider",
        "line": 271
      },
      {
        "name": "startInstall",
        "line": 299
      },
      {
        "name": "cancelInstall",
        "line": 305
      },
      {
        "name": "onInstallProgress",
        "line": 311
      },
      {
        "name": "onInstallLog",
        "line": 322
      },
      {
        "name": "onInstallDone",
        "line": 330
      },
      {
        "name": "onInstallError",
        "line": 340
      },
      {
        "name": "onInstallCancelled",
        "line": 347
      },
      {
        "name": "onUpdateStatus",
        "line": 363
      },
      {
        "name": "applyUpdate",
        "line": 370
      },
      {
        "name": "oauthConnect",
        "line": 402
      },
      {
        "name": "oauthCancel",
        "line": 412
      },
      {
        "name": "mindshubLogin",
        "line": 431
      },
      {
        "name": "mindshubRefresh",
        "line": 438
      },
      {
        "name": "mindshubFinalize",
        "line": 445
      },
      {
        "name": "mindshubGetCachedToken",
        "line": 452
      },
      {
        "name": "getAccessToken",
        "line": 460
      },
      {
        "name": "logout",
        "line": 473
      }
    ],
    "Calls": [
      "host bridge methods"
    ],
    "Called by": [
      "renderer components"
    ],
    "Data read": [
      "window.antontron",
      "browser origin"
    ],
    "Data written": [
      "IPC/HTTP operations"
    ],
    "External dependencies": [
      "Electron bridge",
      "browser APIs"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/cowork/components/artifact/ArtifactViewer.jsx",
    "Responsibility": "Render text, documents and sandboxed artifact previews",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_extOfPath",
        "line": 30
      },
      {
        "name": "_isTextArtifact",
        "line": 36
      },
      {
        "name": "_parseCsv",
        "line": 54
      },
      {
        "name": "_countCsvRows",
        "line": 91
      },
      {
        "name": "_csvRowsToGfmTable",
        "line": 113
      },
      {
        "name": "PathRow",
        "line": 150
      },
      {
        "name": "AccessPasswordRow",
        "line": 256
      },
      {
        "name": "ActionsPopover",
        "line": 292
      },
      {
        "name": "ArtifactViewer",
        "line": 374
      }
    ],
    "Calls": [
      "artifact API",
      "iframe"
    ],
    "Called by": [
      "cowork artifact views"
    ],
    "Data read": [
      "artifact records",
      "HTTP content"
    ],
    "Data written": [
      "preview state"
    ],
    "External dependencies": [
      "React",
      "browser iframe"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/main/index.ts",
    "Responsibility": "Electron application and privileged IPC lifecycle",
    "Important classes": [],
    "Important functions": [
      {
        "name": "getAntonEnvPath",
        "line": 18
      },
      {
        "name": "getCoworkStatePath",
        "line": 22
      },
      {
        "name": "readEnvFile",
        "line": 26
      },
      {
        "name": "clearStoredProviderState",
        "line": 42
      },
      {
        "name": "getDevMode",
        "line": 72
      },
      {
        "name": "getUpdateMode",
        "line": 81
      },
      {
        "name": "checkConfigured",
        "line": 86
      },
      {
        "name": "httpRequest",
        "line": 96
      },
      {
        "name": "validateAnthropic",
        "line": 129
      },
      {
        "name": "validateMinds",
        "line": 158
      },
      {
        "name": "validateOpenAICompatible",
        "line": 185
      },
      {
        "name": "getProjectsDir",
        "line": 225
      },
      {
        "name": "ensureProjectsDir",
        "line": 230
      },
      {
        "name": "ensureDefaultProject",
        "line": 237
      },
      {
        "name": "getIconPath",
        "line": 250
      },
      {
        "name": "createWindow",
        "line": 260
      },
      {
        "name": "setupIPC",
        "line": 388
      },
      {
        "name": "drainServerForQuit",
        "line": 964
      }
    ],
    "Calls": [
      "startServer",
      "IPC handlers",
      "BrowserWindow"
    ],
    "Called by": [
      "Electron package main"
    ],
    "Data read": [
      "configuration",
      "tokens",
      "install state"
    ],
    "Data written": [
      "window/process/OS operations"
    ],
    "External dependencies": [
      "Electron",
      "Node"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/main/preload.ts",
    "Responsibility": "Expose named desktop capabilities to isolated renderer",
    "Important classes": [],
    "Important functions": [],
    "Calls": [
      "contextBridge",
      "ipcRenderer"
    ],
    "Called by": [
      "BrowserWindow preload"
    ],
    "Data read": [
      "IPC replies"
    ],
    "Data written": [
      "IPC requests"
    ],
    "External dependencies": [
      "Electron"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/main/server-process.ts",
    "Responsibility": "Start, inspect and stop local API subprocess",
    "Important classes": [],
    "Important functions": [
      {
        "name": "appendStderr",
        "line": 52
      },
      {
        "name": "getServerLogPath",
        "line": 63
      },
      {
        "name": "openLogStream",
        "line": 72
      },
      {
        "name": "writeLog",
        "line": 86
      },
      {
        "name": "killTree",
        "line": 94
      },
      {
        "name": "killProcessOnPort",
        "line": 104
      },
      {
        "name": "getServerPort",
        "line": 123
      },
      {
        "name": "getServerOrigin",
        "line": 127
      },
      {
        "name": "getUvPath",
        "line": 131
      },
      {
        "name": "getEnvPath",
        "line": 145
      },
      {
        "name": "getDevServerDir",
        "line": 156
      },
      {
        "name": "getCoworkServerBin",
        "line": 167
      },
      {
        "name": "probeHealth",
        "line": 178
      },
      {
        "name": "startServer",
        "line": 205
      },
      {
        "name": "stopServer",
        "line": 386
      },
      {
        "name": "isServerRunning",
        "line": 455
      },
      {
        "name": "isServerStarting",
        "line": 464
      },
      {
        "name": "getServerDiagnostics",
        "line": 490
      }
    ],
    "Calls": [
      "startServer",
      "stopServer"
    ],
    "Called by": [
      "main index"
    ],
    "Data read": [
      "install/runtime paths",
      "health",
      "process output"
    ],
    "Data written": [
      "child process",
      "logs"
    ],
    "External dependencies": [
      "Node child_process",
      "HTTP"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/main/minds-auth.ts",
    "Responsibility": "Desktop identity, refresh, organization and inference-key setup",
    "Important classes": [],
    "Important functions": [
      {
        "name": "timedFetch",
        "line": 35
      },
      {
        "name": "envHasMindsCommitted",
        "line": 43
      },
      {
        "name": "refreshTokensOnly",
        "line": 55
      },
      {
        "name": "silentRefresh",
        "line": 81
      },
      {
        "name": "endKeycloakSession",
        "line": 97
      },
      {
        "name": "decodeJwtPayload",
        "line": 131
      },
      {
        "name": "normalizeOrgRef",
        "line": 145
      },
      {
        "name": "getActiveOrgFromPayload",
        "line": 157
      },
      {
        "name": "hasActiveOrgClaim",
        "line": 175
      },
      {
        "name": "pushUniqueOrg",
        "line": 179
      },
      {
        "name": "getCurrentActiveOrg",
        "line": 185
      },
      {
        "name": "listUserOrgs",
        "line": 204
      },
      {
        "name": "listOrgCandidates",
        "line": 222
      },
      {
        "name": "switchActiveOrg",
        "line": 238
      },
      {
        "name": "ensureActiveOrg",
        "line": 271
      },
      {
        "name": "listExistingKeys",
        "line": 331
      },
      {
        "name": "deleteKeyByPrefix",
        "line": 346
      },
      {
        "name": "fetchAuthContext",
        "line": 363
      },
      {
        "name": "canCreateApiKeys",
        "line": 388
      },
      {
        "name": "normalizeHubEntitlements",
        "line": 392
      },
      {
        "name": "requiresHubUpgrade",
        "line": 410
      },
      {
        "name": "canUseAntonWithMinds",
        "line": 418
      },
      {
        "name": "provisionAntonApiKey",
        "line": 422
      },
      {
        "name": "writeMindsKeyToEnvAndRestart",
        "line": 558
      },
      {
        "name": "scheduleRefresh",
        "line": 613
      }
    ],
    "Calls": [
      "refreshTokensOnly",
      "silentRefresh",
      "token-store"
    ],
    "Called by": [
      "main IPC"
    ],
    "Data read": [
      "OAuth tokens",
      "identity API"
    ],
    "Data written": [
      "token state",
      "provider configuration"
    ],
    "External dependencies": [
      "Keycloak",
      "external auth service"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/main/token-store.ts",
    "Responsibility": "Store access token in memory and encrypted refresh token on disk",
    "Important classes": [],
    "Important functions": [
      {
        "name": "saveTokens",
        "line": 10
      },
      {
        "name": "getAccessToken",
        "line": 18
      },
      {
        "name": "isAccessTokenExpired",
        "line": 20
      },
      {
        "name": "getRefreshToken",
        "line": 24
      },
      {
        "name": "clearTokens",
        "line": 33
      }
    ],
    "Calls": [
      "saveTokens",
      "getRefreshToken",
      "clearTokens"
    ],
    "Called by": [
      "minds-auth",
      "main"
    ],
    "Data read": [
      "mindshub-refresh.bin"
    ],
    "Data written": [
      "memory",
      "encrypted refresh file"
    ],
    "External dependencies": [
      "Electron safeStorage",
      "fs"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/src/renderer/vite.config.ts",
    "Responsibility": "Web/desktop build entries, output directories and dev proxy",
    "Important classes": [],
    "Important functions": [],
    "Calls": [
      "defineConfig"
    ],
    "Called by": [
      "Vite CLI"
    ],
    "Data read": [
      "environment",
      "package.json",
      "Git hash"
    ],
    "Data written": [
      "Vite configuration/build outputs"
    ],
    "External dependencies": [
      "Vite",
      "React plugin",
      "Node"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Frontend",
    "File": "frontend/scripts/start-server.mjs",
    "Responsibility": "Browser helper backend launch and readiness",
    "Important classes": [],
    "Important functions": [
      {
        "name": "getServerDir",
        "line": 30
      },
      {
        "name": "getUvPath",
        "line": 37
      },
      {
        "name": "getEnvPath",
        "line": 47
      },
      {
        "name": "probeHealth",
        "line": 55
      },
      {
        "name": "start",
        "line": 77
      },
      {
        "name": "stop",
        "line": 136
      },
      {
        "name": "isRunning",
        "line": 155
      },
      {
        "name": "onUnexpectedExit",
        "line": 159
      }
    ],
    "Calls": [
      "start",
      "stop",
      "getServerDir"
    ],
    "Called by": [
      "dev-web.mjs"
    ],
    "Data read": [
      "COWORK_SERVER_DIR",
      "health"
    ],
    "Data written": [
      "API child process"
    ],
    "External dependencies": [
      "uv",
      "Node child_process"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  }
]
```

## Core API

```json
[
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/server.py",
    "Responsibility": "ASGI app, CORS, router and lifespan",
    "Important classes": [],
    "Important functions": [
      {
        "name": "lifespan",
        "line": 25
      },
      {
        "name": "create_app",
        "line": 52
      },
      {
        "name": "_install_channels",
        "line": 90
      }
    ],
    "Calls": [
      "create_app",
      "lifespan",
      "run_dev_setup",
      "start_scheduler"
    ],
    "Called by": [
      "Uvicorn"
    ],
    "Data read": [
      "application settings",
      "channel config"
    ],
    "Data written": [
      "app state",
      "scheduler/adapter tasks"
    ],
    "External dependencies": [
      "FastAPI"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/api/v1/router.py",
    "Responsibility": "Canonical domain and compatibility route registration",
    "Important classes": [],
    "Important functions": [],
    "Calls": [
      "include_router"
    ],
    "Called by": [
      "create_app"
    ],
    "Data read": [
      "endpoint routers"
    ],
    "Data written": [
      "route table"
    ],
    "External dependencies": [
      "FastAPI"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "Responsibility": "Response streaming endpoint and in-flight/cancel status",
    "Important classes": [
      {
        "name": "CancelRequest",
        "line": 114
      }
    ],
    "Important functions": [
      {
        "name": "mark_stream_active",
        "line": 34
      },
      {
        "name": "mark_stream_finished",
        "line": 41
      },
      {
        "name": "get_active_stream_ids",
        "line": 46
      },
      {
        "name": "request_cancel",
        "line": 51
      },
      {
        "name": "options_handler",
        "line": 61
      },
      {
        "name": "responses",
        "line": 73
      },
      {
        "name": "in_flight_list",
        "line": 102
      },
      {
        "name": "in_flight",
        "line": 108
      },
      {
        "name": "cancel_response",
        "line": 119
      },
      {
        "name": "tail_response",
        "line": 126
      }
    ],
    "Calls": [
      "ResponsesHandler.handle",
      "tracked_stream"
    ],
    "Called by": [
      "API router",
      "scheduler status helpers"
    ],
    "Data read": [
      "ResponsesRequest",
      "DB session"
    ],
    "Data written": [
      "process-local active stream map"
    ],
    "External dependencies": [
      "FastAPI",
      "asyncio"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/handlers/responses.py",
    "Responsibility": "Resolve conversation/input and persist completed harness response",
    "Important classes": [
      {
        "name": "ResponsesHandler",
        "line": 36
      }
    ],
    "Important functions": [
      {
        "name": "ResponsesHandler.__init__",
        "line": 37
      },
      {
        "name": "ResponsesHandler.handle",
        "line": 42
      },
      {
        "name": "ResponsesHandler._stream",
        "line": 117
      },
      {
        "name": "ResponsesHandler._collect",
        "line": 156
      },
      {
        "name": "ResponsesHandler._save_assistant_turn",
        "line": 183
      },
      {
        "name": "ResponsesHandler._build_harness_input",
        "line": 194
      },
      {
        "name": "ResponsesHandler._relink_attachments",
        "line": 236
      },
      {
        "name": "ResponsesHandler._resolve_project_id",
        "line": 256
      },
      {
        "name": "ResponsesHandler._image_block",
        "line": 267
      },
      {
        "name": "ResponsesHandler._prompt_text",
        "line": 279
      },
      {
        "name": "ResponsesHandler._extract_original_content",
        "line": 283
      },
      {
        "name": "ResponsesHandler._build_output",
        "line": 296
      }
    ],
    "Calls": [
      "get_harness",
      "stream_response",
      "save_assistant_turn"
    ],
    "Called by": [
      "responses endpoint",
      "scheduler"
    ],
    "Data read": [
      "request",
      "prior messages",
      "files",
      "settings"
    ],
    "Data written": [
      "user/assistant messages",
      "events"
    ],
    "External dependencies": [
      "SQLModel",
      "FastAPI"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/harnesses/base.py",
    "Responsibility": "Harness protocol and registry",
    "Important classes": [
      {
        "name": "TextInputBlock",
        "line": 13
      },
      {
        "name": "FileInputBlock",
        "line": 18
      },
      {
        "name": "MemoryItem",
        "line": 24
      },
      {
        "name": "HarnessProvider",
        "line": 31
      }
    ],
    "Important functions": [
      {
        "name": "HarnessProvider.stream_response",
        "line": 36
      },
      {
        "name": "HarnessProvider.sync_skills",
        "line": 46
      },
      {
        "name": "HarnessProvider.overwrite_memory",
        "line": 51
      },
      {
        "name": "HarnessProvider.retrieve_memory",
        "line": 60
      },
      {
        "name": "HarnessProvider.delete_memory",
        "line": 68
      },
      {
        "name": "HarnessProvider.list_memory",
        "line": 76
      },
      {
        "name": "register",
        "line": 86
      },
      {
        "name": "get_harness",
        "line": 91
      }
    ],
    "Calls": [
      "register",
      "get_harness"
    ],
    "Called by": [
      "settings and handlers"
    ],
    "Data read": [
      "harness name"
    ],
    "Data written": [
      "registered classes"
    ],
    "External dependencies": [
      "Python typing"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/harnesses/anton_harness/harness.py",
    "Responsibility": "Adapt API project/history/settings to Anton session",
    "Important classes": [
      {
        "name": "AntonMemoryCategory",
        "line": 36
      },
      {
        "name": "AntonHarness",
        "line": 43
      }
    ],
    "Important functions": [
      {
        "name": "_build_filtered_vault",
        "line": 25
      },
      {
        "name": "AntonHarness.sync_skills",
        "line": 48
      },
      {
        "name": "AntonHarness.overwrite_memory",
        "line": 75
      },
      {
        "name": "AntonHarness._write_to_global_memory",
        "line": 85
      },
      {
        "name": "AntonHarness._write_to_project_memory",
        "line": 92
      },
      {
        "name": "AntonHarness._resolve_memory_path",
        "line": 99
      },
      {
        "name": "AntonHarness.retrieve_memory",
        "line": 108
      },
      {
        "name": "AntonHarness._read_from_global_memory",
        "line": 118
      },
      {
        "name": "AntonHarness._read_from_project_memory",
        "line": 125
      },
      {
        "name": "AntonHarness.list_memory",
        "line": 132
      },
      {
        "name": "AntonHarness.delete_memory",
        "line": 145
      },
      {
        "name": "AntonHarness._delete_global_memory",
        "line": 153
      },
      {
        "name": "AntonHarness._delete_project_memory",
        "line": 159
      },
      {
        "name": "AntonHarness.stream_response",
        "line": 165
      },
      {
        "name": "AntonHarness._to_anton_input",
        "line": 185
      },
      {
        "name": "AntonHarness._build_chat_session",
        "line": 201
      },
      {
        "name": "AntonHarness._build_llm_client",
        "line": 421
      }
    ],
    "Calls": [
      "ChatSession",
      "LLMClient factory",
      "Cortex",
      "turn_stream"
    ],
    "Called by": [
      "ResponsesHandler",
      "channel runtime"
    ],
    "Data read": [
      "DB conversation",
      "provider settings",
      "local vault",
      "skills"
    ],
    "Data written": [
      "workspace/memory/skills",
      "DS_* environment",
      "temporary filtered vault"
    ],
    "External dependencies": [
      "anton-agent"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/harnesses/anton_harness/stream_formatter.py",
    "Responsibility": "Translate Anton stream events into response SSE",
    "Important classes": [],
    "Important functions": [
      {
        "name": "format_responses_stream",
        "line": 43
      }
    ],
    "Calls": [
      "format_responses_stream"
    ],
    "Called by": [
      "ResponsesHandler through harness formatter"
    ],
    "Data read": [
      "Anton event iterator"
    ],
    "Data written": [
      "formatted events",
      "event sink"
    ],
    "External dependencies": [
      "Anton event classes"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/harnesses/hermes_harness/harness.py",
    "Responsibility": "Adapt cowork settings, history, memory and skills to Hermes",
    "Important classes": [
      {
        "name": "HermesMemoryCategory",
        "line": 96
      },
      {
        "name": "HermesHarness",
        "line": 102
      }
    ],
    "Important functions": [
      {
        "name": "_sync_hermes_config",
        "line": 40
      },
      {
        "name": "_build_datasource_context",
        "line": 66
      },
      {
        "name": "HermesHarness.sync_skills",
        "line": 107
      },
      {
        "name": "HermesHarness.overwrite_memory",
        "line": 144
      },
      {
        "name": "HermesHarness.retrieve_memory",
        "line": 152
      },
      {
        "name": "HermesHarness.delete_memory",
        "line": 161
      },
      {
        "name": "HermesHarness.list_memory",
        "line": 169
      },
      {
        "name": "HermesHarness._resolve_memory_path",
        "line": 179
      },
      {
        "name": "HermesHarness.stream_response",
        "line": 185
      },
      {
        "name": "HermesHarness._to_prompt_string",
        "line": 260
      },
      {
        "name": "HermesHarness._run",
        "line": 272
      }
    ],
    "Calls": [
      "AIAgent",
      "get_user_settings"
    ],
    "Called by": [
      "ResponsesHandler",
      "channel runtime"
    ],
    "Data read": [
      "conversation",
      "user settings",
      "vault"
    ],
    "Data written": [
      "Hermes home/config",
      "stream events"
    ],
    "External dependencies": [
      "external hermes-agent"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/providers.py",
    "Responsibility": "Construct planning/coding providers and fetch/validate catalogs",
    "Important classes": [],
    "Important functions": [
      {
        "name": "minds_chat_base_url",
        "line": 19
      },
      {
        "name": "fetch_minds_models",
        "line": 48
      },
      {
        "name": "check_config_status",
        "line": 101
      },
      {
        "name": "ping_provider",
        "line": 114
      },
      {
        "name": "ping_providers",
        "line": 161
      },
      {
        "name": "validate_anthropic",
        "line": 178
      },
      {
        "name": "validate_minds",
        "line": 195
      },
      {
        "name": "validate_openai_compatible",
        "line": 210
      },
      {
        "name": "validate_provider",
        "line": 232
      },
      {
        "name": "build_llm_client",
        "line": 245
      },
      {
        "name": "resolve_stored_key",
        "line": 293
      }
    ],
    "Calls": [
      "build_llm_client",
      "fetch_minds_models",
      "ping_provider"
    ],
    "Called by": [
      "harnesses",
      "settings endpoints",
      "probe"
    ],
    "Data read": [
      "saved keys/model settings",
      "remote model list"
    ],
    "Data written": [
      "model-list cache",
      "provider requests"
    ],
    "External dependencies": [
      "httpx",
      "Anton providers"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/settings.py",
    "Responsibility": "Validate settings, encrypt secrets and invalidate cached settings",
    "Important classes": [
      {
        "name": "SettingService",
        "line": 15
      }
    ],
    "Important functions": [
      {
        "name": "SettingService.__init__",
        "line": 16
      },
      {
        "name": "SettingService._fetch_row",
        "line": 19
      },
      {
        "name": "SettingService._fetch_all_rows",
        "line": 22
      },
      {
        "name": "SettingService._validate_key",
        "line": 26
      },
      {
        "name": "SettingService._load",
        "line": 31
      },
      {
        "name": "SettingService._to_response",
        "line": 40
      },
      {
        "name": "SettingService.load",
        "line": 59
      },
      {
        "name": "SettingService.list_settings",
        "line": 62
      },
      {
        "name": "SettingService.get_setting",
        "line": 68
      },
      {
        "name": "SettingService.upsert_setting",
        "line": 74
      },
      {
        "name": "SettingService.bulk_upsert",
        "line": 101
      },
      {
        "name": "SettingService.delete_setting",
        "line": 139
      }
    ],
    "Calls": [
      "encrypt",
      "decrypt",
      "invalidate_user_settings_cache"
    ],
    "Called by": [
      "settings API",
      "bootstrap"
    ],
    "Data read": [
      "Setting rows"
    ],
    "Data written": [
      "Setting rows"
    ],
    "External dependencies": [
      "SQLModel",
      "Pydantic",
      "Fernet"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/db/session.py",
    "Responsibility": "SQLAlchemy engines and FastAPI SQLModel session dependencies",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_create_engine",
        "line": 18
      },
      {
        "name": "get_engine",
        "line": 42
      },
      {
        "name": "get_session_factory",
        "line": 56
      },
      {
        "name": "get_session",
        "line": 77
      },
      {
        "name": "get_open_session",
        "line": 113
      }
    ],
    "Calls": [
      "get_engine",
      "get_session",
      "get_open_session"
    ],
    "Called by": [
      "API endpoints and services"
    ],
    "Data read": [
      "database URI"
    ],
    "Data written": [
      "engine/factory caches",
      "transaction lifecycle"
    ],
    "External dependencies": [
      "SQLAlchemy",
      "SQLModel"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/dev_setup.py",
    "Responsibility": "Apply migrations, seed General project and migrate old settings",
    "Important classes": [],
    "Important functions": [
      {
        "name": "run_dev_setup",
        "line": 20
      }
    ],
    "Calls": [
      "run_schema_migrations",
      "migrate_env_to_db"
    ],
    "Called by": [
      "server lifespan",
      "CLI"
    ],
    "Data read": [
      "DB URI",
      "existing schema",
      "legacy settings"
    ],
    "Data written": [
      "schema",
      "General row/directory",
      "settings"
    ],
    "External dependencies": [
      "SQLAlchemy",
      "SQLModel"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/conversations.py",
    "Responsibility": "Conversation/message/event persistence and history projection",
    "Important classes": [
      {
        "name": "ConversationService",
        "line": 14
      }
    ],
    "Important functions": [
      {
        "name": "ConversationService.__init__",
        "line": 15
      },
      {
        "name": "ConversationService.list_conversations",
        "line": 18
      },
      {
        "name": "ConversationService.get_conversation",
        "line": 30
      },
      {
        "name": "ConversationService.create_conversation",
        "line": 36
      },
      {
        "name": "ConversationService.project_by_name",
        "line": 56
      },
      {
        "name": "ConversationService.update_conversation",
        "line": 61
      },
      {
        "name": "ConversationService.delete_conversation",
        "line": 79
      },
      {
        "name": "ConversationService.delete_turn",
        "line": 98
      },
      {
        "name": "ConversationService.save_assistant_turn",
        "line": 139
      },
      {
        "name": "ConversationService.get_messages",
        "line": 168
      }
    ],
    "Calls": [
      "save_assistant_turn",
      "get_messages"
    ],
    "Called by": [
      "response handler",
      "conversation API",
      "channels"
    ],
    "Data read": [
      "Conversation",
      "Message",
      "MessageEvent"
    ],
    "Data written": [
      "same tables"
    ],
    "External dependencies": [
      "SQLModel"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/files.py",
    "Responsibility": "Uploaded bytes and File metadata lifecycle",
    "Important classes": [
      {
        "name": "FileService",
        "line": 23
      }
    ],
    "Important functions": [
      {
        "name": "attachment_purpose",
        "line": 15
      },
      {
        "name": "FileService.__init__",
        "line": 24
      },
      {
        "name": "FileService._root_dir",
        "line": 27
      },
      {
        "name": "FileService._to_response",
        "line": 30
      },
      {
        "name": "FileService.list_files",
        "line": 39
      },
      {
        "name": "FileService.list_file_rows",
        "line": 45
      },
      {
        "name": "FileService.get_file_row",
        "line": 51
      },
      {
        "name": "FileService.relink_purpose",
        "line": 54
      },
      {
        "name": "FileService.get_file",
        "line": 66
      },
      {
        "name": "FileService.create_file",
        "line": 72
      },
      {
        "name": "FileService.create_file_from_bytes",
        "line": 94
      },
      {
        "name": "FileService._get_file_model",
        "line": 115
      },
      {
        "name": "FileService.delete_file",
        "line": 121
      },
      {
        "name": "FileService.get_file_content",
        "line": 132
      }
    ],
    "Calls": [
      "create_file",
      "get_file_content",
      "relink_purpose"
    ],
    "Called by": [
      "files API",
      "response handler",
      "channels"
    ],
    "Data read": [
      "UploadFile",
      "file paths and rows"
    ],
    "Data written": [
      "file bytes",
      "File rows"
    ],
    "External dependencies": [
      "FastAPI",
      "SQLModel",
      "filesystem"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/artifacts.py",
    "Responsibility": "Discover artifacts, validate paths and mount/launch previews",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_human_mtime",
        "line": 86
      },
      {
        "name": "_projects_root",
        "line": 94
      },
      {
        "name": "_registered_project_dirs",
        "line": 98
      },
      {
        "name": "_scan_artifact_dirs",
        "line": 119
      },
      {
        "name": "_iter_artifact_folders",
        "line": 129
      },
      {
        "name": "_load_metadata",
        "line": 160
      },
      {
        "name": "_user_files",
        "line": 169
      },
      {
        "name": "_pick_primary",
        "line": 190
      },
      {
        "name": "_load_published_map",
        "line": 211
      },
      {
        "name": "_published_url_for",
        "line": 223
      },
      {
        "name": "_published_access_for",
        "line": 232
      },
      {
        "name": "_project_artifacts_base",
        "line": 257
      },
      {
        "name": "serve_url_for",
        "line": 277
      },
      {
        "name": "_candidate_relative_artifacts",
        "line": 298
      },
      {
        "name": "resolve_artifact_path",
        "line": 319
      },
      {
        "name": "_artifact_root_for",
        "line": 361
      },
      {
        "name": "_fullstack_types",
        "line": 387
      },
      {
        "name": "_unpublish_folder",
        "line": 400
      },
      {
        "name": "delete_artifact",
        "line": 427
      },
      {
        "name": "reveal_in_file_manager",
        "line": 459
      },
      {
        "name": "list_artifacts",
        "line": 470
      },
      {
        "name": "preview_artifact",
        "line": 525
      },
      {
        "name": "mount_preview",
        "line": 540
      },
      {
        "name": "get_preview_mount",
        "line": 620
      },
      {
        "name": "html_artifacts",
        "line": 624
      },
      {
        "name": "_launch_lock",
        "line": 687
      },
      {
        "name": "_probe_port",
        "line": 695
      },
      {
        "name": "_resolve_project_root",
        "line": 704
      },
      {
        "name": "_ensure_backend_running",
        "line": 724
      },
      {
        "name": "_launch_backend_locked",
        "line": 748
      },
      {
        "name": "shutdown_launched_backends",
        "line": 847
      }
    ],
    "Calls": [
      "resolve_artifact_path",
      "list_artifacts",
      "mount_preview"
    ],
    "Called by": [
      "artifact API",
      "publish",
      "channels"
    ],
    "Data read": [
      "project directories",
      "artifact metadata"
    ],
    "Data written": [
      "preview mounts",
      "backend process maps"
    ],
    "External dependencies": [
      "Anton artifact launcher",
      "filesystem"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/publish.py",
    "Responsibility": "Validate and publish artifact; retain publication metadata",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_cowork_state_dir",
        "line": 32
      },
      {
        "name": "_state_path",
        "line": 42
      },
      {
        "name": "_load_state",
        "line": 46
      },
      {
        "name": "_save_state",
        "line": 57
      },
      {
        "name": "_secret_str",
        "line": 69
      },
      {
        "name": "_utc_now_iso",
        "line": 78
      },
      {
        "name": "_resolve_publish_target",
        "line": 82
      },
      {
        "name": "list_publishable",
        "line": 118
      },
      {
        "name": "publish_artifact",
        "line": 129
      },
      {
        "name": "unpublish_artifact",
        "line": 226
      }
    ],
    "Calls": [
      "publish_artifact",
      "anton.publisher.publish"
    ],
    "Called by": [
      "publish endpoint",
      "harness tool"
    ],
    "Data read": [
      "artifact files",
      "Minds key",
      "vault"
    ],
    "Data written": [
      "external publication",
      ".published.json",
      "state history"
    ],
    "External dependencies": [
      "external publisher"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/scheduler.py",
    "Responsibility": "Poll due schedules and execute agent requests",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_advance_next_run_at",
        "line": 25
      },
      {
        "name": "_handle_missed_runs",
        "line": 47
      },
      {
        "name": "execute_schedule",
        "line": 84
      },
      {
        "name": "_scheduler_loop",
        "line": 158
      },
      {
        "name": "start_scheduler",
        "line": 185
      }
    ],
    "Calls": [
      "execute_schedule",
      "ResponsesHandler.handle"
    ],
    "Called by": [
      "server lifespan",
      "schedule API"
    ],
    "Data read": [
      "Schedule records"
    ],
    "Data written": [
      "ScheduleRun",
      "conversation results",
      "next run state"
    ],
    "External dependencies": [
      "asyncio",
      "SQLModel"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/channels/runtime.py",
    "Responsibility": "Route channel turns to harnesses and persist replies",
    "Important classes": [
      {
        "name": "_KeyedLocks",
        "line": 96
      },
      {
        "name": "LiveAdapterRegistry",
        "line": 124
      },
      {
        "name": "AntonChannelRuntime",
        "line": 185
      }
    ],
    "Important functions": [
      {
        "name": "turn_used_tools",
        "line": 46
      },
      {
        "name": "artifacts_since",
        "line": 58
      },
      {
        "name": "typing_loop",
        "line": 76
      },
      {
        "name": "conversation_link",
        "line": 85
      },
      {
        "name": "_KeyedLocks.__init__",
        "line": 100
      },
      {
        "name": "_KeyedLocks.acquire",
        "line": 106
      },
      {
        "name": "LiveAdapterRegistry.__init__",
        "line": 128
      },
      {
        "name": "LiveAdapterRegistry.get",
        "line": 132
      },
      {
        "name": "LiveAdapterRegistry.refresh",
        "line": 136
      },
      {
        "name": "LiveAdapterRegistry.refresh_all",
        "line": 160
      },
      {
        "name": "LiveAdapterRegistry.remove",
        "line": 167
      },
      {
        "name": "LiveAdapterRegistry.shutdown",
        "line": 176
      },
      {
        "name": "AntonChannelRuntime.__init__",
        "line": 188
      },
      {
        "name": "AntonChannelRuntime._lock_key",
        "line": 199
      },
      {
        "name": "AntonChannelRuntime.handle",
        "line": 203
      },
      {
        "name": "AntonChannelRuntime._handle_locked",
        "line": 211
      },
      {
        "name": "AntonChannelRuntime._resolve_or_create_binding",
        "line": 258
      },
      {
        "name": "AntonChannelRuntime._should_respond",
        "line": 285
      },
      {
        "name": "AntonChannelRuntime._ensure_conversation",
        "line": 301
      },
      {
        "name": "AntonChannelRuntime._touch_channel_session",
        "line": 317
      },
      {
        "name": "AntonChannelRuntime.resolve_turn_harness",
        "line": 340
      },
      {
        "name": "AntonChannelRuntime._run_anton",
        "line": 355
      },
      {
        "name": "AntonChannelRuntime._event_text",
        "line": 398
      },
      {
        "name": "AntonChannelRuntime.build_input_blocks",
        "line": 402
      },
      {
        "name": "AntonChannelRuntime.send_turn_artifacts",
        "line": 431
      },
      {
        "name": "AntonChannelRuntime._deliver",
        "line": 446
      }
    ],
    "Calls": [
      "get_harness",
      "FileService",
      "ConversationService"
    ],
    "Called by": [
      "channel ingress/webhooks"
    ],
    "Data read": [
      "channel binding/session",
      "credentials",
      "attachments"
    ],
    "Data written": [
      "conversation/message/event state",
      "adapter output"
    ],
    "External dependencies": [
      "Anton dispatch types",
      "channel SDKs"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/connectors/specs/_registry.py",
    "Responsibility": "Load/search connector form definitions",
    "Important classes": [
      {
        "name": "ConnectorSpecRegistry",
        "line": 14
      }
    ],
    "Important functions": [
      {
        "name": "ConnectorSpecRegistry.__init__",
        "line": 15
      },
      {
        "name": "ConnectorSpecRegistry._load_all",
        "line": 19
      },
      {
        "name": "ConnectorSpecRegistry.get_connectors",
        "line": 35
      },
      {
        "name": "ConnectorSpecRegistry.get_connector",
        "line": 40
      },
      {
        "name": "ConnectorSpecRegistry.list_connectors",
        "line": 46
      },
      {
        "name": "ConnectorSpecRegistry._to_connector_spec_response",
        "line": 64
      },
      {
        "name": "ConnectorSpecRegistry.reload",
        "line": 79
      },
      {
        "name": "ConnectorSpecRegistry._normalize",
        "line": 83
      },
      {
        "name": "ConnectorSpecRegistry._exact_match",
        "line": 86
      },
      {
        "name": "ConnectorSpecRegistry._token_score",
        "line": 98
      },
      {
        "name": "ConnectorSpecRegistry.match_connector",
        "line": 117
      }
    ],
    "Calls": [
      "registry methods"
    ],
    "Called by": [
      "connector specs API",
      "tools",
      "probe"
    ],
    "Data read": [
      "connector JSON files"
    ],
    "Data written": [
      "in-memory registry"
    ],
    "External dependencies": [
      "Pydantic connector schemas"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/api/v1/endpoints/connectors/submissions.py",
    "Responsibility": "Validate credential forms and start streamed probe",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_resolve_fields",
        "line": 24
      },
      {
        "name": "_fields_from_spec_dict",
        "line": 35
      },
      {
        "name": "_missing_required",
        "line": 57
      },
      {
        "name": "submit_form",
        "line": 68
      }
    ],
    "Calls": [
      "submit_form",
      "ProbeHandler.run"
    ],
    "Called by": [
      "frontend streamDataVaultSubmission"
    ],
    "Data read": [
      "form values/spec/method"
    ],
    "Data written": [
      "SubmissionStore staging"
    ],
    "External dependencies": [
      "FastAPI"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/handlers/probe.py",
    "Responsibility": "Credential probe lifecycle and saved-connection updates",
    "Important classes": [
      {
        "name": "ProbeHandler",
        "line": 25
      }
    ],
    "Important functions": [
      {
        "name": "ProbeHandler.__init__",
        "line": 26
      },
      {
        "name": "ProbeHandler.run",
        "line": 29
      },
      {
        "name": "ProbeHandler._build_llm_client",
        "line": 385
      },
      {
        "name": "ProbeHandler._save_assistant_turn",
        "line": 389
      }
    ],
    "Calls": [
      "CredentialProbe.run",
      "LocalDataVault.save"
    ],
    "Called by": [
      "submit_form endpoint"
    ],
    "Data read": [
      "staged raw values",
      "specs",
      "conversation"
    ],
    "Data written": [
      "vault records",
      "status/events/messages"
    ],
    "External dependencies": [
      "Anton",
      "SQLModel"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/connectors/probe.py",
    "Responsibility": "Build Anton-driven credential test with feedback tools",
    "Important classes": [
      {
        "name": "ProbeOutcome",
        "line": 27
      },
      {
        "name": "CredentialProbe",
        "line": 36
      }
    ],
    "Important functions": [
      {
        "name": "CredentialProbe.__init__",
        "line": 39
      },
      {
        "name": "CredentialProbe._set_status",
        "line": 60
      },
      {
        "name": "CredentialProbe._set_field_status",
        "line": 66
      },
      {
        "name": "CredentialProbe._remove_field",
        "line": 77
      },
      {
        "name": "CredentialProbe._switch_method",
        "line": 85
      },
      {
        "name": "CredentialProbe._report_success",
        "line": 93
      },
      {
        "name": "CredentialProbe._report_failure",
        "line": 98
      },
      {
        "name": "CredentialProbe._request_extra_field",
        "line": 104
      },
      {
        "name": "CredentialProbe._summarize_field_list",
        "line": 113
      },
      {
        "name": "CredentialProbe._summarize_form",
        "line": 135
      },
      {
        "name": "CredentialProbe._write_credentials_env",
        "line": 167
      },
      {
        "name": "CredentialProbe._build_prompt",
        "line": 189
      },
      {
        "name": "CredentialProbe.run",
        "line": 265
      }
    ],
    "Calls": [
      "CredentialProbe.run",
      "ChatSession"
    ],
    "Called by": [
      "ProbeHandler"
    ],
    "Data read": [
      "credentials",
      "form roster"
    ],
    "Data written": [
      "temporary env file",
      "feedback events"
    ],
    "External dependencies": [
      "Anton",
      "filesystem"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/connectors/connections.py",
    "Responsibility": "List/get/delete saved connections; mask secure_keys",
    "Important classes": [
      {
        "name": "ConnectionsService",
        "line": 11
      }
    ],
    "Important functions": [
      {
        "name": "ConnectionsService._vault",
        "line": 12
      },
      {
        "name": "ConnectionsService.list",
        "line": 17
      },
      {
        "name": "ConnectionsService.get",
        "line": 32
      },
      {
        "name": "ConnectionsService.delete",
        "line": 58
      }
    ],
    "Calls": [
      "ConnectionsService.get",
      "LocalDataVault"
    ],
    "Called by": [
      "connection endpoints"
    ],
    "Data read": [
      "LocalDataVault records"
    ],
    "Data written": [
      "vault deletions"
    ],
    "External dependencies": [
      "anton-agent"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core API",
    "File": "backend/core_api/cowork/services/connectors/submissions.py",
    "Responsibility": "Temporary credential submission staging",
    "Important classes": [
      {
        "name": "SubmissionStore",
        "line": 8
      }
    ],
    "Important functions": [
      {
        "name": "SubmissionStore.__init__",
        "line": 9
      },
      {
        "name": "SubmissionStore.stage",
        "line": 13
      },
      {
        "name": "SubmissionStore.get",
        "line": 39
      },
      {
        "name": "SubmissionStore.consume",
        "line": 46
      },
      {
        "name": "SubmissionStore._purge_expired",
        "line": 50
      }
    ],
    "Calls": [
      "stage",
      "get",
      "consume"
    ],
    "Called by": [
      "submission endpoint",
      "ProbeHandler"
    ],
    "Data read": [
      "form values"
    ],
    "Data written": [
      "24-hour TTL process dictionary"
    ],
    "External dependencies": [
      "Python stdlib"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  }
]
```

## Core Agent

```json
[
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/session.py",
    "Responsibility": "Prompt/model/tool orchestration, recovery and completion checks",
    "Important classes": [
      {
        "name": "ChatSessionConfig",
        "line": 87
      },
      {
        "name": "ChatSession",
        "line": 125
      }
    ],
    "Important functions": [
      {
        "name": "_extract_datasources",
        "line": 73
      },
      {
        "name": "ChatSession.__init__",
        "line": 128
      },
      {
        "name": "ChatSession.history",
        "line": 277
      },
      {
        "name": "ChatSession._apply_error_tracking",
        "line": 280
      },
      {
        "name": "ChatSession.repair_history",
        "line": 318
      },
      {
        "name": "ChatSession._persist_history",
        "line": 356
      },
      {
        "name": "ChatSession._coerce_to_block_list",
        "line": 394
      },
      {
        "name": "ChatSession._append_history",
        "line": 409
      },
      {
        "name": "ChatSession._validate_history_for_provider",
        "line": 457
      },
      {
        "name": "ChatSession._record_cell_explainability",
        "line": 498
      },
      {
        "name": "ChatSession._build_system_prompt",
        "line": 536
      },
      {
        "name": "ChatSession._build_tools",
        "line": 630
      },
      {
        "name": "ChatSession._build_core_tools",
        "line": 637
      },
      {
        "name": "ChatSession.close",
        "line": 694
      },
      {
        "name": "ChatSession._reap_tracked_backends",
        "line": 699
      },
      {
        "name": "ChatSession._summarize_history",
        "line": 720
      },
      {
        "name": "ChatSession._compact_scratchpads",
        "line": 826
      },
      {
        "name": "ChatSession._seal_dangling_tool_uses",
        "line": 834
      },
      {
        "name": "ChatSession.hard_truncate_history",
        "line": 934
      },
      {
        "name": "ChatSession.plan_with_recovery",
        "line": 987
      },
      {
        "name": "ChatSession.plan_stream_with_recovery",
        "line": 1043
      },
      {
        "name": "ChatSession._acc_observe",
        "line": 1101
      },
      {
        "name": "ChatSession._acc_maybe_nudge",
        "line": 1137
      },
      {
        "name": "ChatSession._schedule_acc_flush",
        "line": 1181
      },
      {
        "name": "ChatSession._schedule_cerebellum_flush",
        "line": 1236
      },
      {
        "name": "ChatSession.turn",
        "line": 1261
      },
      {
        "name": "ChatSession.turn_stream",
        "line": 1401
      },
      {
        "name": "ChatSession._stream_and_handle_tools",
        "line": 1564
      },
      {
        "name": "ChatSession._maybe_consolidate_scratchpads",
        "line": 2151
      },
      {
        "name": "ChatSession._consolidate",
        "line": 2161
      }
    ],
    "Calls": [
      "turn_stream",
      "_stream_and_handle_tools",
      "plan_stream_with_recovery"
    ],
    "Called by": [
      "AntonHarness",
      "CLI/runtime constructors"
    ],
    "Data read": [
      "history",
      "settings",
      "memory",
      "tool results"
    ],
    "Data written": [
      "history",
      "stream events",
      "memory tasks"
    ],
    "External dependencies": [
      "LLMClient",
      "ToolRegistry",
      "ScratchpadManager"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/llm/client.py",
    "Responsibility": "Bind planning/coding roles to provider/model pairs",
    "Important classes": [
      {
        "name": "LLMClient",
        "line": 35
      }
    ],
    "Important functions": [
      {
        "name": "_resolve_openai_compatible_flavor",
        "line": 12
      },
      {
        "name": "LLMClient.__init__",
        "line": 36
      },
      {
        "name": "LLMClient.plan",
        "line": 51
      },
      {
        "name": "LLMClient.plan_stream",
        "line": 69
      },
      {
        "name": "LLMClient.planning_provider",
        "line": 89
      },
      {
        "name": "LLMClient.coding_provider",
        "line": 94
      },
      {
        "name": "LLMClient.coding_model",
        "line": 99
      },
      {
        "name": "LLMClient.code",
        "line": 103
      },
      {
        "name": "LLMClient._generate_object_with",
        "line": 121
      },
      {
        "name": "LLMClient.generate_object",
        "line": 163
      },
      {
        "name": "LLMClient.generate_object_code",
        "line": 224
      },
      {
        "name": "LLMClient.from_settings",
        "line": 251
      }
    ],
    "Calls": [
      "plan",
      "plan_stream",
      "code",
      "generate_object"
    ],
    "Called by": [
      "ChatSession",
      "memory",
      "helper code"
    ],
    "Data read": [
      "model settings",
      "messages"
    ],
    "Data written": [
      "provider requests"
    ],
    "External dependencies": [
      "LLMProvider"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/llm/provider.py",
    "Responsibility": "Provider contract and normalized response/tool/usage/event types",
    "Important classes": [
      {
        "name": "ToolCall",
        "line": 10
      },
      {
        "name": "Usage",
        "line": 25
      },
      {
        "name": "LLMResponse",
        "line": 32
      },
      {
        "name": "StreamTextDelta",
        "line": 40
      },
      {
        "name": "StreamToolUseStart",
        "line": 45
      },
      {
        "name": "StreamToolUseDelta",
        "line": 51
      },
      {
        "name": "StreamToolUseEnd",
        "line": 57
      },
      {
        "name": "StreamComplete",
        "line": 62
      },
      {
        "name": "StreamTaskProgress",
        "line": 67
      },
      {
        "name": "StreamToolResult",
        "line": 85
      },
      {
        "name": "StreamContextCompacted",
        "line": 102
      },
      {
        "name": "ContextOverflowError",
        "line": 294
      },
      {
        "name": "TokenLimitExceeded",
        "line": 303
      },
      {
        "name": "ProviderConnectionInfo",
        "line": 308
      },
      {
        "name": "LLMProvider",
        "line": 321
      }
    ],
    "Important functions": [
      {
        "name": "_try_repair_tool_json",
        "line": 120
      },
      {
        "name": "safe_parse_tool_input",
        "line": 203
      },
      {
        "name": "compute_context_pressure",
        "line": 284
      },
      {
        "name": "ContextOverflowError.__init__",
        "line": 297
      },
      {
        "name": "LLMProvider.native_web_tools",
        "line": 325
      },
      {
        "name": "LLMProvider.complete",
        "line": 342
      },
      {
        "name": "LLMProvider.export_connection_info",
        "line": 354
      },
      {
        "name": "LLMProvider.stream",
        "line": 362
      }
    ],
    "Calls": [
      "compute_context_pressure",
      "LLMProvider"
    ],
    "Called by": [
      "provider clients and session"
    ],
    "Data read": [
      "provider response values"
    ],
    "Data written": [
      "normalized data"
    ],
    "External dependencies": [
      "dataclasses",
      "typing"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/llm/openai.py",
    "Responsibility": "Translate requests/streaming for OpenAI-compatible and Responses APIs",
    "Important classes": [
      {
        "name": "OpenAIProvider",
        "line": 502
      }
    ],
    "Important functions": [
      {
        "name": "_translate_tools",
        "line": 28
      },
      {
        "name": "_translate_tool_choice",
        "line": 45
      },
      {
        "name": "_translate_messages",
        "line": 57
      },
      {
        "name": "_translate_assistant_blocks",
        "line": 99
      },
      {
        "name": "_translate_user_blocks",
        "line": 127
      },
      {
        "name": "_is_azure_endpoint",
        "line": 259
      },
      {
        "name": "_translate_tools_to_responses",
        "line": 280
      },
      {
        "name": "_translate_tool_choice_to_responses",
        "line": 300
      },
      {
        "name": "_translate_messages_to_responses_input",
        "line": 312
      },
      {
        "name": "_translate_assistant_blocks_to_responses",
        "line": 361
      },
      {
        "name": "_translate_user_blocks_to_responses",
        "line": 393
      },
      {
        "name": "_user_message_from_parts",
        "line": 438
      },
      {
        "name": "_native_web_entries_for_flavor",
        "line": 453
      },
      {
        "name": "build_chat_completion_kwargs",
        "line": 483
      },
      {
        "name": "OpenAIProvider.__init__",
        "line": 512
      },
      {
        "name": "OpenAIProvider.export_connection_info",
        "line": 571
      },
      {
        "name": "OpenAIProvider.native_web_tools",
        "line": 580
      },
      {
        "name": "OpenAIProvider._build_trace_headers",
        "line": 590
      },
      {
        "name": "OpenAIProvider.complete",
        "line": 619
      },
      {
        "name": "OpenAIProvider.stream",
        "line": 727
      },
      {
        "name": "OpenAIProvider._build_responses_kwargs",
        "line": 891
      },
      {
        "name": "OpenAIProvider._complete_via_responses",
        "line": 924
      },
      {
        "name": "OpenAIProvider._stream_via_responses",
        "line": 976
      },
      {
        "name": "_parse_response_object",
        "line": 1117
      }
    ],
    "Calls": [
      "OpenAIProvider",
      "stream",
      "complete"
    ],
    "Called by": [
      "LLMClient",
      "API provider factory"
    ],
    "Data read": [
      "keys",
      "base URL",
      "messages",
      "tools"
    ],
    "Data written": [
      "provider HTTP requests and normalized events"
    ],
    "External dependencies": [
      "openai SDK"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/llm/anthropic.py",
    "Responsibility": "Anthropic model/tool/stream adapter",
    "Important classes": [
      {
        "name": "AnthropicProvider",
        "line": 56
      }
    ],
    "Important functions": [
      {
        "name": "_build_native_web_tools",
        "line": 35
      },
      {
        "name": "AnthropicProvider.native_web_tools",
        "line": 59
      },
      {
        "name": "AnthropicProvider.__init__",
        "line": 64
      },
      {
        "name": "AnthropicProvider.export_connection_info",
        "line": 71
      },
      {
        "name": "AnthropicProvider.complete",
        "line": 74
      },
      {
        "name": "AnthropicProvider.stream",
        "line": 154
      }
    ],
    "Calls": [
      "AnthropicProvider",
      "stream",
      "complete"
    ],
    "Called by": [
      "LLMClient",
      "API provider factory"
    ],
    "Data read": [
      "key",
      "messages",
      "tools"
    ],
    "Data written": [
      "provider requests and events"
    ],
    "External dependencies": [
      "anthropic SDK"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/llm/prompt_builder.py",
    "Responsibility": "Assemble runtime, memory, project, datasource and skill prompt",
    "Important classes": [
      {
        "name": "SystemPromptContext",
        "line": 21
      },
      {
        "name": "ChatSystemPromptBuilder",
        "line": 35
      }
    ],
    "Important functions": [
      {
        "name": "ChatSystemPromptBuilder._build_tool_prompts_section",
        "line": 40
      },
      {
        "name": "ChatSystemPromptBuilder._build_procedural_memory_section",
        "line": 63
      },
      {
        "name": "ChatSystemPromptBuilder._build_visualizations_section",
        "line": 108
      },
      {
        "name": "ChatSystemPromptBuilder.build",
        "line": 124
      }
    ],
    "Calls": [
      "ChatSystemPromptBuilder.build"
    ],
    "Called by": [
      "ChatSession._build_system_prompt"
    ],
    "Data read": [
      "prompt context",
      "tool prompts",
      "SkillStore"
    ],
    "Data written": [
      "system prompt string"
    ],
    "External dependencies": [
      "Anton prompts"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/tools/registry.py",
    "Responsibility": "Named ToolDef registration and dispatch",
    "Important classes": [
      {
        "name": "ToolRegistry",
        "line": 10
      }
    ],
    "Important functions": [
      {
        "name": "ToolRegistry.__init__",
        "line": 15
      },
      {
        "name": "ToolRegistry.__bool__",
        "line": 18
      },
      {
        "name": "ToolRegistry.register_tool",
        "line": 21
      },
      {
        "name": "ToolRegistry.get_tool_defs",
        "line": 27
      },
      {
        "name": "ToolRegistry.dispatch_tool",
        "line": 31
      },
      {
        "name": "ToolRegistry.unregister_tool",
        "line": 40
      },
      {
        "name": "ToolRegistry.dump",
        "line": 44
      }
    ],
    "Calls": [
      "register_tool",
      "dispatch_tool",
      "dump"
    ],
    "Called by": [
      "ChatSession"
    ],
    "Data read": [
      "ToolDef",
      "tool-call input"
    ],
    "Data written": [
      "tool execution result"
    ],
    "External dependencies": [
      "async handlers"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/tools/tool_handlers.py",
    "Responsibility": "Core tool implementations and artifact/backend integration",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_fire_pre_execute",
        "line": 16
      },
      {
        "name": "_fire_post_execute",
        "line": 39
      },
      {
        "name": "_artifact_store",
        "line": 59
      },
      {
        "name": "handle_create_artifact",
        "line": 73
      },
      {
        "name": "handle_update_artifact_metadata",
        "line": 120
      },
      {
        "name": "handle_launch_backend",
        "line": 192
      },
      {
        "name": "handle_list_artifacts",
        "line": 253
      },
      {
        "name": "handle_open_artifact",
        "line": 282
      },
      {
        "name": "handle_recall",
        "line": 313
      },
      {
        "name": "handle_memorize",
        "line": 331
      },
      {
        "name": "handle_scratchpad",
        "line": 394
      },
      {
        "name": "handle_read_image",
        "line": 520
      }
    ],
    "Calls": [
      "handle_create_artifact",
      "handle_scratchpad",
      "handle_memorize"
    ],
    "Called by": [
      "ToolRegistry",
      "ChatSession special scratchpad path"
    ],
    "Data read": [
      "tool arguments",
      "session workspace/runtime/memory"
    ],
    "Data written": [
      "artifact metadata/files",
      "execution",
      "memory"
    ],
    "External dependencies": [
      "ArtifactStore",
      "scratchpad runtime"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/backends/manager.py",
    "Responsibility": "Allocate/reuse named execution runtimes",
    "Important classes": [
      {
        "name": "ScratchpadManager",
        "line": 10
      }
    ],
    "Important functions": [
      {
        "name": "ScratchpadManager.__init__",
        "line": 13
      },
      {
        "name": "ScratchpadManager.pads",
        "line": 34
      },
      {
        "name": "ScratchpadManager.available_packages",
        "line": 39
      },
      {
        "name": "ScratchpadManager.probe_packages",
        "line": 44
      },
      {
        "name": "ScratchpadManager.get_or_create",
        "line": 50
      },
      {
        "name": "ScratchpadManager.remove",
        "line": 66
      },
      {
        "name": "ScratchpadManager.list_pads",
        "line": 74
      },
      {
        "name": "ScratchpadManager.cancel_all_running",
        "line": 77
      },
      {
        "name": "ScratchpadManager.close_all",
        "line": 82
      },
      {
        "name": "ScratchpadManager.venv_python",
        "line": 88
      }
    ],
    "Calls": [
      "get_or_create",
      "close_all",
      "cancel_all_running"
    ],
    "Called by": [
      "ChatSession",
      "tools"
    ],
    "Data read": [
      "coding configuration",
      "replay cells"
    ],
    "Data written": [
      "runtime pool"
    ],
    "External dependencies": [
      "ScratchpadRuntime"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/backends/local.py",
    "Responsibility": "Persistent local Python subprocess and venv lifecycle",
    "Important classes": [
      {
        "name": "LocalScratchpadRuntime",
        "line": 28
      }
    ],
    "Important functions": [
      {
        "name": "LocalScratchpadRuntime.__init__",
        "line": 33
      },
      {
        "name": "LocalScratchpadRuntime._ensure_venv",
        "line": 73
      },
      {
        "name": "LocalScratchpadRuntime._find_uv",
        "line": 106
      },
      {
        "name": "LocalScratchpadRuntime._create_venv",
        "line": 125
      },
      {
        "name": "LocalScratchpadRuntime.venv_python",
        "line": 164
      },
      {
        "name": "LocalScratchpadRuntime.ensure_venv",
        "line": 175
      },
      {
        "name": "LocalScratchpadRuntime._verify_venv_python",
        "line": 189
      },
      {
        "name": "LocalScratchpadRuntime._nuke_venv",
        "line": 206
      },
      {
        "name": "LocalScratchpadRuntime._add_windows_firewall_rule",
        "line": 215
      },
      {
        "name": "LocalScratchpadRuntime._setup_parent_site_packages",
        "line": 241
      },
      {
        "name": "LocalScratchpadRuntime._try_recycle_venv",
        "line": 257
      },
      {
        "name": "LocalScratchpadRuntime._save_requirements",
        "line": 277
      },
      {
        "name": "LocalScratchpadRuntime._load_requirements",
        "line": 288
      },
      {
        "name": "LocalScratchpadRuntime._save_python_version",
        "line": 301
      },
      {
        "name": "LocalScratchpadRuntime._check_python_version",
        "line": 311
      },
      {
        "name": "LocalScratchpadRuntime.start",
        "line": 323
      },
      {
        "name": "LocalScratchpadRuntime.reset",
        "line": 420
      },
      {
        "name": "LocalScratchpadRuntime.close",
        "line": 428
      },
      {
        "name": "LocalScratchpadRuntime.cancel",
        "line": 436
      },
      {
        "name": "LocalScratchpadRuntime.cleanup",
        "line": 457
      },
      {
        "name": "LocalScratchpadRuntime.execute_streaming",
        "line": 462
      },
      {
        "name": "LocalScratchpadRuntime._read_result",
        "line": 562
      },
      {
        "name": "LocalScratchpadRuntime.install_packages",
        "line": 650
      },
      {
        "name": "LocalScratchpadRuntime._stop_process",
        "line": 685
      },
      {
        "name": "LocalScratchpadRuntime._kill_tree",
        "line": 708
      },
      {
        "name": "local_scratchpad_runtime_factory",
        "line": 726
      }
    ],
    "Calls": [
      "start",
      "execute_streaming",
      "close"
    ],
    "Called by": [
      "ScratchpadManager"
    ],
    "Data read": [
      "environment",
      "code",
      "workspace",
      "replay cells"
    ],
    "Data written": [
      "venv",
      "subprocess",
      "cell results"
    ],
    "External dependencies": [
      "asyncio subprocess",
      "uv/venv"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/backends/scratchpad_boot.py",
    "Responsibility": "Subprocess execution namespace and wire protocol",
    "Important classes": [
      {
        "name": "_CellLogHandler",
        "line": 691
      }
    ],
    "Important functions": [
      {
        "name": "_load_namespace",
        "line": 21
      },
      {
        "name": "_dump_namespace",
        "line": 40
      },
      {
        "name": "progress",
        "line": 474
      },
      {
        "name": "sample",
        "line": 483
      },
      {
        "name": "_truncate_sample",
        "line": 674
      },
      {
        "name": "_CellLogHandler.__init__",
        "line": 694
      },
      {
        "name": "_CellLogHandler.emit",
        "line": 699
      }
    ],
    "Calls": [
      "exec",
      "coding helpers"
    ],
    "Called by": [
      "LocalScratchpadRuntime subprocess"
    ],
    "Data read": [
      "code cells",
      "inherited environment"
    ],
    "Data written": [
      "stdout/results",
      "arbitrary generated-code effects"
    ],
    "External dependencies": [
      "Python",
      "provider SDK helpers"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/datasources/data_vault.py",
    "Responsibility": "Plaintext credential record storage and environment mapping",
    "Important classes": [
      {
        "name": "DataVault",
        "line": 129
      },
      {
        "name": "LocalDataVault",
        "line": 187
      }
    ],
    "Important functions": [
      {
        "name": "is_secret_key",
        "line": 38
      },
      {
        "name": "_sanitize",
        "line": 57
      },
      {
        "name": "resolve_modify_merge",
        "line": 62
      },
      {
        "name": "_slug_env_prefix",
        "line": 116
      },
      {
        "name": "DataVault.save",
        "line": 138
      },
      {
        "name": "DataVault.load",
        "line": 155
      },
      {
        "name": "DataVault.read_record",
        "line": 159
      },
      {
        "name": "DataVault.delete",
        "line": 166
      },
      {
        "name": "DataVault.list_connections",
        "line": 170
      },
      {
        "name": "DataVault.inject_env",
        "line": 174
      },
      {
        "name": "DataVault.clear_ds_env",
        "line": 178
      },
      {
        "name": "DataVault.next_connection_number",
        "line": 182
      },
      {
        "name": "LocalDataVault.__init__",
        "line": 190
      },
      {
        "name": "LocalDataVault._path_for",
        "line": 193
      },
      {
        "name": "LocalDataVault._ensure_dir",
        "line": 196
      },
      {
        "name": "LocalDataVault.save",
        "line": 200
      },
      {
        "name": "LocalDataVault.load",
        "line": 241
      },
      {
        "name": "LocalDataVault._read_raw",
        "line": 252
      },
      {
        "name": "LocalDataVault.read_record",
        "line": 261
      },
      {
        "name": "LocalDataVault.delete",
        "line": 279
      },
      {
        "name": "LocalDataVault.list_connections",
        "line": 287
      },
      {
        "name": "LocalDataVault.env_for",
        "line": 308
      },
      {
        "name": "LocalDataVault.inject_env",
        "line": 333
      },
      {
        "name": "LocalDataVault.clear_ds_env",
        "line": 348
      },
      {
        "name": "LocalDataVault.next_connection_number",
        "line": 354
      }
    ],
    "Calls": [
      "LocalDataVault.save",
      "load",
      "inject_env",
      "env_for"
    ],
    "Called by": [
      "API probes/harness/connections",
      "CLI"
    ],
    "Data read": [
      "connection JSON"
    ],
    "Data written": [
      "connection JSON",
      "DS_* variables"
    ],
    "External dependencies": [
      "filesystem",
      "os.environ"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/utils/datasources.py",
    "Responsibility": "Datasource prompt roster and credential text scrubbing",
    "Important classes": [],
    "Important functions": [
      {
        "name": "_reset_registered_ds_vars",
        "line": 24
      },
      {
        "name": "parse_connection_slug",
        "line": 30
      },
      {
        "name": "register_secret_vars",
        "line": 60
      },
      {
        "name": "scrub_credentials",
        "line": 82
      },
      {
        "name": "build_datasource_context",
        "line": 110
      },
      {
        "name": "restore_namespaced_env",
        "line": 148
      },
      {
        "name": "find_matching_connection",
        "line": 160
      },
      {
        "name": "save_connection",
        "line": 192
      },
      {
        "name": "persist_custom_engine",
        "line": 216
      },
      {
        "name": "remove_engine_block",
        "line": 286
      }
    ],
    "Calls": [
      "build_datasource_context",
      "scrub_credentials"
    ],
    "Called by": [
      "ChatSession",
      "datasource commands"
    ],
    "Data read": [
      "vault metadata",
      "DS_* environment"
    ],
    "Data written": [
      "prompt/result strings"
    ],
    "External dependencies": [
      "LocalDataVault"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/artifacts/store.py",
    "Responsibility": "Artifact folders, metadata, provenance and file rescans",
    "Important classes": [
      {
        "name": "ArtifactStore",
        "line": 90
      }
    ],
    "Important functions": [
      {
        "name": "_utc_now",
        "line": 55
      },
      {
        "name": "_new_id",
        "line": 59
      },
      {
        "name": "_sanitize_slug",
        "line": 66
      },
      {
        "name": "_truncate_summary",
        "line": 83
      },
      {
        "name": "ArtifactStore.__init__",
        "line": 99
      },
      {
        "name": "ArtifactStore.root",
        "line": 105
      },
      {
        "name": "ArtifactStore.ensure_root",
        "line": 108
      },
      {
        "name": "ArtifactStore.folder_for",
        "line": 112
      },
      {
        "name": "ArtifactStore.metadata_path",
        "line": 115
      },
      {
        "name": "ArtifactStore.readme_path",
        "line": 118
      },
      {
        "name": "ArtifactStore._unique_slug",
        "line": 123
      },
      {
        "name": "ArtifactStore.create",
        "line": 137
      },
      {
        "name": "ArtifactStore.update",
        "line": 181
      },
      {
        "name": "ArtifactStore.list",
        "line": 212
      },
      {
        "name": "ArtifactStore.open",
        "line": 231
      },
      {
        "name": "ArtifactStore.record_turn",
        "line": 238
      },
      {
        "name": "ArtifactStore.rescan_files",
        "line": 289
      },
      {
        "name": "ArtifactStore.render_readme",
        "line": 316
      },
      {
        "name": "ArtifactStore._save",
        "line": 328
      },
      {
        "name": "ArtifactStore._load_silent",
        "line": 342
      },
      {
        "name": "ArtifactStore._render_readme_text",
        "line": 354
      }
    ],
    "Calls": [
      "ArtifactStore.create",
      "open",
      "record_turn",
      "rescan_files"
    ],
    "Called by": [
      "artifact tools"
    ],
    "Data read": [
      "metadata.json",
      "files"
    ],
    "Data written": [
      "artifact directory",
      "metadata.json",
      "README.md"
    ],
    "External dependencies": [
      "filesystem",
      "artifact models"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/memory/cortex.py",
    "Responsibility": "Compose memory and coordinate encoding/consolidation",
    "Important classes": [
      {
        "name": "_IdentityFacts",
        "line": 41
      },
      {
        "name": "_CompactionResult",
        "line": 63
      },
      {
        "name": "Cortex",
        "line": 104
      }
    ],
    "Important functions": [
      {
        "name": "Cortex.__init__",
        "line": 112
      },
      {
        "name": "Cortex.build_memory_context",
        "line": 171
      },
      {
        "name": "Cortex._format_rules_engrams",
        "line": 232
      },
      {
        "name": "Cortex._retrieve_relevant_rules",
        "line": 245
      },
      {
        "name": "Cortex.get_scratchpad_context",
        "line": 300
      },
      {
        "name": "Cortex.encode",
        "line": 318
      },
      {
        "name": "Cortex._log_write_engram",
        "line": 362
      },
      {
        "name": "Cortex._log_read_engram",
        "line": 372
      },
      {
        "name": "Cortex.encoding_gate",
        "line": 382
      },
      {
        "name": "Cortex.needs_compaction",
        "line": 405
      },
      {
        "name": "Cortex.compact_all",
        "line": 417
      },
      {
        "name": "Cortex.vacuum",
        "line": 433
      },
      {
        "name": "Cortex.maybe_vacuum",
        "line": 447
      },
      {
        "name": "Cortex._compact_file",
        "line": 462
      },
      {
        "name": "Cortex.maybe_update_identity",
        "line": 515
      }
    ],
    "Calls": [
      "build_memory_context",
      "encode",
      "maybe_update_identity"
    ],
    "Called by": [
      "ChatSession",
      "memory tools"
    ],
    "Data read": [
      "global/project memory"
    ],
    "Data written": [
      "memory updates",
      "prompt context"
    ],
    "External dependencies": [
      "Hippocampus",
      "LLMClient"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/memory/hippocampus.py",
    "Responsibility": "Filesystem semantic/behavioral memory storage and retrieval",
    "Important classes": [
      {
        "name": "Hippocampus",
        "line": 70
      }
    ],
    "Important functions": [
      {
        "name": "_extract_metadata",
        "line": 32
      },
      {
        "name": "Hippocampus.__init__",
        "line": 79
      },
      {
        "name": "Hippocampus.clear",
        "line": 90
      },
      {
        "name": "Hippocampus.recall_identities",
        "line": 101
      },
      {
        "name": "Hippocampus.get_identities",
        "line": 115
      },
      {
        "name": "Hippocampus.del_identity",
        "line": 131
      },
      {
        "name": "Hippocampus.update_identity",
        "line": 140
      },
      {
        "name": "Hippocampus.rewrite_identity",
        "line": 152
      },
      {
        "name": "Hippocampus.save_identities",
        "line": 182
      },
      {
        "name": "Hippocampus.clear_identity",
        "line": 187
      },
      {
        "name": "Hippocampus.recall_lessons",
        "line": 194
      },
      {
        "name": "Hippocampus.get_lessons",
        "line": 203
      },
      {
        "name": "Hippocampus.del_lesson",
        "line": 255
      },
      {
        "name": "Hippocampus.update_lesson",
        "line": 266
      },
      {
        "name": "Hippocampus._lessons_to_text",
        "line": 280
      },
      {
        "name": "Hippocampus.recall_topic",
        "line": 308
      },
      {
        "name": "Hippocampus.recall_scratchpad_wisdom",
        "line": 323
      },
      {
        "name": "Hippocampus.recall_rules",
        "line": 356
      },
      {
        "name": "Hippocampus.get_rules",
        "line": 370
      },
      {
        "name": "Hippocampus.del_rule",
        "line": 395
      },
      {
        "name": "Hippocampus.update_rule",
        "line": 404
      },
      {
        "name": "Hippocampus.save_rules",
        "line": 416
      },
      {
        "name": "Hippocampus.encode_rule",
        "line": 433
      },
      {
        "name": "Hippocampus.encode_lesson",
        "line": 467
      },
      {
        "name": "Hippocampus.entry_count",
        "line": 495
      },
      {
        "name": "Hippocampus._encode_with_lock",
        "line": 509
      },
      {
        "name": "Hippocampus._extract_entry_texts",
        "line": 552
      },
      {
        "name": "Hippocampus._sanitize_slug",
        "line": 573
      }
    ],
    "Calls": [
      "Hippocampus methods"
    ],
    "Called by": [
      "Cortex"
    ],
    "Data read": [
      "rules.md",
      "lessons.md",
      "topics/profile files"
    ],
    "Data written": [
      "memory files"
    ],
    "External dependencies": [
      "filesystem"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/memory/skills.py",
    "Responsibility": "Skill directory storage/search and staged representations",
    "Important classes": [
      {
        "name": "StageStats",
        "line": 76
      },
      {
        "name": "SkillStats",
        "line": 93
      },
      {
        "name": "Skill",
        "line": 101
      },
      {
        "name": "SkillStore",
        "line": 210
      }
    ],
    "Important functions": [
      {
        "name": "Skill.to_meta_dict",
        "line": 125
      },
      {
        "name": "Skill.to_stats_dict",
        "line": 139
      },
      {
        "name": "_stage_stats_to_dict",
        "line": 148
      },
      {
        "name": "_stage_stats_from_dict",
        "line": 157
      },
      {
        "name": "slugify",
        "line": 174
      },
      {
        "name": "make_unique_label",
        "line": 188
      },
      {
        "name": "SkillStore.__init__",
        "line": 220
      },
      {
        "name": "SkillStore._skill_dir",
        "line": 225
      },
      {
        "name": "SkillStore._ensure_root",
        "line": 228
      },
      {
        "name": "SkillStore.load",
        "line": 231
      },
      {
        "name": "SkillStore._load_stats",
        "line": 261
      },
      {
        "name": "SkillStore.list_all",
        "line": 276
      },
      {
        "name": "SkillStore.list_summaries",
        "line": 289
      },
      {
        "name": "SkillStore.save",
        "line": 318
      },
      {
        "name": "SkillStore.delete",
        "line": 343
      },
      {
        "name": "SkillStore.increment_recommended",
        "line": 353
      },
      {
        "name": "SkillStore._stage_for",
        "line": 387
      },
      {
        "name": "SkillStore.closest_match",
        "line": 398
      }
    ],
    "Calls": [
      "SkillStore",
      "Skill"
    ],
    "Called by": [
      "harness sync",
      "prompt builder",
      "recall_skill"
    ],
    "Data read": [
      "meta.json",
      "declarative.md",
      "optional code/chunks"
    ],
    "Data written": [
      "skill files and usage stats"
    ],
    "External dependencies": [
      "filesystem",
      "JSON"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/dispatch/policy.py",
    "Responsibility": "Pure proposed-action allow/deny/prompt evaluator",
    "Important classes": [
      {
        "name": "GateDecision",
        "line": 30
      },
      {
        "name": "FileScope",
        "line": 44
      },
      {
        "name": "PermissionPolicy",
        "line": 61
      },
      {
        "name": "ProposedAction",
        "line": 103
      },
      {
        "name": "GateResult",
        "line": 129
      }
    ],
    "Important functions": [
      {
        "name": "evaluate",
        "line": 138
      },
      {
        "name": "_path_in_scopes",
        "line": 224
      },
      {
        "name": "_host_in_allowlist",
        "line": 236
      }
    ],
    "Calls": [
      "evaluate"
    ],
    "Called by": [
      "dispatch path",
      "not proven on direct cowork tool loop"
    ],
    "Data read": [
      "PermissionPolicy",
      "ProposedAction"
    ],
    "Data written": [
      "GateResult"
    ],
    "External dependencies": [
      "Python dataclasses"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Core Agent",
    "File": "backend/core_agent/anton/core/dispatch/local_runtime.py",
    "Responsibility": "Per-session background dispatch orchestration",
    "Important classes": [
      {
        "name": "InProcessRuntimeOrchestrator",
        "line": 43
      },
      {
        "name": "LocalScratchpadOrchestrator",
        "line": 190
      }
    ],
    "Important functions": [
      {
        "name": "InProcessRuntimeOrchestrator.__init__",
        "line": 60
      },
      {
        "name": "InProcessRuntimeOrchestrator.wake",
        "line": 74
      },
      {
        "name": "InProcessRuntimeOrchestrator.stop",
        "line": 88
      },
      {
        "name": "InProcessRuntimeOrchestrator.stop_all",
        "line": 103
      },
      {
        "name": "InProcessRuntimeOrchestrator._run",
        "line": 126
      },
      {
        "name": "_extract_text",
        "line": 167
      },
      {
        "name": "LocalScratchpadOrchestrator.__init__",
        "line": 222
      },
      {
        "name": "LocalScratchpadOrchestrator.wake",
        "line": 242
      },
      {
        "name": "LocalScratchpadOrchestrator.stop",
        "line": 256
      },
      {
        "name": "LocalScratchpadOrchestrator.stop_all",
        "line": 277
      },
      {
        "name": "LocalScratchpadOrchestrator._close_chat_session",
        "line": 303
      },
      {
        "name": "LocalScratchpadOrchestrator._get_chat_session",
        "line": 322
      },
      {
        "name": "LocalScratchpadOrchestrator._run",
        "line": 348
      },
      {
        "name": "LocalScratchpadOrchestrator._run_turn",
        "line": 390
      },
      {
        "name": "LocalScratchpadOrchestrator._safe_error_message",
        "line": 441
      }
    ],
    "Calls": [
      "wake",
      "stop",
      "agent callable"
    ],
    "Called by": [
      "dispatch router"
    ],
    "Data read": [
      "inbound store rows",
      "agent groups"
    ],
    "Data written": [
      "outbound rows",
      "runtime task/session cache"
    ],
    "External dependencies": [
      "asyncio",
      "session store"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  }
]
```

## Separate Data Engine

```json
[
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/__main__.py",
    "Responsibility": "Data-engine process startup and service orchestration",
    "Important classes": [
      {
        "name": "TrunkProcessEnum",
        "line": 63
      },
      {
        "name": "TrunkProcessData",
        "line": 78
      }
    ],
    "Important functions": [
      {
        "name": "TrunkProcessEnum._missing_",
        "line": 72
      },
      {
        "name": "TrunkProcessData.request_restart_attempt",
        "line": 93
      },
      {
        "name": "TrunkProcessData.should_restart",
        "line": 114
      },
      {
        "name": "close_api_gracefully",
        "line": 133
      },
      {
        "name": "clean_mindsdb_tmp_dir",
        "line": 160
      },
      {
        "name": "set_error_model_status_by_pids",
        "line": 183
      },
      {
        "name": "set_error_model_status_for_unfinished",
        "line": 211
      },
      {
        "name": "do_clean_process_marks",
        "line": 233
      },
      {
        "name": "create_permanent_integrations",
        "line": 241
      },
      {
        "name": "validate_default_project",
        "line": 270
      },
      {
        "name": "start_process",
        "line": 315
      }
    ],
    "Calls": [
      "start_http",
      "start_mysql",
      "start_scheduler",
      "start_ml_task_queue"
    ],
    "Called by": [
      "module/CLI launcher"
    ],
    "Data read": [
      "Config",
      "metadata"
    ],
    "Data written": [
      "processes",
      "service status"
    ],
    "External dependencies": [
      "multiprocessing",
      "SQLAlchemy"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/api/http/namespaces/sql.py",
    "Responsibility": "HTTP SQL execution, native handler branch and result encoding",
    "Important classes": [
      {
        "name": "ReponseFormat",
        "line": 33
      },
      {
        "name": "Query",
        "line": 41
      },
      {
        "name": "Charter",
        "line": 191
      },
      {
        "name": "ParametrizeConstants",
        "line": 307
      },
      {
        "name": "ListDatabases",
        "line": 407
      }
    ],
    "Important functions": [
      {
        "name": "Query.__init__",
        "line": 42
      },
      {
        "name": "Query.post",
        "line": 48
      },
      {
        "name": "Charter.__init__",
        "line": 192
      },
      {
        "name": "Charter._extract_error_message",
        "line": 195
      },
      {
        "name": "Charter.post",
        "line": 259
      },
      {
        "name": "ParametrizeConstants.__init__",
        "line": 308
      },
      {
        "name": "ParametrizeConstants.post",
        "line": 312
      },
      {
        "name": "ListDatabases.get",
        "line": 410
      }
    ],
    "Calls": [
      "Query.post",
      "FakeMysqlProxy",
      "handler.native_query"
    ],
    "Called by": [
      "HTTP router"
    ],
    "Data read": [
      "query/context/params"
    ],
    "Data written": [
      "query effects",
      "HTTP response"
    ],
    "External dependencies": [
      "Flask",
      "flask-restx",
      "mindsdb SQL parser"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/interfaces/database/integrations.py",
    "Responsibility": "Integration metadata and handler discovery/creation",
    "Important classes": [
      {
        "name": "IntegrationController",
        "line": 53
      }
    ],
    "Important functions": [
      {
        "name": "IntegrationController._is_not_empty_str",
        "line": 55
      },
      {
        "name": "IntegrationController.__init__",
        "line": 58
      },
      {
        "name": "IntegrationController.community_handlers_dir",
        "line": 65
      },
      {
        "name": "IntegrationController._add_integration_record",
        "line": 73
      },
      {
        "name": "IntegrationController.add",
        "line": 85
      },
      {
        "name": "IntegrationController.check_connection",
        "line": 133
      },
      {
        "name": "IntegrationController.modify",
        "line": 144
      },
      {
        "name": "IntegrationController.delete",
        "line": 161
      },
      {
        "name": "IntegrationController._get_integration_record_data",
        "line": 220
      },
      {
        "name": "IntegrationController.get_by_id",
        "line": 297
      },
      {
        "name": "IntegrationController.get",
        "line": 304
      },
      {
        "name": "IntegrationController._get_integration_record",
        "line": 312
      },
      {
        "name": "IntegrationController.get_all",
        "line": 344
      },
      {
        "name": "IntegrationController._make_handler_args",
        "line": 356
      },
      {
        "name": "IntegrationController.create_tmp_handler",
        "line": 382
      },
      {
        "name": "IntegrationController.copy_integration_storage",
        "line": 421
      },
      {
        "name": "IntegrationController.get_ml_handler",
        "line": 435
      },
      {
        "name": "IntegrationController.get_data_handler",
        "line": 467
      },
      {
        "name": "IntegrationController.reload_handler_module",
        "line": 560
      },
      {
        "name": "IntegrationController._read_dependencies",
        "line": 571
      },
      {
        "name": "IntegrationController._get_handler_meta",
        "line": 580
      },
      {
        "name": "IntegrationController._get_handler_icon",
        "line": 652
      },
      {
        "name": "IntegrationController._register_handler_dir",
        "line": 672
      },
      {
        "name": "IntegrationController._load_handler_modules",
        "line": 704
      },
      {
        "name": "IntegrationController._get_connection_args",
        "line": 762
      },
      {
        "name": "IntegrationController._get_base_class_type",
        "line": 801
      },
      {
        "name": "IntegrationController._get_handler_info",
        "line": 837
      },
      {
        "name": "IntegrationController._fetch_community_handler",
        "line": 888
      },
      {
        "name": "IntegrationController.import_handler",
        "line": 925
      },
      {
        "name": "IntegrationController.get_handlers_import_status",
        "line": 989
      },
      {
        "name": "IntegrationController.get_handlers_metadata",
        "line": 1002
      },
      {
        "name": "IntegrationController.get_handler_metadata",
        "line": 1005
      },
      {
        "name": "IntegrationController.get_handler_meta",
        "line": 1009
      },
      {
        "name": "IntegrationController.get_handler_module",
        "line": 1033
      },
      {
        "name": "IntegrationController.create_permanent_integrations",
        "line": 1040
      }
    ],
    "Calls": [
      "IntegrationController.add",
      "get_data_handler"
    ],
    "Called by": [
      "SQL executor",
      "HTTP SQL",
      "controllers"
    ],
    "Data read": [
      "Integration records",
      "handler metadata",
      "connection data"
    ],
    "Data written": [
      "integration rows",
      "credential files",
      "handler cache"
    ],
    "External dependencies": [
      "SQLAlchemy",
      "handler plugins"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/integrations/handlers/postgres_handler/postgres_handler.py",
    "Responsibility": "PostgreSQL driver, schema and query execution",
    "Important classes": [
      {
        "name": "PostgresHandler",
        "line": 152
      }
    ],
    "Important functions": [
      {
        "name": "_map_type",
        "line": 38
      },
      {
        "name": "_get_columns",
        "line": 79
      },
      {
        "name": "_make_df",
        "line": 136
      },
      {
        "name": "PostgresHandler.__init__",
        "line": 161
      },
      {
        "name": "PostgresHandler.__del__",
        "line": 173
      },
      {
        "name": "PostgresHandler._make_connection_args",
        "line": 177
      },
      {
        "name": "PostgresHandler.connect",
        "line": 203
      },
      {
        "name": "PostgresHandler.disconnect",
        "line": 232
      },
      {
        "name": "PostgresHandler.check_connection",
        "line": 241
      },
      {
        "name": "PostgresHandler._cast_dtypes",
        "line": 268
      },
      {
        "name": "PostgresHandler.native_query",
        "line": 306
      },
      {
        "name": "PostgresHandler._execute_client_side",
        "line": 336
      },
      {
        "name": "PostgresHandler._execute_server_side",
        "line": 368
      },
      {
        "name": "PostgresHandler._handle_query_exception",
        "line": 409
      },
      {
        "name": "PostgresHandler.insert",
        "line": 436
      },
      {
        "name": "PostgresHandler.query",
        "line": 473
      },
      {
        "name": "PostgresHandler.get_tables",
        "line": 489
      },
      {
        "name": "PostgresHandler.get_columns",
        "line": 513
      },
      {
        "name": "PostgresHandler.subscribe",
        "line": 562
      },
      {
        "name": "PostgresHandler.meta_get_tables",
        "line": 647
      },
      {
        "name": "PostgresHandler.meta_get_columns",
        "line": 683
      },
      {
        "name": "PostgresHandler.meta_get_column_statistics",
        "line": 719
      },
      {
        "name": "PostgresHandler.meta_get_primary_keys",
        "line": 793
      },
      {
        "name": "PostgresHandler.meta_get_foreign_keys",
        "line": 827
      }
    ],
    "Calls": [
      "PostgresHandler.connect",
      "native_query",
      "check_connection"
    ],
    "Called by": [
      "IntegrationController",
      "SQL native path"
    ],
    "Data read": [
      "connection args",
      "SQL"
    ],
    "Data written": [
      "database query effects",
      "TableResponse"
    ],
    "External dependencies": [
      "psycopg",
      "pandas"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/interfaces/storage/db.py",
    "Responsibility": "Data-engine ORM schema and metadata DB layer",
    "Important classes": [
      {
        "name": "Base",
        "line": 40
      },
      {
        "name": "NumpyEncoder",
        "line": 99
      },
      {
        "name": "Array",
        "line": 112
      },
      {
        "name": "Json",
        "line": 129
      },
      {
        "name": "SecretDataJson",
        "line": 144
      },
      {
        "name": "PREDICTOR_STATUS",
        "line": 148
      },
      {
        "name": "Predictor",
        "line": 162
      },
      {
        "name": "Project",
        "line": 219
      },
      {
        "name": "Integration",
        "line": 233
      },
      {
        "name": "File",
        "line": 249
      },
      {
        "name": "View",
        "line": 265
      },
      {
        "name": "JsonStorage",
        "line": 276
      },
      {
        "name": "Jobs",
        "line": 300
      },
      {
        "name": "JobsHistory",
        "line": 322
      },
      {
        "name": "ChatBots",
        "line": 341
      },
      {
        "name": "ChatBotsHistory",
        "line": 372
      },
      {
        "name": "Triggers",
        "line": 384
      },
      {
        "name": "Tasks",
        "line": 400
      },
      {
        "name": "AgentSkillsAssociation",
        "line": 423
      },
      {
        "name": "Skills",
        "line": 434
      },
      {
        "name": "Agents",
        "line": 459
      },
      {
        "name": "KnowledgeBase",
        "line": 527
      },
      {
        "name": "QueryContext",
        "line": 588
      },
      {
        "name": "Queries",
        "line": 602
      },
      {
        "name": "LLMLog",
        "line": 623
      },
      {
        "name": "LLMData",
        "line": 646
      }
    ],
    "Important functions": [
      {
        "name": "init",
        "line": 49
      },
      {
        "name": "serializable_insert",
        "line": 73
      },
      {
        "name": "NumpyEncoder.default",
        "line": 102
      },
      {
        "name": "Array.process_bind_param",
        "line": 117
      },
      {
        "name": "Array.process_result_value",
        "line": 125
      },
      {
        "name": "Json.process_bind_param",
        "line": 134
      },
      {
        "name": "Json.process_result_value",
        "line": 137
      },
      {
        "name": "Predictor.get_name_and_version",
        "line": 197
      },
      {
        "name": "JsonStorage.to_dict",
        "line": 287
      },
      {
        "name": "ChatBots.as_dict",
        "line": 358
      },
      {
        "name": "Skills.as_dict",
        "line": 447
      },
      {
        "name": "Agents.as_dict",
        "line": 478
      },
      {
        "name": "KnowledgeBase.as_dict",
        "line": 559
      }
    ],
    "Calls": [
      "SQLAlchemy model/session operations"
    ],
    "Called by": [
      "engine controllers"
    ],
    "Data read": [
      "database configuration",
      "tenant context"
    ],
    "Data written": [
      "Integration/File/Jobs/other records"
    ],
    "External dependencies": [
      "SQLAlchemy",
      "SecretData"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/api/mcp/tools/query.py",
    "Responsibility": "MCP query tool over SQL fa?ade",
    "Important classes": [],
    "Important functions": [
      {
        "name": "query",
        "line": 31
      }
    ],
    "Calls": [
      "query",
      "FakeMysqlProxy.process_query"
    ],
    "Called by": [
      "MCP registry"
    ],
    "Data read": [
      "SQL and context"
    ],
    "Data written": [
      "query effects",
      "normalized MCP result"
    ],
    "External dependencies": [
      "MCP",
      "Pydantic"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  },
  {
    "Subsystem": "Separate Data Engine",
    "File": "backend/data-vault/mindsdb/utilities/config.py",
    "Responsibility": "Merge engine configuration, storage and queue options",
    "Important classes": [
      {
        "name": "HTTP_AUTH_TYPE",
        "line": 106
      },
      {
        "name": "Config",
        "line": 115
      }
    ],
    "Important functions": [
      {
        "name": "get_bool_env_var",
        "line": 16
      },
      {
        "name": "get_list_env_var",
        "line": 41
      },
      {
        "name": "_merge_key_recursive",
        "line": 59
      },
      {
        "name": "_merge_configs",
        "line": 69
      },
      {
        "name": "_overwrite_configs",
        "line": 75
      },
      {
        "name": "create_data_dir",
        "line": 82
      },
      {
        "name": "Config.__new__",
        "line": 154
      },
      {
        "name": "Config.prepare_env_config",
        "line": 314
      },
      {
        "name": "Config.fetch_auto_config",
        "line": 548
      },
      {
        "name": "Config.fetch_user_config",
        "line": 574
      },
      {
        "name": "Config.ensure_auto_config_is_relevant",
        "line": 600
      },
      {
        "name": "Config.merge_configs",
        "line": 606
      },
      {
        "name": "Config.__getitem__",
        "line": 629
      },
      {
        "name": "Config.get",
        "line": 633
      },
      {
        "name": "Config.get_all",
        "line": 637
      },
      {
        "name": "Config.update",
        "line": 641
      },
      {
        "name": "Config.raise_warnings",
        "line": 665
      },
      {
        "name": "Config.cmd_args",
        "line": 685
      },
      {
        "name": "Config.parse_cmd_args",
        "line": 690
      },
      {
        "name": "Config.paths",
        "line": 742
      },
      {
        "name": "Config.user_config",
        "line": 746
      },
      {
        "name": "Config.auto_config",
        "line": 750
      },
      {
        "name": "Config.env_config",
        "line": 754
      },
      {
        "name": "Config.is_cloud",
        "line": 758
      }
    ],
    "Calls": [
      "Config",
      "prepare_env_config"
    ],
    "Called by": [
      "engine startup/controllers"
    ],
    "Data read": [
      "environment",
      "config files"
    ],
    "Data written": [
      "effective configuration",
      "storage initialization"
    ],
    "External dependencies": [
      "Python stdlib"
    ],
    "Evidence": "CONFIRMED source; Calls/Called by are curated path relationships, not an exhaustive static call graph"
  }
]
```

## Canonical Core API route declarations

CONFIRMED by AST extraction and router prefixes. These exclude compatibility routes, plugin-added channel webhooks, FastAPI-generated documentation routes and the separate data-engine APIs. Trailing slashes are preserved from decorators.

```json
[
  {
    "method": "GET",
    "path": "/api/v1/artifacts/",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "list_artifacts",
    "line": 41
  },
  {
    "method": "GET",
    "path": "/api/v1/artifacts/preview",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "preview_artifact",
    "line": 46
  },
  {
    "method": "POST",
    "path": "/api/v1/artifacts/preview-mount",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "preview_mount_endpoint",
    "line": 62
  },
  {
    "method": "GET",
    "path": "/api/v1/artifacts/preview-asset/{token}/{rel_path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "preview_asset",
    "line": 88
  },
  {
    "method": "GET",
    "path": "/api/v1/artifacts/serve/{project_name}/{file_path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "serve_artifact_file",
    "line": 109
  },
  {
    "method": "POST",
    "path": "/api/v1/artifacts/open",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "open_artifact",
    "line": 130
  },
  {
    "method": "POST",
    "path": "/api/v1/artifacts/reveal",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "reveal_artifact",
    "line": 168
  },
  {
    "method": "DELETE",
    "path": "/api/v1/artifacts/",
    "file": "backend/core_api/cowork/api/v1/endpoints/artifacts.py",
    "function": "delete_artifact_endpoint",
    "line": 193
  },
  {
    "method": "GET",
    "path": "/api/v1/channels/status",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "channel_status",
    "line": 54
  },
  {
    "method": "GET",
    "path": "/api/v1/channels/plugins",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "list_plugins",
    "line": 59
  },
  {
    "method": "GET",
    "path": "/api/v1/channels/installations",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "list_installations",
    "line": 64
  },
  {
    "method": "GET",
    "path": "/api/v1/channels/agent",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "get_channel_agent",
    "line": 77
  },
  {
    "method": "PUT",
    "path": "/api/v1/channels/agent",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "set_channel_agent",
    "line": 88
  },
  {
    "method": "GET",
    "path": "/api/v1/channels/{channel_type}/config",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "get_config",
    "line": 112
  },
  {
    "method": "PUT",
    "path": "/api/v1/channels/{channel_type}/config",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "set_config",
    "line": 120
  },
  {
    "method": "DELETE",
    "path": "/api/v1/channels/{channel_type}/config",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "delete_config",
    "line": 141
  },
  {
    "method": "POST",
    "path": "/api/v1/channels/{channel_type}/reload",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "reload_channel",
    "line": 159
  },
  {
    "method": "GET",
    "path": "/api/v1/channels/bindings",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "list_bindings",
    "line": 174
  },
  {
    "method": "POST",
    "path": "/api/v1/channels/bindings",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "create_binding",
    "line": 179
  },
  {
    "method": "PATCH",
    "path": "/api/v1/channels/bindings/{binding_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "update_binding",
    "line": 189
  },
  {
    "method": "DELETE",
    "path": "/api/v1/channels/bindings/{binding_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "delete_binding",
    "line": 199
  },
  {
    "method": "POST",
    "path": "/api/v1/channels/{channel_type}/setup",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "setup_channel",
    "line": 215
  },
  {
    "method": "POST",
    "path": "/api/v1/channels/{channel_type}/teardown",
    "file": "backend/core_api/cowork/api/v1/endpoints/channels.py",
    "function": "teardown_channel",
    "line": 233
  },
  {
    "method": "GET",
    "path": "/api/v1/connectors/connections/",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/connections.py",
    "function": "list_connections",
    "line": 12
  },
  {
    "method": "GET",
    "path": "/api/v1/connectors/connections/{engine}/{name}",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/connections.py",
    "function": "get_connection",
    "line": 17
  },
  {
    "method": "DELETE",
    "path": "/api/v1/connectors/connections/{engine}/{name}",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/connections.py",
    "function": "delete_connection",
    "line": 25
  },
  {
    "method": "POST",
    "path": "/api/v1/connectors/oauth/{service}/start",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/oauth.py",
    "function": "start_oauth",
    "line": 15
  },
  {
    "method": "GET",
    "path": "/api/v1/connectors/oauth/{service}/callback",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/oauth.py",
    "function": "oauth_callback",
    "line": 22
  },
  {
    "method": "GET",
    "path": "/api/v1/connectors/specs/",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/specs.py",
    "function": "list_connector_specs",
    "line": 15
  },
  {
    "method": "GET",
    "path": "/api/v1/connectors/specs/{connector_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/specs.py",
    "function": "get_connector_spec",
    "line": 20
  },
  {
    "method": "POST",
    "path": "/api/v1/connectors/specs/match",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/specs.py",
    "function": "match_connector_spec",
    "line": 28
  },
  {
    "method": "POST",
    "path": "/api/v1/connectors/submissions/",
    "file": "backend/core_api/cowork/api/v1/endpoints/connectors/submissions.py",
    "function": "submit_form",
    "line": 68
  },
  {
    "method": "GET",
    "path": "/api/v1/conversations/",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "list_conversations",
    "line": 29
  },
  {
    "method": "POST",
    "path": "/api/v1/conversations/",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "create_conversation",
    "line": 49
  },
  {
    "method": "GET",
    "path": "/api/v1/conversations/{conversation_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "get_conversation",
    "line": 64
  },
  {
    "method": "PATCH",
    "path": "/api/v1/conversations/{conversation_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "update_conversation",
    "line": 72
  },
  {
    "method": "GET",
    "path": "/api/v1/conversations/{conversation_id}/items",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "get_messages",
    "line": 90
  },
  {
    "method": "DELETE",
    "path": "/api/v1/conversations/{conversation_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "delete_conversation",
    "line": 98
  },
  {
    "method": "DELETE",
    "path": "/api/v1/conversations/{conversation_id}/turns/{turn_index}",
    "file": "backend/core_api/cowork/api/v1/endpoints/conversations.py",
    "function": "delete_conversation_turn",
    "line": 106
  },
  {
    "method": "POST",
    "path": "/api/v1/files/",
    "file": "backend/core_api/cowork/api/v1/endpoints/files.py",
    "function": "upload_file",
    "line": 18
  },
  {
    "method": "GET",
    "path": "/api/v1/files/",
    "file": "backend/core_api/cowork/api/v1/endpoints/files.py",
    "function": "list_files",
    "line": 27
  },
  {
    "method": "GET",
    "path": "/api/v1/files/{file_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/files.py",
    "function": "retrieve_file",
    "line": 32
  },
  {
    "method": "DELETE",
    "path": "/api/v1/files/{file_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/files.py",
    "function": "delete_file",
    "line": 40
  },
  {
    "method": "GET",
    "path": "/api/v1/files/{file_id}/content",
    "file": "backend/core_api/cowork/api/v1/endpoints/files.py",
    "function": "retrieve_file_content",
    "line": 47
  },
  {
    "method": "GET",
    "path": "/api/v1/health/",
    "file": "backend/core_api/cowork/api/v1/endpoints/health.py",
    "function": "health",
    "line": 22
  },
  {
    "method": "GET",
    "path": "/api/v1/memory/",
    "file": "backend/core_api/cowork/api/v1/endpoints/memory.py",
    "function": "list_memory",
    "line": 87
  },
  {
    "method": "POST",
    "path": "/api/v1/memory/",
    "file": "backend/core_api/cowork/api/v1/endpoints/memory.py",
    "function": "save_memory",
    "line": 109
  },
  {
    "method": "DELETE",
    "path": "/api/v1/memory/",
    "file": "backend/core_api/cowork/api/v1/endpoints/memory.py",
    "function": "delete_memory",
    "line": 138
  },
  {
    "method": "PUT",
    "path": "/api/v1/memory/",
    "file": "backend/core_api/cowork/api/v1/endpoints/memory.py",
    "function": "update_memory_canonical",
    "line": 169
  },
  {
    "method": "GET",
    "path": "/api/v1/pins/",
    "file": "backend/core_api/cowork/api/v1/endpoints/pins.py",
    "function": "list_pins",
    "line": 18
  },
  {
    "method": "POST",
    "path": "/api/v1/pins/",
    "file": "backend/core_api/cowork/api/v1/endpoints/pins.py",
    "function": "pin_item",
    "line": 23
  },
  {
    "method": "POST",
    "path": "/api/v1/pins/{item_id}/visit",
    "file": "backend/core_api/cowork/api/v1/endpoints/pins.py",
    "function": "record_visit",
    "line": 34
  },
  {
    "method": "DELETE",
    "path": "/api/v1/pins/{item_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/pins.py",
    "function": "unpin_item",
    "line": 42
  },
  {
    "method": "GET",
    "path": "/api/v1/projects/{project_name}/instructions",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "get_project_instructions",
    "line": 93
  },
  {
    "method": "GET",
    "path": "/api/v1/projects/{project_name}/files",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "list_project_files",
    "line": 107
  },
  {
    "method": "GET",
    "path": "/api/v1/projects/{project_name}/files/{path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "read_project_file",
    "line": 134
  },
  {
    "method": "PUT",
    "path": "/api/v1/projects/{project_name}/files/{path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "write_project_file",
    "line": 155
  },
  {
    "method": "POST",
    "path": "/api/v1/projects/{project_name}/files/upload",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "upload_project_files",
    "line": 170
  },
  {
    "method": "DELETE",
    "path": "/api/v1/projects/{project_name}/files/{path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "delete_project_file",
    "line": 197
  },
  {
    "method": "POST",
    "path": "/api/v1/projects/preview-mount-file",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "preview_mount_file",
    "line": 209
  },
  {
    "method": "GET",
    "path": "/api/v1/projects/preview-asset/{token}/{rel_path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "preview_asset",
    "line": 227
  },
  {
    "method": "GET",
    "path": "/api/v1/projects/{project_name}/files-raw/{path:path}",
    "file": "backend/core_api/cowork/api/v1/endpoints/project_files.py",
    "function": "download_project_file",
    "line": 246
  },
  {
    "method": "GET",
    "path": "/api/v1/projects/",
    "file": "backend/core_api/cowork/api/v1/endpoints/projects.py",
    "function": "list_projects",
    "line": 17
  },
  {
    "method": "POST",
    "path": "/api/v1/projects/",
    "file": "backend/core_api/cowork/api/v1/endpoints/projects.py",
    "function": "create_project",
    "line": 22
  },
  {
    "method": "PATCH",
    "path": "/api/v1/projects/{project_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/projects.py",
    "function": "update_project",
    "line": 27
  },
  {
    "method": "DELETE",
    "path": "/api/v1/projects/{project_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/projects.py",
    "function": "delete_project",
    "line": 37
  },
  {
    "method": "GET",
    "path": "/api/v1/publish/",
    "file": "backend/core_api/cowork/api/v1/endpoints/publish.py",
    "function": "list_publishable_endpoint",
    "line": 29
  },
  {
    "method": "POST",
    "path": "/api/v1/publish/",
    "file": "backend/core_api/cowork/api/v1/endpoints/publish.py",
    "function": "publish_artifact",
    "line": 34
  },
  {
    "method": "DELETE",
    "path": "/api/v1/publish/",
    "file": "backend/core_api/cowork/api/v1/endpoints/publish.py",
    "function": "unpublish_artifact",
    "line": 49
  },
  {
    "method": "OPTIONS",
    "path": "/api/v1/responses/",
    "file": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "function": "options_handler",
    "line": 61
  },
  {
    "method": "POST",
    "path": "/api/v1/responses/",
    "file": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "function": "responses",
    "line": 73
  },
  {
    "method": "GET",
    "path": "/api/v1/responses/in-flight-list",
    "file": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "function": "in_flight_list",
    "line": 102
  },
  {
    "method": "GET",
    "path": "/api/v1/responses/in-flight",
    "file": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "function": "in_flight",
    "line": 108
  },
  {
    "method": "POST",
    "path": "/api/v1/responses/cancel",
    "file": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "function": "cancel_response",
    "line": 119
  },
  {
    "method": "GET",
    "path": "/api/v1/responses/tail",
    "file": "backend/core_api/cowork/api/v1/endpoints/responses.py",
    "function": "tail_response",
    "line": 126
  },
  {
    "method": "GET",
    "path": "/api/v1/schedules/",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "list_schedules",
    "line": 24
  },
  {
    "method": "POST",
    "path": "/api/v1/schedules/",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "create_schedule",
    "line": 30
  },
  {
    "method": "GET",
    "path": "/api/v1/schedules/{schedule_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "get_schedule",
    "line": 45
  },
  {
    "method": "PUT",
    "path": "/api/v1/schedules/{schedule_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "update_schedule",
    "line": 54
  },
  {
    "method": "PATCH",
    "path": "/api/v1/schedules/{schedule_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "update_schedule",
    "line": 54
  },
  {
    "method": "DELETE",
    "path": "/api/v1/schedules/{schedule_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "delete_schedule",
    "line": 66
  },
  {
    "method": "POST",
    "path": "/api/v1/schedules/{schedule_id}/pause",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "pause_schedule",
    "line": 73
  },
  {
    "method": "POST",
    "path": "/api/v1/schedules/{schedule_id}/resume",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "resume_schedule",
    "line": 81
  },
  {
    "method": "POST",
    "path": "/api/v1/schedules/{schedule_id}/run-now",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "run_schedule_now",
    "line": 89
  },
  {
    "method": "GET",
    "path": "/api/v1/schedules/{schedule_id}/runs",
    "file": "backend/core_api/cowork/api/v1/endpoints/schedules.py",
    "function": "list_schedule_runs",
    "line": 117
  },
  {
    "method": "GET",
    "path": "/api/v1/search",
    "file": "backend/core_api/cowork/api/v1/endpoints/search.py",
    "function": "search_cowork",
    "line": 34
  },
  {
    "method": "GET",
    "path": "/api/v1/settings/",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "list_settings",
    "line": 44
  },
  {
    "method": "PUT",
    "path": "/api/v1/settings/{key}",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "upsert_setting",
    "line": 49
  },
  {
    "method": "DELETE",
    "path": "/api/v1/settings/{key}",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "delete_setting",
    "line": 61
  },
  {
    "method": "POST",
    "path": "/api/v1/settings/validate",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "validate_settings",
    "line": 78
  },
  {
    "method": "GET",
    "path": "/api/v1/settings/configured",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "check_configured",
    "line": 91
  },
  {
    "method": "GET",
    "path": "/api/v1/settings/install-status",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "install_status",
    "line": 103
  },
  {
    "method": "GET",
    "path": "/api/v1/settings/reveal-key/{name}",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "reveal_key",
    "line": 108
  },
  {
    "method": "POST",
    "path": "/api/v1/settings/test-providers",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "test_providers",
    "line": 127
  },
  {
    "method": "POST",
    "path": "/api/v1/settings/validate-provider",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "validate_provider_endpoint",
    "line": 158
  },
  {
    "method": "GET",
    "path": "/api/v1/settings/recommended-models",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "recommended_models",
    "line": 163
  },
  {
    "method": "GET",
    "path": "/api/v1/settings/raw",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "read_raw_settings",
    "line": 191
  },
  {
    "method": "POST",
    "path": "/api/v1/settings/raw",
    "file": "backend/core_api/cowork/api/v1/endpoints/settings.py",
    "function": "write_raw_settings",
    "line": 212
  },
  {
    "method": "GET",
    "path": "/api/v1/skills/",
    "file": "backend/core_api/cowork/api/v1/endpoints/skills.py",
    "function": "list_skills",
    "line": 16
  },
  {
    "method": "POST",
    "path": "/api/v1/skills/",
    "file": "backend/core_api/cowork/api/v1/endpoints/skills.py",
    "function": "create_skill",
    "line": 22
  },
  {
    "method": "GET",
    "path": "/api/v1/skills/{skill_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/skills.py",
    "function": "get_skill",
    "line": 37
  },
  {
    "method": "PUT",
    "path": "/api/v1/skills/{skill_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/skills.py",
    "function": "update_skill",
    "line": 45
  },
  {
    "method": "DELETE",
    "path": "/api/v1/skills/{skill_id}",
    "file": "backend/core_api/cowork/api/v1/endpoints/skills.py",
    "function": "delete_skill",
    "line": 61
  }
]
```
