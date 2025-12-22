# granite.config.ts Schema Reference (React Native)

This document describes the expected structure and fields for `granite.config.ts` in apps-in-toss **React Native projects** using the Granite plugin system.

**Note:** This schema is specific to React Native-based apps. For web apps, see [web-granite-config-schema.md](web-granite-config-schema.md).

## Required Structure

A valid `granite.config.ts` file must:

1. Import `defineConfig` from `@granite-js/react-native/config`
2. Import `appsInToss` from `@apps-in-toss/framework/plugins`
3. Export a default configuration using `defineConfig()`
4. Include all required fields

## Example

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-native-app',
  entryFile: './src/_app.tsx',
  outdir: 'dist',
  cwd: process.cwd(),
  build: {
    resolver: {
      alias: [
        { from: '@components', to: './src/components', exact: false }
      ],
    },
  },
  metro: {
    resolver: {
      conditionNames: ['react-native', 'require', 'node', 'default'],
    },
  },
  devServer: {
    middlewares: [],
  },
  plugins: [
    appsInToss({
      brand: {
        displayName: 'My Native App',
        primaryColor: '#0064FF',
        icon: 'https://static.toss.im/icons/app-icon.png',
      },
      permissions: [
        { name: 'clipboard', access: 'read' },
        { name: 'geolocation', access: 'access' },
      ],
      navigationBar: {
        withBackButton: true,
        withHomeButton: false,
      },
    }),
  ],
});
```

## Required Fields

### `scheme` (string, required)
URL scheme for deep linking (e.g., 'intoss', 'granite').

```typescript
scheme: 'intoss'
```

### `appName` (string, required)
Unique identifier for your microservice/application.

```typescript
appName: 'my-native-app'
```

## Optional Fields

### `host` (string, optional)
Host name used in the URL pattern (e.g., 'scheme://host/app-name'). Optional when using default routing.

```typescript
host: 'my-app'
```

### `entryFile` (string, optional)
Application entry point. Defaults to `'./src/_app.tsx'`.

```typescript
entryFile: './src/index.tsx'
```

### `outdir` (string, optional)
Build output directory. Defaults to `'dist'`.

```typescript
outdir: 'build'
```

### `cwd` (string, optional)
Working directory for the build process. Defaults to `process.cwd()`.

```typescript
cwd: __dirname
```

### `build` (BuildConfig, optional)
Bundler customization settings for the build process.

#### `build.resolver` (ResolverConfig, optional)
Module resolution configuration.

**`alias`** (AliasConfig[], optional)
Array of module alias configurations:

```typescript
build: {
  resolver: {
    alias: [
      {
        from: '@components',
        to: './src/components',
        exact: false
      },
      {
        from: '@utils',
        to: './src/utils',
        exact: false
      }
    ],
  }
}
```

Each alias config contains:
- `from` (string): Source module name to match
- `to` (string | AliasResolver): Target path or resolver function
- `exact` (boolean): If true, only exact matches; if false, matches subpaths too

**`protocol`** (ProtocolConfig[], optional)
Custom protocol handlers for non-standard import protocols:

```typescript
build: {
  resolver: {
    protocol: [
      {
        protocol: 'custom',
        resolve: async (path, context) => {
          // Custom resolution logic
          return { path: resolvedPath };
        },
        load: async (args) => {
          // Custom loading logic
          return { contents: code, loader: 'js' };
        }
      }
    ]
  }
}
```

#### `build.transformer` (TransformerConfig, optional)
Code transformation hooks for custom processing:

```typescript
build: {
  transformer: {
    transformSync: (id, code) => {
      // Synchronous transformation
      return transformedCode;
    },
    transformAsync: async (id, code) => {
      // Asynchronous transformation
      return transformedCode;
    }
  }
}
```

#### `build.esbuild` (EsbuildConfig, optional)
Esbuild-specific configuration:

```typescript
build: {
  esbuild: {
    prelude: 'console.log("App starting...");',
    // Other esbuild options...
  }
}
```

- `prelude` (string, optional): Script to inject at the entry point

#### `build.swc` (SwcConfig, optional)
SWC transformer configuration with plugin support:

```typescript
build: {
  swc: {
    jsc: {
      parser: {
        syntax: 'typescript',
        tsx: true,
      },
    },
  }
}
```

#### `build.babel` (BabelConfig, optional)
Babel transformation settings:

```typescript
build: {
  babel: {
    skip: (id) => id.includes('node_modules'),
    configFile: './babel.config.js',
    presets: ['@babel/preset-react'],
    plugins: ['@babel/plugin-transform-runtime']
  }
}
```

Contains:
- `skip` (function, optional): Conditional skip rules for files
- `configFile` (string, optional): Path to babel config file
- `presets` (array, optional): Babel presets
- `plugins` (array, optional): Babel plugins

### `metro` (AdditionalMetroConfig, optional)
Metro bundler configuration.

#### `metro.serializer` (object, optional)
Partial support for Metro serializer options:

```typescript
metro: {
  serializer: {
    getPolyfills: () => [require.resolve('./polyfills.js')]
  }
}
```

- `getPolyfills` (function, optional): Returns array of polyfill file paths

#### `metro.resolver` (object, optional)
Partial support for Metro resolver options:

```typescript
metro: {
  resolver: {
    blockList: [/node_modules\/react-native-gesture-handler\/.*/],
    resolverMainFields: ['react-native', 'browser', 'main'],
    conditionNames: ['react-native', 'require', 'node', 'default'],
    resolveRequest: (context, moduleName, platform) => {
      // Custom resolution logic
      return { filePath: resolvedPath };
    }
  }
}
```

- `blockList` (RegExp[], optional): Patterns to exclude from bundling
- `resolverMainFields` (string[], optional): Priority order for package.json fields
- `conditionNames` (string[], optional): Export condition names (defaults to `['react-native', 'require', 'node', 'default']`)
- `resolveRequest` (function, optional): Custom module resolution

#### `metro.reporter` (object, optional)
Metro reporter configuration for build progress/status reporting.

#### `metro.babelConfig` (babel.TransformOptions, optional)
Babel configuration for Metro:

```typescript
metro: {
  babelConfig: {
    presets: ['module:metro-react-native-babel-preset'],
    plugins: ['react-native-reanimated/plugin']
  }
}
```

#### `metro.transformSync` (function, optional)
Synchronous transformation function:

```typescript
metro: {
  transformSync: (id, code) => {
    return transformedCode;
  }
}
```

#### `metro.projectRoot` (string, optional)
Metro project root directory.

### `devServer` (DevServerConfig, optional)
Development server configuration using Fastify.

#### `devServer.middlewares` (Middleware[], optional)
Array of Fastify plugins (async or callback-based):

```typescript
devServer: {
  middlewares: [
    async (fastify, opts) => {
      fastify.get('/api/health', async () => {
        return { status: 'ok' };
      });
    }
  ]
}
```

#### `devServer.inspectorProxy` (InspectorProxyConfig, optional)
Chrome DevTools Protocol configuration:

```typescript
devServer: {
  inspectorProxy: {
    delegate: {
      onDeviceMessage: (message, socket) => {
        // Handle device messages
        return true; // or false
      },
      onDebuggerMessage: (message, socket) => {
        // Handle debugger messages
        return true; // or false
      }
    }
  }
}
```

- `delegate.onDeviceMessage` (function, optional): Intercept messages from device
- `delegate.onDebuggerMessage` (function, optional): Intercept messages from debugger

### `plugins` (PluginInput[], optional)
Array of Granite plugins to extend functionality:

```typescript
import { appsInToss } from '@apps-in-toss/framework/plugins';

