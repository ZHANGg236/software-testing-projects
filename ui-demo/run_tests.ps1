$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Virtual environment was not found: $python"
}

Push-Location $PSScriptRoot
try {
    & $python -m pytest
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
