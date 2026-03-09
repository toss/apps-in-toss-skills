# Validation Policies

This document outlines all validation rules and policies for apps-in-toss projects.

## Critical Validations

These validations must pass for a project to be considered valid:

### 1. Project Structure

**Required files:**
- `package.json` - Project manifest and dependencies
- `granite.config.ts` - Apps-in-toss configuration file

**Common directories (warnings if missing):**
- `src/` - Source code directory
- `node_modules/` - Installed dependencies

### 2. Framework Dependency

**Rule:** Project must use either `@apps-in-toss/framework` or `@apps-in-toss/web-framework`

**Check:** The framework must be present in either `dependencies` or `devDependencies` in `package.json`

**Rationale:** All apps-in-toss projects require the framework to function properly.

### 3. granite.config.ts Configuration

**Required structure:**
```typescript
import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'your-app-name',
  web: {
    port: 3000,
    commands: {
      dev: 'npm run dev',
      build: 'npm run build',
    },
  },
});
```

**Required fields:**
- `appName` - Application identifier
- `web.port` - Development server port
- `web.commands.dev` - Development command
- `web.commands.build` - Build command

**Required imports:**
- Must import from `@apps-in-toss/web-framework` or `@apps-in-toss/framework`

**Required exports:**
- Must have `export default defineConfig(...)`

## Warnings

These are not critical errors but should be addressed:

### package.json Warnings

- Missing `name` field
- Missing `version` field
- Missing `dev` or `start` script (if not defined in granite.config.ts)
- Missing `build` script (if not defined in granite.config.ts)

### Project Structure Warnings

- Missing `src/` directory
- Missing `tsconfig.json` for TypeScript projects
- Missing `node_modules/` (run `npm install`)

## Code Style and Linting

While not enforced by the validator, apps-in-toss projects should follow these guidelines:

### TypeScript Usage

- Use TypeScript for all source code
- Maintain strict type checking
- Use proper type imports

### Import Statements

- Use ES modules (`import`/`export`)
- Prefer named imports for clarity
- Keep imports organized

### Configuration

- Keep configuration in `granite.config.ts`
- Use `defineConfig` helper for type safety
- Provide sensible defaults

## Best Practices

### Development Workflow

1. Use `npm run dev` for development
2. Use `npm run build` for production builds
3. Test builds before deployment

### Configuration Management

- Use environment variables for sensitive data
- Don't commit `.env` files
- Document required environment variables

### Dependencies

- Keep dependencies up to date
- Use exact versions for framework packages
- Regularly audit for security issues

## Running Validations

### Validate entire project
```bash
npx tsx scripts/validate-all.ts /path/to/project
```

### Validate specific components

**granite.config.ts:**
```bash
npx tsx scripts/validate-granite-config.ts granite.config.ts
```

**package.json:**
```bash
npx tsx scripts/validate-package-json.ts package.json
```

**Project structure:**
```bash
npx tsx scripts/validate-project-structure.ts /path/to/project
```