plugins: [
  appsInToss({
    brand: {
      displayName: 'My App',
      primaryColor: '#3182F6',
      icon: 'https://example.com/icon.png',
    },
    permissions: [
      { name: 'clipboard', access: 'read' },
      { name: 'camera', access: 'access' },
    ],
    navigationBar: {
      withBackButton: true,
      withHomeButton: false,
    },
  }),
  myCustomPlugin(),
  {
    name: 'inline-plugin',
    dev: {
      order: 'pre',
      handler: async (context, args) => {
        // Pre-dev hook logic
      }
    },
    build: {
      order: 'post',
      handler: async (context, args) => {
        // Post-build hook logic
      }
    }
  }
]
```

Each plugin can be:
- A resolved plugin object
- A promise resolving to a plugin
- An array of plugins (recursive)

Plugin structure:
- `name` (string, required): Plugin identifier
- `dev` (object, optional): Development mode handler
  - `order`: `'pre'` | `'post'`
  - `handler`: Async/sync function
- `build` (object, optional): Build mode handler
  - `order`: `'pre'` | `'post'`
  - `handler`: Async/sync function
- `config` (PluginConfig, optional): Plugin-specific configuration

#### Apps-in-Toss Plugin (`appsInToss`)

The `appsInToss` plugin is a core plugin for Apps-in-Toss React Native projects. It sets up micro-frontend architecture, runtime configuration, and deployment artifacts.

**Import:**
```typescript
import { appsInToss } from '@apps-in-toss/framework/plugins';
```

**Options (AppsInTossPluginOptions):**

**`brand`** (object, required)
Brand configuration with display name, colors, and icon.

```typescript
appsInToss({
  brand: {
    displayName: 'My App',
    primaryColor: '#0064FF',
    icon: 'https://example.com/icon.png',
  },
  // ...
})
```

Properties:
- `displayName` (string, required): Display name of the app shown to users
- `primaryColor` (string, required): Primary brand color in hex format (e.g., `'#3182F6'`)
- `icon` (string, required): URL to the app icon image

**`permissions`** (Permission[], required)
Array of permissions required by the app.

```typescript
appsInToss({
  permissions: [
    { name: 'clipboard', access: 'read' },
    { name: 'geolocation', access: 'access' },
    { name: 'camera', access: 'access' },
  ],
  // ...
})
```

Available permissions:
- `clipboard`: `{ name: 'clipboard', access: 'read' | 'write' }`
- `geolocation`: `{ name: 'geolocation', access: 'access' }`
- `contacts`: `{ name: 'contacts', access: 'read' | 'write' }`
- `photos`: `{ name: 'photos', access: 'read' | 'write' }`
- `camera`: `{ name: 'camera', access: 'access' }`

**`appType`** (string, optional)
Type of application. Allowed values: `'general'` | `'game'`. Defaults to `'general'`.

```typescript
appsInToss({
  appType: 'game',
  // ...
})
```

**`navigationBar`** (object, optional)
Navigation bar configuration for the app.

```typescript
appsInToss({
  navigationBar: {
    withBackButton: true,
    withHomeButton: false,
    initialAccessoryButton: {
      id: 'share',
      title: 'Share',
      icon: { name: 'share' },
    },
  },
  // ...
})
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

