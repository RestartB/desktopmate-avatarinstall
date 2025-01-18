Using module .\installer-temp\VdfDeserializer.psm1;

function ToMarkdown([String]$Text) {
    if ([string]::IsNullOrEmpty($Text)) { return "" }
    # Detect if ConvertFrom-Markdown is available
    if ($legacyPowershell) {
        return $Text.Replace("*", "")
    } else {
        return (ConvertFrom-Markdown -InputObject $Text.Replace("\", "/") -AsVT100EncodedString).VT100EncodedString.Replace("`n", "")
    }
}

# Check if Powershell version is 6 or newer
Write-Host "`nChecking Powershell version..."
if ($PSVersionTable.PSVersion.Major -lt 6) {
    $legacyPowershell = $true
} else {
    $legacyPowershell = $false
}
Write-Host -ForegroundColor Green (ToMarkdown "Powershell version: **$($PSVersionTable.PSVersion)** (legacy: $legacyPowershell)")
Write-Host

Write-Host (ToMarkdown "**Desktop Mate Avatar Loader Autoinstall v1.1.0 - Powershell**")
Write-Host (ToMarkdown "**2025, RestartB**")
Write-Host (ToMarkdown "https://github.com/RestartB/desktopmate-avatarinstall")

Write-Host

Write-Host (ToMarkdown "**Please ensure that Desktop Mate has been opened once before running the script, and that it is not currently running.**")
Write-Host (ToMarkdown "*Press enter to continue...*")
Read-Host

Write-Host "Checking operating system..."

$os = [System.Environment]::OSVersion.Platform
if ($os -eq "Win32NT") {
    Write-Host -ForegroundColor Green (ToMarkdown "Operating system: **Windows**")
} else {
    Write-Host -ForegroundColor Red (ToMarkdown "Operating system: **$os**")
    Write-Host "This script is only compatible with Windows."
    exit
}

# Read registry to find Steam
Write-Host "`nDetecting Steam..."
$steamPath = Get-ItemProperty -Path "HKCU:\Software\Valve\Steam" -Name "SteamPath" -ErrorAction SilentlyContinue

if ($null -eq $steamPath) {
    Write-Host -ForegroundColor Red "Error: Could not detect Steam installation."
    exit
} else {
    Write-Host -ForegroundColor Green (ToMarkdown "Steam installation found at: **$($steamPath.SteamPath)**")
}

# Open Steam library file
Write-Host "`nOpening Steam Library..."
$steamLibraryFile = "$($steamPath.SteamPath)\steamapps\libraryfolders.vdf"
$vdf = [VdfDeserializer]::new()

$steamLibrary = $vdf.Deserialize((Get-Content -Path $steamLibraryFile -Raw))
$steamLibraryJSON = ConvertTo-Json $steamLibrary -Depth 5
$steamLibraryData = ConvertFrom-Json $steamLibraryJSON
$desktopMatePath = $null

Write-Host "Finding Desktop Mate install..."
foreach ($folder in $steamLibraryData.libraryfolders.PSObject.Properties) {
    $libraryPath = $folder.Value.path
    $libraryApps = $folder.Value.apps.PSObject.Properties

    foreach ($app in $libraryApps) {
        # Check if target ID matches Desktop Mate's AppID
        if ($app.Name -eq "3301060") {
            $desktopMatePath = "$libraryPath\steamapps\common\Desktop Mate"
            Write-Host -ForegroundColor Green (ToMarkdown "Found Desktop Mate: **$desktopMatePath**")
            break
        }
    }
}

if ($null -eq $desktopMatePath) {
    Write-Host -ForegroundColor Red "Error: Could not find Desktop Mate installation."
    exit
}

# Make temp folder if it doesn't exist
$tempFolder = "$PSScriptRoot\installer-temp"
if (-not (Test-Path $tempFolder)) {
    New-Item -ItemType Directory -Path $tempFolder
}

# Download .NET 6
Write-Host "`nDownloading & installing .NET 6..."
$dotnetInstallerPath = "$PSScriptRoot\installer-temp\dotnet-install.ps1"
Invoke-WebRequest -Uri "https://dot.net/v1/dotnet-install.ps1" -OutFile $dotnetInstallerPath

# Run .NET 6 installer
& $dotnetInstallerPath -Channel 6.0 -Version latest -Runtime dotnet

# Download .NET 6
Write-Host "`nDownloading MelonLoader..."
$melonPath = "$PSScriptRoot\installer-temp\melonloader.zip"
Invoke-WebRequest -Uri "https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x64.zip" -OutFile $melonPath

Write-Host -ForegroundColor Green "Downloaded!"

# Download .NET 6
Write-Host "`nDownloading mod..."
$modPath = "$PSScriptRoot\installer-temp\mod.zip"
Invoke-WebRequest -Uri "https://github.com/YusufOzmen01/desktopmate-custom-avatar-loader/releases/latest/download/CustomAvatarLoader.zip" -OutFile $modPath

Write-Host -ForegroundColor Green "Downloaded!"

# Extract files
Write-Host "`nExtracting files..."
Expand-Archive -Path $melonPath -DestinationPath $desktopMatePath -Force
Expand-Archive -Path $modPath -DestinationPath $desktopMatePath -Force
Write-Host -ForegroundColor Green "Done!"

# Cleanup
Write-Host "`nCleaning up..."
Remove-Item -Path $tempFolder -Recurse
Write-Host -ForegroundColor Green "Cleaned up!"

# Done
Write-Host -ForegroundColor Green "`nAll done!"
Write-Host "Press enter to run Desktop Mate (press open when prompted), or press CTRL+C / close the window to exit.`n"

Write-Host (ToMarkdown "**Note**")
Write-Host "The first launch of Desktop Mate may take longer than usual, this is normal as the mod loader is injecting itself into Desktop Mate."

Read-Host
Start-Process "steam://rungameid/3301060"