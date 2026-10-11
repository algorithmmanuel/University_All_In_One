# Phase 8.2 — Frontend maintainability

## First incremental extraction
- `web/lib/pathways.ts`: typed academy model, offline fallback content, and runtime response validation.
- `web/lib/api.ts`: centralized public pathway API request with AbortSignal.
- `web/lib/preview-quiz.ts`: local preview-only quiz content.
- `web/app/page.tsx`: retains existing rendered UI and state while delegating API/data concerns.

## Engineering intent
Preserve the existing page, route, text, navigation, mission preview and offline fallback. This is a small extraction, not a redesign. The client validates the server response before rendering and never sends preview quiz answers to the API.

## Local verification (Windows PowerShell)
```powershell
git pull --ff-only origin feature/phase-8-engineering-hardening
Set-Location web
npm install
npx tsc --noEmit
npm run build
Set-Location ..
```

If `npm install` changes `web/package-lock.json`, retain it for review; do not discard existing local edits. Commit a reviewed lockfile before switching CI to `npm ci`.

## Remaining work
- Verify TypeScript and Next.js production build on the developer's machine.
- Add committed dependency lockfile and a frontend CI quality gate.
- Extract presentation components in small batches with browser regressions.
- Review mobile responsiveness, accessibility and authenticated API flows.

## Batch 2 — Reusable components and CI
- `web/components/home/academy-sections.tsx` owns academy cards and selected pathway preview; the parent keeps selection state.
- `web/components/home/preview-quiz.tsx` owns its own ephemeral quiz state and preserves the existing answers and scoring.
- `web/app/page.tsx` composes these components and retains API availability state and navigation.
- `.github/workflows/frontend-quality.yml` checks TypeScript and production builds on pushes and pull requests affecting frontend files.

The CI workflow temporarily uses `npm install` because no reviewed `web/package-lock.json` exists in GitHub. This is not a reproducible dependency install. Preserve and review the local lockfile, commit it, then replace CI installation with `npm ci`.

Browser verification remains necessary for pathway selection, quiz feedback, keyboard navigation and offline fallback; a successful build does not prove interaction behavior.

## Batch 3 — Frontend regression gate
- `web/tests/pathways.test.cjs` checks pathway validation, rejection of malformed server responses and stable display order. Tests use Node's built-in test runner and the existing TypeScript dependency; no additional testing package is required.
- `npm run typecheck`, `npm test`, and `npm run build` are enforced in the frontend GitHub workflow.
- Dependency locking remains **pending** because `web/package-lock.json` exists only on the developer machine. Do not synthesize or overwrite it remotely. Review and commit the actual local lockfile, then switch CI to `npm ci`.

### Lockfile handoff (Windows PowerShell, project root)
```powershell
Set-Location web
npm install --package-lock-only
npm run typecheck
npm test
npm run build
Set-Location ..
git status --short
git add web/package-lock.json
git commit -m "build(web): commit reviewed npm dependency lockfile"
git push origin feature/phase-8-engineering-hardening
```
Inspect `git status --short` before staging; the commands intentionally stage only the lockfile. Do not overwrite unrelated local changes. After pushing, update CI installation to `npm ci` and verify the workflow.

## Lockfile closure
Developer committed and pushed `web/package-lock.json` at `a8bddf2`. Frontend CI now uses `npm ci --no-audit --no-fund` and an npm cache keyed to that lockfile (workflow commit `be73160`). This improves reproducibility; dependency vulnerability assessment remains a separate check. Confirm the first lockfile-backed CI run before marking this gate verified.
