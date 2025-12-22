# Unity Game Project Validation Guide

This document provides validation guidelines for Unity-based game projects in the Apps-in-Toss ecosystem.

## Overview

Unity games for Apps-in-Toss are **WebGL builds** that integrate with the platform through the Apps-in-Toss Unity SDK or custom JavaScript bridges.

**Important:** Unity games follow the **web framework configuration** since they are WebGL-based. Always refer to [web-granite-config-schema.md](web-granite-config-schema.md) for `granite.config.ts` structure.

## Additional references (Apps-in-Toss Unity docs)

- Getting started: [Unity overview](https://developers-apps-in-toss.toss.im/unity/intro/overview.md)
- Preparation: [Runtime structure](https://developers-apps-in-toss.toss.im/unity/guide/runtime-structure.md), [Precheck](https://developers-apps-in-toss.toss.im/unity/guide/precheck.md), [Recommended Unity versions](https://developers-apps-in-toss.toss.im/unity/guide/recommend-engine.md)
- Porting: [Migration sequence](https://developers-apps-in-toss.toss.im/unity/intro/migration-guide.md), [Unity SDK](https://developers-apps-in-toss.toss.im/unity/porting-tutorials/unity-sdk.md), [Unity porting tutorial](https://developers-apps-in-toss.toss.im/unity/porting-tutorials/unity.md)
- Optimization: [Performance guide](https://developers-apps-in-toss.toss.im/unity/optimization/perf-optimization.md), [Evaluation criteria](https://developers-apps-in-toss.toss.im/unity/optimization/perf-measure.md), [Runtime performance](https://developers-apps-in-toss.toss.im/unity/optimization/runtime/performance.md), [Startup](https://developers-apps-in-toss.toss.im/unity/optimization/start/startup-speed.md), [Loading/resources/memory/rendering/platform-specific](https://developers-apps-in-toss.toss.im/unity/optimization/start/loading.md) and related sub-guides
- Debugging: [Unity WebGL debugging & exceptions](https://developers-apps-in-toss.toss.im/unity/debug/debug-exception.md)

## What to validate from official Unity docs

- Platform model (overview/runtime-structure): WebGL build → WASM + JS bridge → Apps-in-Toss web runtime (Vite bundler, Granite build). Must use web-framework config, not React Native.
- Precheck (compatibility): WebGL only (no native plugins); file I/O and sockets limited; AR/XR/Compute highly constrained; target touch/mobile form factors; memory-sensitive (< ~200MB ideal).
- Engine versions (recommend-engine): Prefer Unity 2023.3 LTS (best perf/GC/WASM); 2022.3 LTS acceptable/stable; 2021.3 LTS legacy support; 2024.2 LTS is experimental (avoid for production).
- Migration flow (migration-guide): 1) Precheck 2) Convert to WebGL package 3) Integrate Apps-in-Toss SDK (auth/pay/etc.) 4) Optimize UX/perf 5) Package `.ait` + monitor after release.
- Performance targets (perf-optimization, perf-measure): Startup <3s target (<5s max), avg FPS ≥30 on mobile, memory <200MB (critical >300MB), first frame <5s, battery ~90–110% of native acceptable.
- Runtime optimization (runtime/performance): Expect adaptive frame-rate/quality, batching/instancing, LOD/culling, pooled updates (avoid heavy per-frame work), GPU/CPU profiling enabled.
- Startup (startup-speed): No heavy work on first frame; split initialization into phases, measure phases; WASM size trimmed (Brotli, stripping), early UI shown fast.
- Loading (loading.md): Priority-based groups (critical/high/background/on-demand), progressive loading, addressables/asset bundles, cache limits and unload paths; scene transitions under ~2s where possible.
- Debugging (debug-exception): Centralized logging to web/Apps-in-Toss, exception handler with recovery, in-app debug console/profiler hooks for WebGL.

## Project Type Detection

A project is identified as a Unity game if:
- `appType: 'game'` is set in `granite.config.ts`
- Unity WebGL build artifacts are present in the project
- Project references Unity SDK packages or has Unity-specific build configuration

## Recommended Setup

### Apps-in-Toss Unity SDK (Strongly Recommended)

**Package:** `apps-in-toss-unity-sdk`
**Installation:** Unity Package Manager via Git URL

```
https://github.com/toss/apps-in-toss-unity-sdk.git
```

**Installation Steps:**
1. Open Unity Editor
2. Navigate to `Window → Package Manager`
3. Click the `+` button
4. Select "Add package from git URL"
5. Enter the Git URL above

### SDK Benefits

1. **C# API Layer**: Direct invocation of Apps-in-Toss features using `DllImport("__Internal")`
2. **JavaScript Bridge**: Automated connection between C# code and WebView SDK
3. **Build Automation**: Automated WebGL building and `.ait` file generation
4. **AIT Menu**: Unity editor menu for:
   - Dev/Production server testing
   - Build & Package automation
   - Configuration (app ID, display name, icons)
   - Direct publish to Apps-in-Toss console
5. **Simplified Integration**: No need to create separate Vite project or implement JS Bridge manually

### API Usage Pattern

All APIs follow async patterns:

```csharp
var deviceId = await AIT.GetDeviceId();
var userInfo = await AIT.GetUserInfo();
```

## Validation Checklist

### Required (granite.config.ts)

Since Unity games are WebGL-based, they must follow **web framework requirements** from [web-granite-config-schema.md](web-granite-config-schema.md):

- ✅ `appName` (string)
- ✅ `brand` object with `displayName`, `primaryColor`, `icon`
- ✅ `permissions` array (can be empty for basic games)
- ✅ `web.port` (number)
- ✅ `web.commands.dev` (string)
- ✅ `web.commands.build` (string)

