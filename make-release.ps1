param(
    [string]$Version = "dev",
    [switch]$SkipBuild,
    [switch]$OneDir,
    [switch]$DebugConsole
)

$ErrorActionPreference = 'Stop'

function Write-Step([string]$msg) {
    Write-Host "`n==> $msg" -ForegroundColor Cyan
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$distDir = Join-Path $root 'dist'
$releaseRoot = Join-Path $root 'release'
$releaseDir = Join-Path $releaseRoot ("SLCode-{0}" -f $Version)
$zipPath = Join-Path $releaseRoot ("SLCode-{0}.zip" -f $Version)

if (!(Test-Path $releaseRoot)) {
    New-Item -ItemType Directory -Path $releaseRoot | Out-Null
}

if (Test-Path $releaseDir) {
    Remove-Item -Recurse -Force $releaseDir
}
New-Item -ItemType Directory -Path $releaseDir | Out-Null

if (!$SkipBuild) {
    Write-Step "Building executable"
    $args = @('build.py')
    if ($OneDir) {
        $args += '--onedir'
    } else {
        $args += '--onefile'
    }
    if ($DebugConsole) {
        $args += '--debug-console'
    }

    & python @args
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed."
    }
} else {
    Write-Step "Skipping build (--SkipBuild)"
}

Write-Step "Locating built executable"
$exePath = $null

$oneDirCandidate = Join-Path $distDir 'SLCode\SLCode.exe'
$oneFileCandidate = Join-Path $distDir 'SLCode.exe'

if ($OneDir) {
    if (Test-Path $oneDirCandidate) { $exePath = $oneDirCandidate }
} else {
    if (Test-Path $oneFileCandidate) { $exePath = $oneFileCandidate }
}

if (-not $exePath) {
    if (Test-Path $oneFileCandidate) {
        $exePath = $oneFileCandidate
        Write-Host "Detected onefile artifact." -ForegroundColor Yellow
    } elseif (Test-Path $oneDirCandidate) {
        $exePath = $oneDirCandidate
        Write-Host "Detected onedir artifact." -ForegroundColor Yellow
    }
}

if (-not $exePath) {
    throw "Could not find built executable in dist/."
}


Write-Step "Staging release files"
Copy-Item $exePath (Join-Path $releaseDir 'SLCode.exe') -Force
# Copy CLI stub
$cliPath = Join-Path $distDir 'slcode-cli.exe'
if (Test-Path $cliPath) {
        Copy-Item $cliPath (Join-Path $releaseDir 'slcode-cli.exe') -Force
}
# Copy Python bundle
$zipBundle = Join-Path $distDir 'SLCode-app.zip'
if (Test-Path $zipBundle) {
        Copy-Item $zipBundle (Join-Path $releaseDir 'SLCode-app.zip') -Force
}

$readme = @"
# SLCode (Windows Release)

## Quick start
1. Double-click **Launch SLCode.bat**
2. If window rendering fails, run **Install WebView2 Runtime.bat** once, then relaunch.

## Included files
- SLCode.exe
- Launch SLCode.bat
- Install WebView2 Runtime.bat

## Notes
- This is a self-contained app bundle from the user's perspective.
- WebView2 runtime may still be required on some machines.
- The cache data itself is not embedded; this app expects your local/project cache structure.
"@
Set-Content -Path (Join-Path $releaseDir 'README.txt') -Value $readme -Encoding UTF8

Write-Step "Creating zip"
if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}
Compress-Archive -Path (Join-Path $releaseDir '*') -DestinationPath $zipPath

Write-Step "Done"
Write-Host "Release folder: $releaseDir" -ForegroundColor Green
Write-Host "Release zip:    $zipPath" -ForegroundColor Green
