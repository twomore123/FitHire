# FitHire Frontend

Next.js frontend application for FitHire - Fitness professional matching platform.

## Phase 1 MVP Status (Complete - UI Structure)

✅ **Completed:**
- Landing page with feature highlights
- Clerk authentication integration (sign-in/sign-up)
- Dashboard navigation structure
- Coach profile page (read-only display)
- Coach matches page (empty state with explanations)
- Manager jobs page (empty state)
- Manager job posting page (form UI structure)
- Complete API client for all backend endpoints
- shadcn/ui component library setup
- Responsive layouts with Tailwind CSS v4

⏳ **Next Phase (Backend Integration):**
- Connect forms to backend API with validation
- Real data fetching and display
- FitScore visualization components
- Profile photo and video uploads (Cloudflare R2)
- Admin verification panel
- Interactive filtering and sorting

## Tech Stack

- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 4 (CSS-based configuration)
- **UI Components:** shadcn/ui
- **Authentication:** Clerk (JWT with organizations)
- **State Management:** Zustand (planned for Phase 2)
- **Forms:** React Hook Form + Zod (planned for Phase 2)
- **API Client:** Native fetch with TypeScript

## Getting Started

### Prerequisites

- Node.js 20+ and npm
- Backend API running (see `/backend/README.md`)
- Clerk account with API keys ([Get started](https://clerk.com))

### Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Set up environment variables:**
```bash
cp .env.example .env.local
```

Edit `.env.local` with your values:
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Clerk Authentication (REQUIRED)
# Get from: https://dashboard.clerk.com/last-active?path=api-keys
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_actual_key_here

# Redirects
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

**CRITICAL:** You must set a valid Clerk publishable key from your dashboard. The app will not build without it.

3. **Run development server:**
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

### Available Scripts

```bash
npm run dev         # Start dev server (port 3000)
npm run build       # Production build (requires valid Clerk key)
npm run start       # Start production server
npm run lint        # Run ESLint
npm run type-check  # TypeScript type checking
```

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── dashboard/           # Protected routes
│   │   ├── coach/          # Coach profile & matches
│   │   │   ├── page.tsx
│   │   │   └── matches/
│   │   ├── manager/        # Job management
│   │   │   ├── page.tsx
│   │   │   └── new/
│   │   ├── layout.tsx      # Dashboard layout with nav
│   │   └── page.tsx        # Dashboard home
│   ├── globals.css         # Tailwind v4 config + CSS vars
│   ├── layout.tsx          # Root layout with ClerkProvider
│   └── page.tsx            # Public landing page
│
├── components/ui/          # shadcn/ui components
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   └── label.tsx
│
├── lib/
│   ├── api-client.ts      # Backend API methods
│   └── utils.ts           # Utilities (cn helper)
│
├── middleware.ts          # Clerk route protection
├── components.json        # shadcn/ui config
└── .env.local            # Environment vars (DON'T COMMIT)
```

## Pages Overview

### Public

**`/`** - Landing Page
- Hero with CTAs
- Feature cards
- Sign-in/sign-up links

### Protected (Auth Required)

**`/dashboard`** - Dashboard Home
- Welcome message with user name
- Quick nav cards (Coach/Manager sections)
- Stats overview (placeholders)

**`/dashboard/coach`** - Coach Profile
- Profile information display
- Completeness indicator
- Certifications & availability sections
- Next steps checklist

**`/dashboard/coach/matches`** - Job Matches
- Top job matches list (empty state for MVP)
- FitScore factors explanation
- Match threshold info

**`/dashboard/manager`** - Manager Jobs
- Job listings (empty state)
- Post new job button
- Stats (active jobs, candidates, avg FitScore)

**`/dashboard/manager/new`** - New Job
- Job posting form (UI structure only)
- FitScore configuration preview
- All required fields shown

## Authentication with Clerk

### Setup

1. Create Clerk app at [dashboard.clerk.com](https://dashboard.clerk.com)
2. **Enable Organizations** (Settings → Organizations)
3. Copy Publishable Key (API Keys page)
4. Add to `.env.local`

### Usage in Components

```typescript
import { useAuth, useUser } from "@clerk/nextjs";

function MyComponent() {
  const { getToken } = useAuth();
  const { user } = useUser();

  async function fetchData() {
    const token = await getToken();
    const data = await coachAPI.list({}, token);
  }
}
```

### Server Components

```typescript
import { currentUser } from "@clerk/nextjs/server";

export default async function Page() {
  const user = await currentUser();
  // user.firstName, user.emailAddresses, etc.
}
```

## Styling (Tailwind CSS v4)

This project uses **Tailwind v4** with CSS-based configuration.

### Key Differences from v3

- No `tailwind.config.js` file
- Configuration in CSS via `@theme`
- Import: `@import "tailwindcss"` (not `@tailwind`)
- CSS variables for theming

### Customization

Edit `app/globals.css`:

```css
@theme inline {
  --color-primary: hsl(240 5.9% 10%);
  --color-secondary: hsl(240 4.8% 95.9%);
  /* Custom colors */
}
```

### Usage

```tsx
<div className="bg-primary text-primary-foreground">
  Styled with theme colors
</div>
```

## UI Components (shadcn/ui)

Components are installed locally in `components/ui/` for customization.

### Installed Components

- Button (with variants: default, outline, ghost, destructive)
- Card (Header, Title, Description, Content, Footer)
- Input
- Label

### Adding More Components

If `npx shadcn add` fails (registry issues), manually copy from [ui.shadcn.com](https://ui.shadcn.com):

1. Visit component docs
2. Copy code
3. Create file in `components/ui/[name].tsx`
4. Adjust imports

Example:
```bash
# If this works:
npx shadcn@latest add select

# Otherwise, manually copy from docs
```

## API Client

Complete typed client for all backend endpoints in `lib/api-client.ts`.

### Coach API

```typescript
import { coachAPI } from "@/lib/api-client";
import { useAuth } from "@clerk/nextjs";

const { getToken } = useAuth();
const token = await getToken();

// Create coach
const coach = await coachAPI.create({
  location_id: 1,
  first_name: "John",
  last_name: "Doe",
  email: "john@example.com",
  city: "Los Angeles",
  state: "CA",
  role_type: "Personal Trainer",
  certifications: [],
  years_experience: 5,
}, token);

// Get matches
const matches = await coachAPI.getMatches(coachId, 20, token);
```

### Job API

```typescript
import { jobAPI } from "@/lib/api-client";

// Create job
const job = await jobAPI.create({
  location_id: 1,
  title: "Group Fitness Instructor",
  description: "...",
  role_type: "Group Fitness Instructor",
  city: "Los Angeles",
  state: "CA",
  required_certifications: ["ACE", "NASM-CPT"],
  min_experience: 2,
  weighting_preset: "balanced",
  fitscore_threshold: 0.60,
}, token);

// Get candidates
const candidates = await jobAPI.getCandidates(jobId, 20, token);
```

### Error Handling

```typescript
import { APIError } from "@/lib/api-client";

try {
  const data = await coachAPI.get(123, token);
} catch (error) {
  if (error instanceof APIError) {
    console.error(`${error.status}: ${error.message}`);
    console.error("Details:", error.details);
  }
}
```

## Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import in Vercel
3. Set env vars:
   ```
   NEXT_PUBLIC_API_URL=https://backend.railway.app
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_xxx
   NEXT_PUBLIC_SITE_URL=https://fithire.vercel.app
   ```
4. Deploy

### Production Environment

```env
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_SITE_URL=https://your-domain.com
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_production_key

# Redirects (same as dev)
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

## Development Workflow

### Before Committing

```bash
npm run lint        # ESLint check
npm run type-check  # TypeScript errors
```

`npm run build` requires valid Clerk key. If you don't have one, skip build and just run lint/type-check.

### Git Workflow

1. Create feature branch: `git checkout -b feature/name`
2. Make changes, test with `npm run dev`
3. Run lint and type-check
4. Commit with clear message
5. Push and create PR

## Troubleshooting

### "Missing publishableKey" Error

**Cause:** No Clerk key in `.env.local`

**Fix:** Get key from [Clerk Dashboard](https://dashboard.clerk.com/last-active?path=api-keys) and add to `.env.local`:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
```

### "Invalid publishableKey" Error

**Cause:** Placeholder key won't work

**Fix:** Use real key from your Clerk account (not the example placeholder)

### CORS Errors with API

**Cause:** Backend doesn't allow your frontend origin

**Fix:** Update backend CORS in `backend/app/main.py`:
```python
allow_origins=["http://localhost:3000", "https://your-vercel.vercel.app"]
```

### Tailwind Classes Not Working

**Cause:** Using Tailwind v3 syntax

**Fix:** This project uses v4 (CSS-based config). No `tailwind.config.js` should exist.

## What's Next (Phase 2)

- **Forms:** Connect UI to backend with React Hook Form + Zod
- **Data Fetching:** Real API calls with loading states
- **FitScore UI:** Visual score breakdowns and explanations
- **File Uploads:** Profile photos and videos via Cloudflare R2
- **Admin Panel:** Coach verification workflow
- **Filtering:** Advanced search and filtering
- **Optimistic UI:** Instant feedback on mutations

## Contributing

See [CLAUDE.md](../CLAUDE.md) for project guidelines and coding standards.

---

**MVP Note:** Phase 1 focuses on UI/UX structure. Forms are placeholders. Backend integration and full functionality coming in next phase.
