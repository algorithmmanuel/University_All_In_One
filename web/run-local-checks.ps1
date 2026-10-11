param([switch]$Build)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
& (Join-Path $root "scripts\sync-before-test.ps1")
Push-Location $PSScriptRoot
try {
    npm run typecheck
    if ($LASTEXITCODE -ne 0) { throw "Frontend typecheck failed." }
    npm test
    if ($LASTEXITCODE -ne 0) { throw "Frontend unit tests failed." }
    if ($Build) {
        Write-Host "Ensure npm run dev is stopped before production build."
        npm run build
        if ($LASTEXITCODE -ne 0) { throw "Frontend production build failed." }
    }
} finally { Pop-Location }
