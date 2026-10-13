$ErrorActionPreference = "Stop"

if ($env:ALLURE_BIN -and (Test-Path -LiteralPath $env:ALLURE_BIN)) {
    $allure = $env:ALLURE_BIN
}
else {
    $allureCommand = Get-Command allure -ErrorAction SilentlyContinue
    if ($allureCommand) {
        $allure = $allureCommand.Source
    }
    else {
        $mockAllure = Join-Path (Split-Path $PSScriptRoot -Parent) "Mock\tools\allure-cli\node_modules\.bin\allure.cmd"
        if (Test-Path -LiteralPath $mockAllure) {
            $allure = $mockAllure
        }
        else {
            throw "Allure CLI was not found. Install Allure or set ALLURE_BIN."
        }
    }
}

Push-Location $PSScriptRoot
try {
    & $allure generate ".\allure-results" -o ".\allure-report" --clean
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
    & $allure open ".\allure-report"
}
finally {
    Pop-Location
}