**What the plugin does:**

The `appsInToss` plugin automatically configures:
1. **Micro-frontend setup** - Configures module federation with predefined remote name and expose paths
2. **Runtime setup script** - Injects app metadata (appType, brand, deploymentId, navigationBar) into global scope
3. **Metro config** - Adds runtime setup script to Metro bundler
4. **Esbuild config** - Adds runtime setup script to esbuild
5. **App manifest** - Generates `app.json` with app metadata, permissions, and deployment info
6. **Bedrock compatibility** - Ensures compatibility with Bedrock runtime (as guest/non-host)
7. **Dev server hooks** - Adds development server middleware and utilities
8. **Build artifacts** - Creates deployment artifacts with generated deployment ID (UUID format)
9. **Post-build notices** - Displays build completion and deployment information

**Full example (based on real Apps-in-Toss project):**

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-app',
  plugins: [
    appsInToss({
      brand: {
        displayName: '마이앱',
        primaryColor: '#3182F6',
        icon: 'https://www.granite.run/granite.png',
      },
      navigationBar: {
        withHomeButton: true,
        withBackButton: true,
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
        { name: 'contacts', access: 'write' },
        { name: 'photos', access: 'read' },
        { name: 'photos', access: 'write' },
        { name: 'camera', access: 'access' },
        { name: 'clipboard', access: 'read' },
        { name: 'clipboard', access: 'write' },
        { name: 'geolocation', access: 'access' },
      ],
    }),
  ],
});
```

## Validation Rules

The validator should check for:

1. ✅ File exists
2. ✅ Contains `defineConfig` function call
3. ✅ Imports `defineConfig` from `@granite-js/react-native/config`
4. ✅ Has `export default defineConfig` statement
5. ✅ Contains required fields: `scheme`, `appName`
6. ✅ Contains `appsInToss` plugin in plugins array (required for Apps-in-Toss projects)
7. ✅ `appsInToss` plugin has required fields: `brand` (with `displayName`, `primaryColor`, `icon`), `permissions`
8. ⚠️ Warns if optional recommended fields are missing (e.g., `navigationBar`)
9. ⚠️ Validates plugin array structure if present

## Common Patterns

### Apps-in-Toss Mini App (Real Example)

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-app',
  plugins: [
    appsInToss({
      brand: {
        displayName: '마이앱',
        primaryColor: '#3182F6',
        icon: 'https://static.toss.im/ml-product/tosst_22367_1_rembg_upscaled.png',
      },
      navigationBar: {
        withHomeButton: true,
        withBackButton: true,
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
        { name: 'contacts', access: 'write' },
        { name: 'photos', access: 'read' },
        { name: 'photos', access: 'write' },
        { name: 'camera', access: 'access' },
        { name: 'clipboard', access: 'read' },
        { name: 'clipboard', access: 'write' },
        { name: 'geolocation', access: 'access' },
      ],
    }),
  ],
});
```