### Strongly Recommended

- ⚠️ **Apps-in-Toss Unity SDK installed** via Package Manager
- ⚠️ WebGL build target configured in Unity
- ⚠️ Proper `.ait` packaging configuration

### Not Required for Games

- ❌ **TDS (Toss Design System)**: Not needed for game apps
- ❌ Custom UI frameworks: Games can use their own UI systems

## Common Validation Issues

### Issue: Unity SDK Not Installed

**Detection:**
- No reference to `apps-in-toss-unity-sdk` in Unity packages
- Manual JavaScript bridge implementation present
- Missing AIT menu in Unity editor

**Solution:**
Install the SDK via Package Manager:
```
https://github.com/toss/apps-in-toss-unity-sdk.git
```

**Benefits:**
- Simplified integration workflow
- Automated build and packaging
- Built-in testing tools
- Direct console publishing

### Issue: Incorrect Configuration Structure

**Detection:**
- Unity WebGL project not following web framework structure
- Missing web framework configuration

**Solution:**
Unity games **must use web framework configuration** since they are WebGL-based:

```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'my-unity-game',
  brand: {
    displayName: 'My Game',
    primaryColor: '#3182F6',
    icon: 'https://static.toss.im/icons/game-icon.png',
  },
  permissions: [],
  web: {
    host: 'localhost',
    port: 3000,
    commands: {
      dev: 'npm run dev',
      build: 'npm run build',
    },
  },
  webViewProps: {
    type: 'game', // Optional: Identifies as game type
  },
  outdir: 'dist',
});
```

**Note:** Unity games do NOT use React Native configuration. They follow web configuration because Unity compiles to WebGL.

### Issue: Missing Required Permissions

**Detection:**
Game needs device features (camera, geolocation, etc.) but permissions array is empty

**Solution:**
Add necessary permissions to granite.config.ts:

```typescript
permissions: [
  { name: 'camera', access: 'access' },
  { name: 'geolocation', access: 'access' },
]
```

## Testing Requirements

**Important:** Apps-in-Toss AIT API does not function in regular browser environments.

**Valid Testing Environments:**
1. **Sandbox App**: Official testing environment
2. **`.ait` File Deployment**: Upload through Apps-in-Toss console

**Cannot Test In:**
- Local development browser
- Standard WebGL preview
- External web hosting

## Build Output Validation

### WebGL Build Artifacts

Check for Unity WebGL build output:
- `Build/` or `dist/` directory with WebGL files
- `index.html` entry point
- `.data`, `.wasm`, `.framework.js` files

### AIT Package

For SDK users, check for `.ait` file generation:
- Automated by SDK's Build & Package feature
- Contains WebGL build + Apps-in-Toss metadata
- Ready for console upload

## Example Unity Game Configuration

### Full Configuration (WebGL - Web Framework)

```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'unity-puzzle-game',
  brand: {
    displayName: 'Puzzle Master',
    primaryColor: '#FF6B6B',
    icon: 'https://static.toss.im/game-icons/puzzle.png',
  },
  web: {
    host: 'localhost',
    port: 3000,
    commands: {
      dev: 'vite --port 3000',
      build: 'vite build',
    },
  },
  navigationBar: {
    withHomeButton: true,
  },
  permissions: [],
  outdir: 'dist',
});
```

## Validation Report Example

```
Validating apps-in-toss Unity game project...

✅ package.json found and valid
✅ granite.config.ts found

Project Type: Web (detected @apps-in-toss/web-framework v1.2.0)
App Type: game (Unity WebGL)
Unity Build: Detected WebGL artifacts in dist/

✅ All required fields present
✅ appType correctly set to 'game'
✅ Brand configuration valid
✅ Permissions configured

⚠️ Recommendations:
1. Apps-in-Toss Unity SDK not detected
   Benefit: Simplified integration and automated build process
   Installation: Unity Package Manager → Add from git URL
   Git URL: https://github.com/toss/apps-in-toss-unity-sdk.git
   Documentation: https://developers-apps-in-toss.toss.im/unity/porting-tutorials/unity-sdk

Note: TDS (Toss Design System) is not required for game apps
```

## Documentation References

- **Unity SDK Installation**: https://developers-apps-in-toss.toss.im/unity/porting-tutorials/unity-sdk
- **Unity SDK GitHub**: https://github.com/toss/apps-in-toss-unity-sdk
- **Apps-in-Toss Developer Portal**: https://developers-apps-in-toss.toss.im

## Key Differences from Non-Game Apps

| Aspect | Non-Game Web Apps | Unity Games (WebGL) |
|--------|------------------|---------------------|
| **Framework** | @apps-in-toss/web-framework | @apps-in-toss/web-framework |
| **Configuration** | web-granite-config-schema.md | **Same** web-granite-config-schema.md |
| **TDS Requirement** | Strongly recommended | Not required |
| **UI Framework** | TDS components | Unity UI or custom |
| **Build Process** | Vite bundler | Unity WebGL → Vite bundler |
| **Additional SDK** | None | Unity SDK (recommended) |
| **Testing** | Browser + Device | Sandbox/Console only |
| **Packaging** | Standard .ait | Unity SDK automated |

## Summary

Unity game projects are **WebGL-based** and follow web framework configuration:

1. **Use web framework** (`@apps-in-toss/web-framework`) - Unity compiles to WebGL
2. **Follow web-granite-config-schema.md** for `granite.config.ts` structure
3. **Install Unity SDK** for simplified integration (strongly recommended)
4. **TDS is not required** - use Unity's own UI systems
5. **Test in proper environment** - Sandbox or console deployment only
6. **Configure permissions** based on game features needed

**Important:** Do NOT use React Native configuration for Unity games. Unity games are web-based (WebGL), not native.
