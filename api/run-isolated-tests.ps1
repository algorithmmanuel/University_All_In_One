param(
    [switch]$FullSuite
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$api = $PSScriptRoot
& (Join-Path $root "scripts\sync-before-test.ps1")
if ($LASTEXITCODE -ne 0) { throw "Repository synchronization failed." }
$python = Join-Path $api ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "API virtual environment not found: $python" }
$envFile = Join-Path $root ".env"
if (-not (Test-Path $envFile)) { throw "Missing root .env. Configure POSTGRES_PASSWORD for Docker Compose first." }
$line = Get-Content $envFile | Where-Object { $_ -match '^\s*POSTGRES_PASSWORD\s*=' } | Select-Object -Last 1
if (-not $line) { throw "POSTGRES_PASSWORD missing from root .env." }
$password = ($line -split '=',2)[1].Trim().Trim('"').Trim("'")
if ([string]::IsNullOrWhiteSpace($password)) { throw "POSTGRES_PASSWORD is empty." }
$escaped = [uri]::EscapeDataString($password)
$testUrl = "postgresql+psycopg://educyber:${escaped}@127.0.0.1:5434/educyber_test?connect_timeout=5"
$env:TEST_DATABASE_URL = $testUrl
$env:DATABASE_URL = $testUrl
$env:POSTGRES_PASSWORD = $password
Push-Location $root
try {
    # Dedicated container, database and volume: never migrate the development
    # database or the pre-existing educyber_test database on port 5433.
    docker compose up -d --wait postgres-test
    if ($LASTEXITCODE -ne 0) { throw "Dedicated PostgreSQL test service failed to start." }
    $running = docker compose ps --status running --services
    if ($LASTEXITCODE -ne 0 -or $running -notcontains "postgres-test") {
        throw "Dedicated PostgreSQL test service is not running."
    }
    Push-Location $api
    try {
        & $python -m alembic upgrade head
        if ($LASTEXITCODE -ne 0) { throw "Test database migration failed. No application database was modified." }
        if ($FullSuite) {
            & $python -m pytest -q
        } else {
            & $python -m pytest test_schema_readiness.py test_full_gameplay_http.py -q
        }
        if ($LASTEXITCODE -ne 0) { throw "Tests failed. See the error output above." }
    } finally { Pop-Location }
} finally {
    Pop-Location
    Remove-Item Env:TEST_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:POSTGRES_PASSWORD -ErrorAction SilentlyContinue
}
