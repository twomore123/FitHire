# FitHire Frontend

Next.js frontend application for the FitHire platform.

## Tech Stack

- **Next.js** 16+ - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Accessible component library
- **Clerk** - Authentication
- **Zustand** - State management
- **React Hook Form** - Form handling
- **Zod** - Schema validation

## Project Structure

```
frontend/
├── app/                     # Next.js App Router
│   ├── (auth)/              # Auth layout group
│   │   ├── sign-in/
│   │   └── sign-up/
│   │
│   ├── (dashboard)/         # Protected routes
│   │   ├── layout.tsx       # Shared dashboard layout
│   │   ├── coach/
│   │   ├── manager/
│   │   └── admin/
│   │
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
│
├── components/              # React components
│   ├── ui/                  # shadcn/ui components
│   ├── features/            # Feature-specific components
│   └── shared/              # Shared components
│
├── lib/                     # Utilities
│   ├── api.ts               # API client
│   ├── auth.ts              # Clerk helpers
│   ├── utils.ts             # General utilities
│   └── types.ts             # TypeScript types
│
├── hooks/                   # Custom React hooks
├── store/                   # Zustand store
├── public/                  # Static assets
└── .env.example             # Environment variables template
```

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your actual credentials
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Development

### Available Scripts

- `npm run dev` - Start development server (http://localhost:3000)
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Lint code with ESLint
- `npm run type-check` - TypeScript type checking

### Adding shadcn/ui Components

To add a new shadcn/ui component:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add form
# etc.
```

Components will be added to `components/ui/`.

### Environment Variables

Create `.env.local` with the following variables (see `.env.example`):

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Clerk (Authentication)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/onboarding
```

### Code Style

- Use TypeScript strict mode
- Follow Next.js App Router conventions
- Use Tailwind CSS for styling (no custom CSS unless necessary)
- Use shadcn/ui components for UI elements
- Keep components small and focused
- Use `"use client"` directive only when needed (prefer Server Components)

### Pre-commit Checklist

Before committing:
1. ✅ Run `npm run lint` to check for linting errors
2. ✅ Run `npm run type-check` to ensure no TypeScript errors
3. ✅ Run `npm run build` to verify production build works

## Folder Conventions

### Components

- `components/ui/` - shadcn/ui components (auto-generated, customize as needed)
- `components/features/` - Feature-specific components (e.g., `features/coaches/ProfileForm.tsx`)
- `components/shared/` - Shared components used across features (e.g., `Header.tsx`, `Sidebar.tsx`)

### App Router

- `(auth)` - Route group for authentication pages (sign-in, sign-up)
- `(dashboard)` - Route group for protected dashboard pages
- Use `layout.tsx` for shared layouts
- Use `loading.tsx` for loading states
- Use `error.tsx` for error handling

## API Integration

The frontend communicates with the FastAPI backend via REST API.

Create an API client in `lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchMatches(coachId: number) {
  const response = await fetch(`${API_URL}/coaches/${coachId}/matches`, {
    headers: {
      'Authorization': `Bearer ${await getAuthToken()}`,
    },
  });
  return response.json();
}
```

## Authentication (Clerk)

Clerk provides authentication and user management.

Protected routes example:

```typescript
import { auth } from '@clerk/nextjs/server';

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect('/sign-in');
  }

  return <div>Dashboard</div>;
}
```

## Deployment

### Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Configure environment variables in Vercel dashboard
3. Deploy automatically on git push to main

### Manual Build

```bash
npm run build
npm run start
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Clerk Documentation](https://clerk.com/docs)
- [Zustand Documentation](https://zustand-demo.pmnd.rs)

## Architecture

See [../docs/architecture.md](../docs/architecture.md) for detailed system architecture.

## License

Proprietary - FitHire by Coach360
