param([switch]$Remove)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$name = "EduCyber-GitHub-Sync-Check"
if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction Stop
    Write-Host "Removed $name"
    exit 0
}
# Periodic check is FETCH-ONLY. No merges, pushes, resets or file changes.
$script = Join-Path $PSScriptRoot "periodic-sync-check.ps1"
$exe = (Get-Command powershell.exe -ErrorAction Stop).Source
$action = New-ScheduledTaskAction -Execute $exe -Argument ('-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + $script + '"') -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 4)
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -StartWhenAvailable
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $settings -Description "Fetch-only EduCyber GitHub revision check every four hours; no local file modification" -Force | Out-Null
Write-Host "Registered $name: GitHub fetch-only check every four hours. No code is automatically overwritten."
