# granite.config.ts Schema Reference (Web Framework)

This document describes the expected structure and fields for `granite.config.ts` in apps-in-toss **web projects** using `@apps-in-toss/web-framework`.

**Note:** This schema is specific to web-based apps. For native or other app types, the configuration structure may differ.

## Required Structure

A valid `granite.config.ts` file must:

1. Import `defineConfig` from `@apps-in-toss/web-framework/config`
2. Export a default configuration using `defineConfig()`
3. Include all required fields

## Example

```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'my-web',
  brand: {
    displayName: '마이웹',
    primaryColor: '#3182F6',
    icon: 'https://www.granite.run/granite.png',
  },
  web: {
    host: 'localhost',
    port: 3000,
    commands: {
      dev: 'vite --port 3000',
      build: 'vite build',
    },
  },
  webViewProps: {
    type: 'partner',
  },
  navigationBar: {
    withHomeButton: true,
    initialAccessoryButton: {
      id: 'init-heart',
      title: '버튼 이름',
      icon: {
        name: 'icon-heart-mono',
      },
    },
  },
  permissions: [
    { name: 'contacts', access: 'read' },
    { name: 'photos', access: 'read' },
    { name: 'photos', access: 'write' },
    { name: 'camera', access: 'access' },
    { name: 'clipboard', access: 'read' },
    { name: 'clipboard', access: 'write' },
    { name: 'geolocation', access: 'access' },
  ],
  outdir: 'dist',
});
```

## Required Fields

### `appName` (string, required)
The name of your app.

```typescript
appName: 'my-app'
```

### `brand` (object, required)
Brand configuration with display name, colors, and icon.

```typescript
brand: {
  displayName: '마이웹',
  primaryColor: '#3182F6',
  icon: 'https://static.toss.im/ml-product/tosst_22367_1_rembg_upscaled.png',
}
```

Properties:
- `displayName` (string, required): Display name of the app shown to users
- `primaryColor` (string, required): Primary brand color in hex format (e.g., `'#3182F6'`)
- `icon` (string, required): URL to the app icon image

### `permissions` (Permission[], required)
Array of permissions required by the app.

```typescript
permissions: [
  { name: 'clipboard', access: 'read' },
  { name: 'geolocation', access: 'access' },
  { name: 'camera', access: 'access' },
]
```

Available permissions:
- `clipboard`: `{ name: 'clipboard', access: 'read' | 'write' }`
- `geolocation`: `{ name: 'geolocation', access: 'access' }`
- `contacts`: `{ name: 'contacts', access: 'read' | 'write' }`
- `photos`: `{ name: 'photos', access: 'read' | 'write' }`
- `camera`: `{ name: 'camera', access: 'access' }`

### `web.port` (number, required)
Port number for the development server.

```typescript
web: {
  port: 3000
}
```

### `web.commands.dev` (string, required)
Command to run the development server.

```typescript
web: {
  commands: {
    dev: 'npm run dev'
  }
}
```

### `web.commands.build` (string, required)
Command to build the project.

```typescript
web: {
  commands: {
    build: 'npm run build'
  }
}
```

## Optional Fields

### `web.host` (string, optional)
Host for the development server. Defaults to `'localhost'`.

### `scheme` (string, optional)
URL scheme. Defaults to `'intoss'`.

### `outdir` (string, optional)
Output directory for build files. Defaults to `'dist'`.

### `webViewProps` (object, optional)
Configuration for the WebView component. See full type definition in the framework documentation.

Common options:
- `type`: `'partner'` | `'external'` | `'game'` (default: `'partner'`)
- `allowsInlineMediaPlayback`: boolean (default: `false`, iOS only)
- `bounces`: boolean (default: `true`, iOS only)
- `pullToRefreshEnabled`: boolean (default: `true`, iOS only)
- `overScrollMode`: `'always'` | `'content'` | `'never'` (default: `'always'`, Android only)
- `mediaPlaybackRequiresUserAction`: boolean (default: `true`)
- `allowsBackForwardNavigationGestures`: boolean (default: `true`)

### `navigationBar` (object, optional)
Navigation bar configuration.

```typescript
navigationBar: {
  withBackButton: true,
  withHomeButton: false,
  initialAccessoryButton: {
    id: 'share',
    title: 'Share',
    icon: { name: 'share' },
  },
}
```

Properties:
- `withBackButton` (boolean, optional): Enable/disable back button
- `withHomeButton` (boolean, optional): Enable/disable home button
- `initialAccessoryButton` (object, optional): Accessory button configuration
  - `id` (string, required): Unique identifier for the button
  - `title` (string, required): Button title text
  - `icon` (Icon, required): Button icon, either:
    - `{ name: string }` - Built-in icon name
    - `{ source: { uri: string } }` - Custom icon from URL

## Common Patterns

### Full Web App Configuration (Real Example)

```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'my-web',
  brand: {
    displayName: '인토스웹',
    primaryColor: '#3182F6',
    icon: 'https://static.toss.im/ml-product/tosst_22367_1_rembg_upscaled.png',
  },
  web: {
    host: 'localhost',
    port: 3000,
    commands: {
      dev: 'vite --port 3000',
      build: 'vite build',
    },
  },
  webViewProps: {
    type: 'partner',
  },
  navigationBar: {
    withHomeButton: true,
    initialAccessoryButton: {
      id: 'init-heart',
      title: '버튼 이름',
      icon: {
        name: 'icon-heart-mono',
      },
    },
  },
  permissions: [
    { name: 'contacts', access: 'read' },
    { name: 'photos', access: 'read' },
    { name: 'photos', access: 'write' },
    { name: 'camera', access: 'access' },
    { name: 'clipboard', access: 'read' },
    { name: 'clipboard', access: 'write' },
    { name: 'geolocation', access: 'access' },
  ],
  outdir: 'dist',
});
```

### Minimal Configuration

```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'my-web-app',
  brand: {
    displayName: 'My App',
    primaryColor: '#3182F6',
    icon: 'https://static.toss.im/icons/app-icon.png',
  },
  permissions: [],
  web: {
    port: 3000,
    commands: {
      dev: 'npm run dev',
      build: 'npm run build',
    },
  },
});
```

## Validation Rules

The validator checks for:

1. ✅ File exists
2. ✅ Contains `defineConfig` function call
3. ✅ Imports from `@apps-in-toss/web-framework/config`
4. ✅ Has `export default defineConfig` statement
5. ✅ Contains required fields: `appName`, `brand` (with `displayName`, `primaryColor`, `icon`), `permissions`, `web.port`, `web.commands.dev`, `web.commands.build`
6. ⚠️ Warns if optional recommended fields are missing (e.g., `navigationBar`, `webViewProps`)
