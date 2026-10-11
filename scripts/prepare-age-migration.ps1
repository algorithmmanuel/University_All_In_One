param(
    [switch]$Apply
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$api = Join-Path $root "api"
$python = Join-Path $api ".venv\Scripts\python.exe"
$branch = "feature/phase-9-platform-expansion"
$backup = $null
$container = $null
$remoteFile = $null

function Assert-LastExit([string]$message) {
    if ($LASTEXITCODE -ne 0) { throw $message }
}

Push-Location $root
try {
    if ((git branch --show-current).Trim() -ne $branch) {
        throw "Wrong Git branch; expected $branch"
    }
    & (Join-Path $root "scripts\sync-before-test.ps1")
    Assert-LastExit "Safe GitHub synchronization failed."
    $changes = @(git status --porcelain --untracked-files=normal)
    $allowedGenerated = @("web/next-env.d.ts", "web/tsconfig.tsbuildinfo")
    $unsafeChanges = @($changes | Where-Object {
        $path = $_.Substring(3).Trim().Replace("\\", "/")
        $path -notin $allowedGenerated
    })
    if ($unsafeChanges.Count -gt 0) {
        throw "Uncommitted source or unknown files remain. Preserve them before database migration."
    }
    if ($changes.Count -gt 0) {
        Write-Host "Only recognized Next.js generated files are modified; preserving them." -ForegroundColor Yellow
    }
    if (-not (Test-Path $python)) { throw "Missing API virtual environment." }
    $envFile = Join-Path $root ".env"
    if (-not (Test-Path $envFile)) { throw "Missing root .env." }
    $line = Get-Content $envFile | Where-Object { $_ -match '^\s*POSTGRES_PASSWORD\s*=' } | Select-Object -Last 1
    if (-not $line) { throw "POSTGRES_PASSWORD missing from root .env." }
    $password = ($line -split '=', 2)[1].Trim().Trim('"').Trim("'")
    if ([string]::IsNullOrWhiteSpace($password)) { throw "Empty database password." }
    $env:POSTGRES_PASSWORD = $password
    $container = (docker compose ps -q postgres).Trim()
    Assert-LastExit "Cannot inspect development PostgreSQL container."
    if (-not $container) { throw "Development PostgreSQL container is not running. No database changed." }
    $service = (docker inspect --format '{{index .Config.Labels "com.docker.compose.service"}}' $container).Trim()
    Assert-LastExit "Unable to inspect container identity."
    if ($service -ne "postgres") { throw "Refusing non-development database container." }
    $dbName = (docker exec $container sh -c 'printf "%s" "$POSTGRES_DB"').Trim()
    $dbUser = (docker exec $container sh -c 'printf "%s" "$POSTGRES_USER"').Trim()
    if ($dbName -ne "educyber" -or $dbUser -ne "educyber") {
        throw "Unexpected database identity. Refusing migration."
    }
    $revision = (docker exec $container psql -U educyber -d educyber -At -c 'SELECT version_num FROM alembic_version').Trim()
    Assert-LastExit "Unable to inspect Alembic version. No database changed."
    if ($revision -notin @("0006_login_limits", "0007_age_safeguards")) {
        throw "Unexpected schema revision $revision. Inspect migrations manually."
    }
    Write-Host "Development database revision: $revision"
    if (-not $Apply) {
        Write-Host "PREFLIGHT PASSED. No backup or migration performed. Rerun with -Apply to back up and migrate." -ForegroundColor Green
        return
    }
    $backupDir = Join-Path $root "local-backups"
    if (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = Join-Path $backupDir "educyber-pre-age-migration-$stamp.dump"
    if (Test-Path $backup) { throw "Backup filename already exists." }
    $remoteFile = "/tmp/educyber-pre-age-migration-$stamp.dump"
    docker exec $container pg_dump -U educyber -d educyber -Fc -f $remoteFile
    Assert-LastExit "Backup creation failed; migration not started."
    docker exec $container pg_restore -l $remoteFile | Out-Null
    Assert-LastExit "Backup archive failed integrity listing; migration not started."
    docker cp "${container}:${remoteFile}" $backup
    Assert-LastExit "Unable to copy backup out of container; migration not started."
    if ((Get-Item $backup).Length -lt 1024) { throw "Backup suspiciously small; migration not started." }
    Write-Host "BACKUP SAVED: $backup" -ForegroundColor Green

    if ($revision -eq "0006_login_limits") {
        $escaped = [uri]::EscapeDataString($password)
        $env:DATABASE_URL = "postgresql+psycopg://educyber:${escaped}@127.0.0.1:5433/educyber?connect_timeout=5"
        Push-Location $api
        try {
            & $python -m alembic upgrade 0007_age_safeguards
            Assert-LastExit "Migration failed. Backup preserved at $backup"
        } finally { Pop-Location }
    }
    $after = (docker exec $container psql -U educyber -d educyber -At -c 'SELECT version_num FROM alembic_version').Trim()
    Assert-LastExit "Post-migration verification failed; backup preserved."
    if ($after -ne "0007_age_safeguards") { throw "Unexpected post-migration revision: $after. Backup at $backup" }
    $columns = (docker exec $container psql -U educyber -d educyber -At -c "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name='users' AND column_name IN ('date_of_birth','age_band','guardian_consent_verified') ORDER BY column_name")
    Assert-LastExit "Cannot verify safeguarding columns."
    if (@($columns).Count -ne 3) { throw "Missing safeguarding columns. Backup at $backup" }
    Write-Host "MIGRATION VERIFIED: revision $after, three safeguarding columns. Backup: $backup" -ForegroundColor Green
} finally {
    if ($container -and $remoteFile) {
        docker exec $container rm -f $remoteFile 2>$null | Out-Null
    }
    Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:POSTGRES_PASSWORD -ErrorAction SilentlyContinue
    Pop-Location
}
