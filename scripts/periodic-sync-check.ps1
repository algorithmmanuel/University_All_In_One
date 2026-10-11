$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $root ".git\educyber-sync"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "latest.txt"
Push-Location $root
try {
    $branch = (git branch --show-current).Trim()
    if ($branch -ne "feature/phase-9-platform-expansion") {
        "[$(Get-Date -Format o)] Skipped: working branch $branch" | Set-Content $log
        exit 0
    }
    git fetch origin $branch --quiet
    if ($LASTEXITCODE -ne 0) { throw "Fetch failed" }
    $local = (git rev-parse HEAD).Trim()
    $remote = (git rev-parse "origin/$branch").Trim()
    $status = if ($local -eq $remote) { "in sync" } else { "different revisions; run sync-before-test.ps1 before testing" }
    "[$(Get-Date -Format o)] $status; local=$local remote=$remote" | Set-Content $log
} catch {
    "[$(Get-Date -Format o)] ERROR: $($_.Exception.Message)" | Set-Content $log
    throw
} finally { Pop-Location }
