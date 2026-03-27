# publish.ps1 - Automates PyPI package update process

param (
    [string]$VersionType = "patch" # Options: major, minor, patch
)

# --- Configuration ---
$pyprojectToml = "pyproject.toml"
$versionFile = "src/claude_data_skills/__version__.py" # New location for version string

# --- Helper Function to Update Version ---
function Update-PackageVersion {
    param (
        [string]$CurrentVersion,
        [string]$VersionType
    )
    $versionParts = $CurrentVersion.Split('.')
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]
    $patch = [int]$versionParts[2]

    switch ($VersionType) {
        "major" { $major++; $minor = 0; $patch = 0 }
        "minor" { $minor++; $patch = 0 }
        "patch" { $patch++ }
        default { Throw "Invalid version type: $VersionType. Must be major, minor, or patch." }
    }
    return "$major.$minor.$patch"
}

# --- Main Script Logic ---

Write-Host "--- Automating PyPI Package Update ---"

# 1. Ensure 'src' directory and __version__.py exist
Write-Host "Creating src/claude_data_skills/__version__.py..."
New-Item -ItemType Directory -Path src/claude_data_skills -Force | Out-Null
# Ensure __version__.py exists, if it doesn't, initialize it for safety before reading
if (-not (Test-Path $versionFile)) {
    Set-Content -Path $versionFile -Value "`__version__ = '0.0.0'`"
}

# 2. Get current version from __version__.py
$currentVersionLine = Get-Content -Path $versionFile | Select-String "__version__ ="
if ($currentVersionLine) {
    # Extract version from a line like: __version__ = '3.0.0'
    $currentVersion = ($currentVersionLine.Line -split "'")[1]
    Write-Host "Current package version: $currentVersion"
} else {
    Throw "Could not find __version__ in $versionFile"
}

# 3. Calculate new version
$newVersion = Update-PackageVersion $currentVersion $VersionType
Write-Host "New package version: $newVersion"

# 4. Update __version__.py
(Get-Content -Path $versionFile) -replace "`__version__ = '$currentVersion'`", "`__version__ = '$newVersion'`" | Set-Content -Path $versionFile
Write-Host "Updated version in $versionFile to $newVersion"

# 5. Install build and twine
Write-Host "Installing build and twine..."
pip install build twine | Out-Null
Write-Host "Build and twine installed."

# 6. Clean up old dist files (important for clean builds)
Write-Host "Cleaning up old distribution files..."
Remove-Item -Path dist -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Old distribution files cleaned."

# 7. Build the package
Write-Host "Building package..."
python -m build | Out-Null
Write-Host "Package built successfully. Distributions are in the dist/ directory."

# 8. Upload to PyPI
Write-Host "Uploading package to PyPI..."
# Twine will automatically use credentials from ~/.pypirc or standard environment variables (TWINE_USERNAME, TWINE_PASSWORD, TWINE_API_KEY)
python -m twine upload dist/*
Write-Host "Package uploaded to PyPI."

Write-Host "--- PyPI Update Process Complete ---"
Write-Host "New version $newVersion is available on PyPI."
