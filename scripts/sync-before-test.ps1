param(
    [switch]$CheckOnly
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    git rev-parse --is-inside-work-tree | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Not a Git working tree." }
    $branch = (git branch --show-current).Trim()
    if ($branch -ne "feature/phase-9-platform-expansion") {
        throw "Expected feature/phase-9-platform-expansion; current branch: $branch. Switch branches deliberately."
    }
    git fetch --prune origin
    if ($LASTEXITCODE -ne 0) { throw "Git fetch failed. No files changed." }
    $upstream = "origin/$branch"
    git rev-parse --verify $upstream | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Upstream branch not found: $upstream" }
    $local = (git rev-parse HEAD).Trim()
    $remote = (git rev-parse $upstream).Trim()
    $base = (git merge-base HEAD $upstream).Trim()
    $dirty = @(git status --porcelain --untracked-files=normal)
    $generatedOnly = $true
    foreach ($entry in $dirty) {
        $path = $entry.Substring(3).Trim().Replace("\\", "/")
        if ($path -notin @("web/next-env.d.ts", "web/tsconfig.tsbuildinfo")) {
            $generatedOnly = $false
            break
        }
    }
    if ($base -ne $local -and $base -ne $remote) {
        throw "Local and GitHub histories diverged. Resolve explicitly; no automatic overwrite."
    }
    if ($base -eq $remote -and $local -ne $remote) {
        throw "Local commits have not been pushed to GitHub. Push/review before testing; no automatic push."
    }
    if ($dirty.Count -gt 0) {
        Write-Host "Local modifications exist:" -ForegroundColor Yellow
        git status --short
        if ($local -ne $remote) {
            if (-not $generatedOnly) {
                throw "GitHub is ahead and source changes exist. Commit or stash deliberately before syncing."
            }
            # Generated-only changes are safe to retain when upstream does not touch
            # those paths. Git fast-forward preserves the working tree in this case.
            $upstreamGeneratedChanges = @(git diff --name-only HEAD $upstream -- web/next-env.d.ts web/tsconfig.tsbuildinfo)
            if ($LASTEXITCODE -ne 0 -or $upstreamGeneratedChanges.Count -gt 0) {
                throw "GitHub also changes a generated file. Preserve it manually before syncing."
            }
            Write-Host "Only known Next.js generated files changed; keeping them in place." -ForegroundColor Yellow
        }
    }
    if ($local -ne $remote) {
        if ($CheckOnly) { throw "GitHub is ahead. Run .\scripts\sync-before-test.ps1 to update safely." }
        git merge --ff-only $upstream
        if ($LASTEXITCODE -ne 0) { throw "Fast-forward failed. No forced reset attempted." }
    }
    $now = (git rev-parse HEAD).Trim()
    if ($now -ne $remote) { throw "Revision mismatch after sync." }
    Write-Host "SYNC VERIFIED: $branch at $($now.Substring(0, 12))" -ForegroundColor Green
    if ($dirty.Count -gt 0) {
        Write-Host "WARNING: local uncommitted changes remain. Test results may differ from GitHub CI." -ForegroundColor Yellow
    }
} finally { Pop-Location }
