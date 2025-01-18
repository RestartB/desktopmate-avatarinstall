Write-Host "Downloading Steam dependency..."

# Make temp folder if it doesn't exist
$tempFolder = "$PSScriptRoot\installer-temp"
if (-not (Test-Path $tempFolder)) {
    New-Item -ItemType Directory -Path $tempFolder
}

# Download Steam dependency
$depInstallerPath = "$PSScriptRoot\installer-temp\VdfDeserializer.psm1"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/BartJolling/ps-steam-cmd/refs/heads/master/VdfDeserializer.psm1" -OutFile $depInstallerPath

# Done
Write-Host "Done. Starting installer script...`n"
& ./installer.ps1 -ExecutionPolicy Bypass