# ClAUDE.md

## Architecture Overview

## Design Style Guide 

**Tech stack:** Next.js (App Router), Tailwind CSS, Shadcn UI

**Visual style**
- Clean, minimal interface
- Use Shadcn componenets for consistency
- Responsive design
- No dark mode for MVP

**Component patterns:**
- Shadcn UI for all interactive elements (buttons, inputs, cards)
- Tailwind for layout and spacing
- Keep components focused and small

## Product & UX Guidlines

**Core UX principles:**

**Copy tone:**
- Casual, friendly user-focused
- Brief labels and instructions
- Helpful error messages that suggest next steps

##Constratinst & Policies

**Security - MUST follow:**
- ALWAYS use environment variables for secrets
- NEVER commit '.env.local' or any file with API keys
- Validate and sanitize all user input

**Code quality:**
- TypeScript strict mode
- Run 'npm run lint' before committing
- No 'any' types without justification

**Dependencies:**
- Prefer Shadcn components over adding new UI libraries
- Minimize external dependencies for MVP

## Repository Etiquette

**Branching:**
- ALWAYS create a feature branch before starting major changes
- NEVER commit directly to 'main'
- Branch naming: 'feature/description' or 'fix/description'

**Git workflow for major changes:**
1. Create a new branch: 'git checkout -b feature/your-feature-name'
2. Develop and commit on the feature branch
3. Test locally before pushing:
   - 'npm run dev' - start dev server at localhost:3000
   - 'npm run lint' - check for linting errors
   - 'npm run build' - production build to catch type erros
4. Push the branch: 'git push -u orgin feature/your-feature-name'
5. Create a PR to merge into 'main'
6. Use the '/update-docs-and-commit' slash command for commits - this ensures docs are updated alongside code changes

**Commits:**
- Write clear commit messages describing the change
- Keep commits focused on single changes

**Pull Requests:**
- Create PRs for all changes to 'main'
- NEVER force push to 'main'
- Include description of what changed and why

**Before pushing:**
1. Run 'npm run lint'
2. Run 'npm run build' to catch type errors

## Documentation

- [Project Spec](PROJECT_SPEC.md) - Full requirements, API specs, tech details
- [Architecture](dosc/architecture.md) - System design and data flow
- [Changelog](docs/changelog.md) - Version history
- [Project Status](docs/project_status.md) - Current progress
- Update files in the docs folder after major milestones and major additions to the project.
