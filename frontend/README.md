# CSV Data Ingestion Frontend

A modern Vue 3 + Vite web application for uploading, analyzing, and visualizing CSV data with an interactive dashboard.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Development](#development)
- [Building](#building)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Features](#features)
- [Configuration](#configuration)
- [Assumptions](#assumptions)

## Prerequisites

- **Bun 1.0+** (recommended package manager)
  - [Bun Installation](https://bun.sh)
- **Backend API** running at `http://localhost:8000` (for development)

## Setup

### 1. Install Dependencies

Using Bun (recommended):

```bash
bun install
```

### 2. Configure API Connection

The application connects to the backend API. By default, it expects:

- **Development**: `http://localhost:8000`
- **Production**: `/api` (proxied by web server)

To change the API endpoint, update the configuration in `src/config/api.ts` or set environment variables.

## Development

### Start Dev Server

```bash
bun run dev
```

The application will open at `http://localhost:5173` with hot module replacement (HMR) enabled.

### Development Features

- **Fast Refresh**: Changes apply instantly without page reload
- **Type Checking**: Vue TypeScript support with automatic checks
- **Auto Imports**: Components and utilities are imported automatically
- **Dev Tools**: Vue DevTools extension support for debugging

## Building

### Development Build

```bash
bun run build-only
```

Outputs to `dist/` directory.

### Production Build

Includes type checking and optimization:

```bash
bun run build
```

### Type Checking

Check TypeScript types without building:

```bash
bun run type-check
```

### Preview Built App

```bash
bun run preview
```

Serves the production build locally at `http://localhost:4173`.

## Testing

### Run Tests

```bash
bun test
```

### Run Tests in Watch Mode

```bash
bun test -- --watch
```

### Run Tests with UI

```bash
bun test -- --ui
```

### Run Specific Test File

```bash
bun test test/unit/components.test.ts
```

### Test Coverage

```bash
bun test -- --coverage
```

### Test Structure

Tests are organized by feature:

```
test/
├── unit/
│   ├── components.test.ts      # Component tests
│   ├── stores.test.ts          # State management tests
│   └── utils.test.ts           # Utility function tests
└── e2e/                         # End-to-end tests (if configured)
```

## Linting

### Run ESLint

```bash
bun run lint
```

### Fix Linting Issues

```bash
bun run lint:fix
```

## Project Structure

```
frontend/
├── src/
│   ├── pages/                  # File-based routing (auto-imported)
│   │   ├── index.vue          # Home page
│   │   ├── upload.vue         # CSV upload page
│   │   ├── datasets/
│   │   │   └── [id].vue       # Dataset detail page
│   │   └── ...
│   ├── components/             # Reusable Vue components
│   │   ├── DataTable.vue      # Sortable, paginated data table
│   │   ├── ChartCard.vue      # Chart visualization wrapper
│   │   ├── UploadForm.vue     # CSV file upload form
│   │   └── ...
│   ├── stores/                 # Pinia state management
│   │   ├── auth.ts            # Authentication state
│   │   ├── datasets.ts        # Dataset management state
│   │   └── ui.ts              # UI state (theme, modals, etc)
│   ├── router/                 # Vue Router configuration
│   │   └── index.ts           # Router setup
│   ├── services/               # API service layer
│   │   ├── api.ts             # Base API client
│   │   ├── auth.ts            # Auth API calls
│   │   └── datasets.ts        # Dataset API calls
│   ├── composables/            # Reusable composition functions
│   │   ├── useAuth.ts         # Authentication composable
│   │   ├── useDatasets.ts     # Dataset operations composable
│   │   └── ...
│   ├── assets/                 # Static assets
│   │   ├── styles/            # Global CSS/UnoCSS
│   │   ├── images/
│   │   └── ...
│   ├── layouts/                # Layout components
│   │   ├── default.vue        # Main layout
│   │   └── ...
│   ├── App.vue                # Root component
│   └── main.ts                # Application entry point
├── public/                      # Static files served as-is
├── test/                        # Test files
├── dist/                        # Production build output
├── index.html                  # HTML entry point
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript configuration
├── eslint.config.ts            # ESLint configuration
├── uno.config.ts               # UnoCSS atomic CSS config
├── components.json             # UI component metadata
├── package.json                # Dependencies and scripts
└── README.md                   # This file
```

## Features

### Core Functionality

- **User Authentication**
  - Register new account
  - Login with email/password
  - Token refresh and persistent sessions
  - Logout

- **CSV Upload & Management**
  - Drag-and-drop CSV upload
  - Progress indication
  - File validation
  - List uploaded datasets
  - View dataset details

- **Data Visualization & Analytics**
  - Interactive data tables with sorting/filtering
  - Summary statistics (min, max, mean, median)
  - Chart visualizations (bar, line, pie charts)
  - Column analysis (numeric and categorical)
  - Responsive grid layout

- **User Interface**
  - Dark mode support
  - Responsive design (mobile, tablet, desktop)
  - Loading states and error messages
  - Toast notifications
  - Accessible components

### Technology Stack

- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite 7
- **Package Manager**: Bun
- **Language**: TypeScript 5.9
- **State Management**: Pinia with Colada for server state
- **Styling**: UnoCSS (atomic CSS)
- **UI Components**: Radix Vue, Reka UI
- **Tables**: TanStack Vue Table
- **Charts**: Unovis Vue
- **Testing**: Vitest
- **Linting**: ESLint with @antfu/eslint-config
- **HTTP Client**: ofetch (simple, modern fetch wrapper)

## Configuration

### API Endpoint

The frontend connects to the backend API. Configure the endpoint:

**Development** (`vite.config.ts`):

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

**Production** (`.nginx.conf`):
Nginx proxies `/api` requests to the backend container.

### Environment Variables

Create `.env.local` for development:

```
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=CSV Data Ingestion
```

### Styling

The application uses **UnoCSS** for utility-first CSS:

- Tailwind-like utility classes
- CSS preset from `uno.config.ts`
- Dark mode support via `presetDarkModeStrategySelector`

Apply dark mode:

```html
<div class="dark:bg-slate-900 bg-white">Content</div>
```

### Icons

Icons are loaded from Iconify using the `@iconify-json/lucide` preset:

```vue
<i class="i-lucide-plus" />
```

Browse available icons: [Icônes](https://icones.netlify.app/)

## Docker Deployment

### Build Image

```bash
docker build -t csv-frontend .
```

### Run Container

```bash
docker run -p 8080:80 csv-frontend
```

The Dockerfile builds the Vue app and serves it with Nginx.

## Development Tips

### Component Development

1. Create component in `src/components/`
2. Components are auto-imported (no need to import)
3. Use `<script setup>` syntax for simplicity

```vue
<script setup lang="ts">
const title = ref('Hello')
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">
      {{ title }}
    </h1>
  </div>
</template>
```

### State Management

Use Pinia stores for application state:

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const increment = () => count.value++

  return { count, increment }
})
```

Use in components:

```vue
<script setup>
const counter = useCounterStore()
</script>

<template>
  <p>Count: {{ counter.count }}</p>
  <button @click="counter.increment">
    Increment
  </button>
</template>
```

### API Calls

Use the service layer for API communication:

```typescript
// services/datasets.ts
import { $fetch } from 'ofetch'

export async function uploadDataset(file: File) {
  const formData = new FormData()
  formData.append('file', file)

  return $fetch('/api/datasets/upload', {
    method: 'POST',
    body: formData,
  })
}
```

### Composables

Create reusable logic with composables:

```typescript
// composables/useDataset.ts
export function useDataset(datasetId: string) {
  const dataset = ref(null)
  const loading = ref(false)

  const fetch = async () => {
    loading.value = true
    dataset.value = await $fetch(`/api/datasets/${datasetId}`)
    loading.value = false
  }

  onMounted(fetch)

  return { dataset, loading, fetch }
}
```

## Troubleshooting

### Port Already in Use

```bash
# Linux/Mac: Find process on port 5173
lsof -i :5173

# Kill process
kill -9 <PID>
```

### API Connection Errors

1. Ensure backend is running: `http://localhost:8000/api/health`
2. Check CORS configuration in backend
3. Verify API URL in frontend config

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules dist .vite
bun install
bun run build
```

### Hot Module Replacement Not Working

1. Check Vite config has correct server setup
2. Try restarting dev server
3. Clear browser cache (Ctrl+Shift+Delete)

### Type Errors

Run type check:

```bash
bun run type-check
```

Fix TypeScript errors:

```bash
bun run type-check -- --noEmit
```

## Performance Optimization

### Production Build Analysis

Analyze bundle size:

```bash
bun run build -- --analyze
```

### Lazy Loading Routes

Routes are lazy-loaded by default via `vite-plugin-vue-layouts`.

### Component Code Splitting

Large components are automatically code-split by Vite.

### Image Optimization

Use modern formats:

```vue
<picture>
  <source srcset="image.webp" type="image/webp">
  <img src="image.png" alt="Description">
</picture>
```

## Assumptions

1. **Backend API**: The application expects the backend API to be available at:
   - Development: `http://localhost:8000`
   - Production: `/api` (proxied by web server)

2. **Authentication**:
   - Uses JWT tokens in HTTP-only cookies
   - Token refresh is automatic via interceptor
   - All protected endpoints require valid token

3. **CSV Data**:
   - Assumes well-formed CSV files with headers
   - Column names are used as-is in UI
   - Data is displayed as strings (type detection happens on backend)

4. **Browser Support**:
   - Modern browsers (Chrome, Firefox, Safari, Edge)
   - ES2020+ JavaScript support required
   - Local storage for session persistence

5. **Screen Sizes**:
   - Responsive design supports: 320px (mobile) to 2560px (4K)
   - Mobile-first approach with breakpoints at 640px, 1024px, 1280px
   - Touch-friendly component sizes for mobile

6. **Performance**:
   - Assumes reasonable network latency (100-500ms)
   - Large datasets (>10,000 rows) may cause UI slowness
   - Tables are paginated to 100 rows per page by default

7. **User Permissions**:
   - Users can only see/edit their own datasets
   - Authentication tokens are user-specific
   - No role-based access control (all authenticated users are equal)

8. **Dark Mode**:
   - Persisted in local storage
   - Respects system preference on first visit
   - Can be toggled via UI

9. **Session Management**:
   - Sessions persist across browser refresh
   - Closing browser doesn't log out (token cleanup on logout)
   - Tokens auto-refresh 5 minutes before expiration

10. **Network Conditions**:
    - Assumes relatively stable internet connection
    - No offline mode support
    - Slow uploads show progress indication

## Deployment Checklist

- [ ] Set correct API URL in production config
- [ ] Update `vite.config.ts` proxy settings for production
- [ ] Configure Nginx for serving static assets
- [ ] Set secure CORS headers
- [ ] Enable gzip compression
- [ ] Set cache headers appropriately
- [ ] Test dark mode functionality
- [ ] Verify mobile responsiveness
- [ ] Test authentication flow
- [ ] Monitor bundle size

## Browser DevTools

### Vue DevTools

Install [Vue DevTools Extension](https://devtools.vuejs.org/) for debugging:

- Component inspection
- Props/state monitoring
- Event tracking
- Timeline profiling

### Vite Plugin Vue DevTools

Built-in debugging available at `/__nuxt_devtools/` in development.

## Contributing

When adding features:

1. Follow the existing file structure
2. Use TypeScript for all new code
3. Add tests for new functionality
4. Update component documentation
5. Test responsiveness on mobile

## References

- [Vue 3 Docs](https://vuejs.org/)
- [Vite Docs](https://vitejs.dev/)
- [Pinia Docs](https://pinia.vuejs.org/)
- [UnoCSS Docs](https://unocss.dev/)
- [Vitest Docs](https://vitest.dev/)
