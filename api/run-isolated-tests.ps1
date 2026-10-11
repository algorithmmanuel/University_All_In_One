param(
    [switch]$FullSuite
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$api = $PSScriptRoot
$python = Join-Path $api ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "API virtual environment not found: $python" }
$envFile = Join-Path $root ".env"
if (-not (Test-Path $envFile)) { throw "Missing root .env. Configure POSTGRES_PASSWORD for Docker Compose first." }
$line = Get-Content $envFile | Where-Object { $_ -match '^\s*POSTGRES_PASSWORD\s*=' } | Select-Object -Last 1
if (-not $line) { throw "POSTGRES_PASSWORD missing from root .env." }
$password = ($line -split '=',2)[1].Trim().Trim('"').Trim("'")
if ([string]::IsNullOrWhiteSpace($password)) { throw "POSTGRES_PASSWORD is empty." }
$escaped = [uri]::EscapeDataString($password)
$testUrl = "postgresql+psycopg://educyber:${escaped}@127.0.0.1:5433/educyber_test?connect_timeout=5"
$env:TEST_DATABASE_URL = $testUrl
$env:DATABASE_URL = $testUrl
$env:POSTGRES_PASSWORD = $password
Push-Location $root
try {
    docker compose ps --status running postgres | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose is unavailable. Start Docker Desktop and the PostgreSQL service." }
    $running = docker compose ps --status running --services
    if ($LASTEXITCODE -ne 0 -or $running -notcontains "postgres") { throw "PostgreSQL is not running. Run docker compose up -d postgres." }
    # Database creation is isolated; never change the application database.
    $exists = docker compose exec -T postgres psql -U educyber -d postgres -Atqc "SELECT 1 FROM pg_database WHERE datname = 'educyber_test'"
    if ($LASTEXITCODE -ne 0) { throw "Unable to query PostgreSQL databases." }
    if (($exists | Out-String).Trim() -ne "1") {
        docker compose exec -T postgres psql -U educyber -d postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE educyber_test"
        if ($LASTEXITCODE -ne 0) { throw "Could not create isolated educyber_test database." }
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
