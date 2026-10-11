param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  & .\scripts\sync-before-test.ps1
  if ($LASTEXITCODE -ne 0) { throw 'Sync failed' }
  $changes = @(git status --porcelain)
  $unsafe = @($changes | Where-Object { $_.Substring(3).Trim().Replace('\','/') -notin @('web/next-env.d.ts','web/tsconfig.tsbuildinfo') })
  if ($unsafe.Count) { throw 'Unexpected local changes; stop before migrating' }
  $id = (docker compose ps -q postgres).Trim()
  if ($LASTEXITCODE -ne 0 -or -not $id) { throw 'Development postgres is unavailable' }
  $details = @(docker inspect $id | ConvertFrom-Json)
  if ($details.Count -ne 1 -or $details[0].Config.Labels.'com.docker.compose.service' -ne 'postgres') { throw 'Unexpected container' }
  $database = (docker exec $id sh -c 'printf "%s" "$POSTGRES_DB"').Trim()
  $user = (docker exec $id sh -c 'printf "%s" "$POSTGRES_USER"').Trim()
  if ($database -ne 'educyber' -or $user -ne 'educyber') { throw 'Unexpected database' }
  $revision = (docker exec $id psql -X -At -U educyber -d educyber -c 'SELECT version_num FROM alembic_version').Trim()
  if ($LASTEXITCODE -ne 0 -or $revision -notin @('0007_age_safeguards','0008_private_beta')) { throw "Unexpected revision $revision" }
  Write-Host "Beta migration preflight: $revision"
  if (-not $Apply) { Write-Host 'PREFLIGHT PASSED; database unchanged'; return }
  $folder = Join-Path $root 'local-backups'
  New-Item -ItemType Directory -Force -Path $folder | Out-Null
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $remote = "/tmp/educyber-beta-$stamp.dump"
  $backup = Join-Path $folder "educyber-beta-$stamp.dump"
  docker exec $id pg_dump -U educyber -d educyber -Fc -f $remote
  if ($LASTEXITCODE -ne 0) { throw 'Backup failed' }
  docker exec $id pg_restore -l $remote | Out-Null
  if ($LASTEXITCODE -ne 0) { throw 'Backup archive invalid' }
  docker cp "${id}:${remote}" $backup
  if ($LASTEXITCODE -ne 0 -or (Get-Item $backup).Length -lt 1024) { throw 'Backup copy failed' }
  docker exec $id rm -f $remote | Out-Null
  Write-Host "BACKUP SAVED: $backup"
  if ($revision -eq '0007_age_safeguards') {
    $line = Get-Content .env | Where-Object { $_ -match '^\s*POSTGRES_PASSWORD\s*=' } | Select-Object -Last 1
    if (-not $line) { throw 'Password missing from .env' }
    $password = ($line -split '=',2)[1].Trim().Trim('"').Trim("'")
    $env:DATABASE_URL = 'postgresql+psycopg://educyber:' + [uri]::EscapeDataString($password) + '@127.0.0.1:5433/educyber?connect_timeout=5'
    Push-Location api
    try { & .\.venv\Scripts\python.exe -m alembic upgrade 0008_private_beta; if ($LASTEXITCODE -ne 0) { throw 'Migration failed' } }
    finally { Pop-Location; Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue }
  }
  $revision = (docker exec $id psql -X -At -U educyber -d educyber -c 'SELECT version_num FROM alembic_version').Trim()
  if ($revision -ne '0008_private_beta') { throw 'Unexpected final revision' }
  Write-Host "MIGRATION VERIFIED: $revision; backup: $backup"
} finally { Pop-Location }