### Full Metro Configuration

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-app',
  metro: {
    resolver: {
      conditionNames: ['react-native', 'require', 'node', 'default'],
      blockList: [/node_modules\/.*\/__(tests|mocks)__\/.*/],
    },
    babelConfig: {
      presets: ['module:metro-react-native-babel-preset'],
    },
  },
  plugins: [
    appsInToss({
      brand: {
        displayName: 'My App',
        primaryColor: '#0064FF',
        icon: 'https://static.toss.im/icons/app-icon.png',
      },
      permissions: [
        { name: 'clipboard', access: 'read' },
      ],
    }),
  ],
});
```

### Build Customization

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-app',
  build: {
    resolver: {
      alias: [
        { from: '@', to: './src', exact: false },
      ],
    },
    babel: {
      skip: (id) => /node_modules/.test(id),
      presets: ['@babel/preset-typescript'],
    },
  },
  plugins: [
    appsInToss({
      brand: {
        displayName: 'My App',
        primaryColor: '#0064FF',
        icon: 'https://static.toss.im/icons/app-icon.png',
      },
      permissions: [],
    }),
  ],
});
```

### Development Server with Middleware

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-app',
  devServer: {
    middlewares: [
      async (fastify) => {
        fastify.get('/health', async () => ({ status: 'ok' }));
      },
    ],
  },
  plugins: [
    appsInToss({
      brand: {
        displayName: 'My App',
        primaryColor: '#0064FF',
        icon: 'https://static.toss.im/icons/app-icon.png',
      },
      permissions: [],
    }),
  ],
});
```

## Differences from Web Configuration

Key differences from the web framework configuration:

1. **React Native uses Metro bundler** instead of web bundlers
2. **Platform-specific settings** for iOS/Android via Metro config
3. **Native navigation** settings instead of web routing
4. **DevServer uses Fastify** middleware instead of web middleware
5. **Custom protocol handlers** for native module resolution
6. **Inspector proxy** for React Native debugging tools

## TypeScript Support

The configuration is fully typed when using TypeScript:

```typescript
import { defineConfig } from '@granite-js/react-native/config';
import { appsInToss } from '@apps-in-toss/framework/plugins';

export default defineConfig({
  scheme: 'intoss',
  appName: 'my-app',
  plugins: [
    appsInToss({
      brand: {
        displayName: 'My App',
        primaryColor: '#3182F6',
        icon: 'https://static.toss.im/icons/app-icon.png',
      },
      permissions: [],
    }),
  ],
  // TypeScript will provide autocomplete and type checking
});
```
