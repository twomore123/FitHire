# FitHire Deployment Guide

This guide walks through deploying FitHire to production (Railway + Vercel).

---

## Prerequisites

1. **Accounts Created:**
   - [Railway](https://railway.app) - Backend hosting
   - [Vercel](https://vercel.com) - Frontend hosting
   - [Clerk](https://clerk.dev) - Authentication (already set up)
   - [Neon](https://neon.tech) - PostgreSQL database (already set up)
   - [Cloudflare R2](https://cloudflare.com/products/r2/) - File storage (already set up)

2. **Local Setup Complete:**
   - Backend API tested locally
   - Frontend tested locally
   - Database migrations run
   - All environment variables documented

---

## Step 1: Deploy Backend to Railway

### 1.1 Create Railway Project

1. Go to [railway.app/new](https://railway.app/new)
2. Click "Deploy from GitHub repo"
3. Connect your GitHub account if not already connected
4. Select the `twomore123/FitHire` repository
5. Choose the `claude/debug-localhost-frontend-q7gGa` branch (or `main` after merging)

### 1.2 Configure Service

1. Set **Root Directory:** `backend`
2. Railway will auto-detect Python and use Nixpacks
3. The `Procfile` and `railway.json` configure the startup command

### 1.3 Set Environment Variables

Go to Variables tab and add:

```bash
# App Settings
ENVIRONMENT=production
API_HOST=0.0.0.0
API_RELOAD=false
SECRET_KEY=<generate-with-openssl-rand-hex-32>

# CORS (add your Vercel domain after deployment)
CORS_ORIGINS=https://fithire.vercel.app,https://www.fithire.com

# Database (Neon)
DATABASE_URL=<your-neon-connection-string>
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30

# Clerk Authentication
CLERK_SECRET_KEY=<your-clerk-secret-key>
CLERK_PUBLISHABLE_KEY=<your-clerk-publishable-key>
CLERK_WEBHOOK_SECRET=<your-clerk-webhook-secret>

# Cloudflare R2
R2_ACCOUNT_ID=<your-cloudflare-account-id>
R2_BUCKET_NAME=fithire
R2_ACCESS_KEY_ID=<your-r2-access-key>
R2_SECRET_ACCESS_KEY=<your-r2-secret-key>
R2_ENDPOINT=<your-r2-endpoint>
R2_PUBLIC_URL=<your-r2-public-url>

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 1.4 Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Railway will provide a URL: `https://fithire-production.up.railway.app`
4. Test the API: `https://your-url.railway.app/api/v1/health`

### 1.5 Run Database Migrations

Use Railway's CLI or add a migration service:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Run migrations
railway run alembic upgrade head
```

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Project

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import the `twomore123/FitHire` repository
3. Select the `claude/debug-localhost-frontend-q7gGa` branch (or `main` after merging)

### 2.2 Configure Project

1. **Framework Preset:** Next.js
2. **Root Directory:** `frontend`
3. **Build Command:** `npm run build` (default)
4. **Output Directory:** `.next` (default)
5. **Install Command:** `npm install` (default)

### 2.3 Set Environment Variables

Go to Settings → Environment Variables and add:

```bash
# Next.js Settings
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_API_URL=https://fithire-production.up.railway.app/api/v1
NEXT_PUBLIC_SITE_URL=https://fithire.vercel.app

# Clerk (Frontend)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=<your-clerk-publishable-key>
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard/coach/edit

# Feature Flags
NEXT_PUBLIC_FEATURE_VIDEO_UPLOAD=true
NEXT_PUBLIC_FEATURE_ADMIN_PANEL=true
NEXT_PUBLIC_FEATURE_ANALYTICS=false
```

### 2.4 Deploy

1. Click "Deploy"
2. Wait for build (~2-3 minutes)
3. Vercel will provide a URL: `https://fithire.vercel.app`
4. Test the frontend by visiting the URL

### 2.5 Update CORS in Backend

Go back to Railway and update `CORS_ORIGINS`:

```bash
CORS_ORIGINS=https://fithire.vercel.app,https://fithire-git-main-twomore123.vercel.app
```

Redeploy the backend for changes to take effect.

---

## Step 3: Configure Custom Domain (Optional)

### 3.1 Frontend Domain

1. In Vercel, go to Settings → Domains
2. Add your custom domain (e.g., `fithire.com`)
3. Follow Vercel's DNS configuration instructions
4. Update environment variables with new domain

### 3.2 Backend Domain

1. In Railway, go to Settings → Domains
2. Click "Generate Domain" or add custom domain
3. Update frontend `NEXT_PUBLIC_API_URL` to use new domain
4. Redeploy frontend

---

## Step 4: Post-Deployment Checklist

### ✅ Backend

- [ ] API is accessible at `/api/v1/health`
- [ ] Database migrations completed
- [ ] Clerk JWT validation works
- [ ] CORS allows frontend domain
- [ ] Environment variables set correctly
- [ ] Logs show no errors

### ✅ Frontend

- [ ] Homepage loads correctly
- [ ] Sign-in/sign-up works
- [ ] Dashboard requires authentication
- [ ] API calls succeed (check Network tab)
- [ ] No console errors
- [ ] Forms submit successfully

### ✅ Integration

- [ ] Sign up → create coach profile → see matches flow works
- [ ] Sign up → create job → see candidates flow works
- [ ] FitScore calculations display correctly
- [ ] All pages load without errors
- [ ] Mobile responsiveness verified

---

## Step 5: Smoke Tests

Run these tests manually after deployment:

### Test 1: Coach Flow

1. Go to production frontend URL
2. Click "Sign Up"
3. Create an account with email
4. Go to Dashboard → My Profile
5. Click "Edit Profile"
6. Fill out complete profile with:
   - Name, email, location
   - Role type (e.g., "Group Fitness Instructor")
   - Certifications (select 2-3)
   - Years of experience
   - Availability (select 3-4 time slots)
   - Cultural fit tags
   - Bio
7. Submit form
8. Go to "My Matches"
9. Verify empty state or matches display

### Test 2: Manager Flow

1. Sign in (or create new account)
2. Go to Dashboard → Jobs
3. Click "Post New Job"
4. Fill out job form with:
   - Title, description, location
   - Role type
   - Required/preferred certifications
   - Experience requirements
   - Availability needs
   - FitScore settings
5. Submit form
6. View job in list
7. Click "View Candidates"
8. Verify candidates list (empty state or actual candidates)

### Test 3: End-to-End Match

1. Create coach profile (Test 1)
2. Create job posting (Test 2)
3. Ensure coach matches job requirements
4. Refresh manager's candidates list
5. Verify coach appears with FitScore
6. Check FitScore breakdown shows all 6 components

---

## Monitoring & Logs

### Railway (Backend)

- View logs: Railway dashboard → Deployments → View Logs
- Monitor: Railway dashboard → Observability
- Restart: Railway dashboard → Settings → Restart

### Vercel (Frontend)

- View logs: Vercel dashboard → Deployments → [deployment] → View Function Logs
- Monitor: Vercel dashboard → Analytics
- Redeploy: Vercel dashboard → Deployments → [deployment] → Redeploy

---

## Troubleshooting

### Backend Issues

**Database connection fails:**
- Verify `DATABASE_URL` is correct
- Check Neon database is active
- Ensure IP allowlist includes Railway IPs

**Authentication fails:**
- Verify Clerk secret key is set
- Check JWKS URL is accessible
- Ensure token validation logic works

**CORS errors:**
- Update `CORS_ORIGINS` to include exact frontend URL
- Check for trailing slashes
- Redeploy backend after changes

### Frontend Issues

**API calls fail:**
- Verify `NEXT_PUBLIC_API_URL` points to Railway
- Check Network tab for exact error
- Ensure CORS is configured correctly
- Verify backend is deployed and healthy

**Authentication issues:**
- Check Clerk publishable key is set
- Verify redirect URLs in Clerk dashboard
- Ensure sign-in/sign-up routes exist

**Build failures:**
- Check build logs for specific errors
- Verify all dependencies are in package.json
- Ensure TypeScript types are correct
- Try building locally first

---

## Rollback Procedure

### Railway

1. Go to Deployments
2. Find last working deployment
3. Click "Redeploy"

### Vercel

1. Go to Deployments
2. Find last working deployment
3. Click "..." → "Promote to Production"

---

## Success Criteria

Phase 1 is complete when:

- ✅ Backend deployed and accessible
- ✅ Frontend deployed and accessible
- ✅ Coach can create profile
- ✅ Manager can create job
- ✅ FitScore calculates correctly (0.0-1.0)
- ✅ Top 20 matches display, sorted by score
- ✅ Threshold filtering works
- ✅ All authentication flows work
- ✅ No console errors
- ✅ Mobile responsive

---

**Deployment Complete!** 🎉

Your FitHire MVP is now live in production.

