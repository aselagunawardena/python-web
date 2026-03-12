#!/usr/bin/env pwsh
# Deploy to Azure App Service
param(
    [string]$ResourceGroup = "rg-finite-aue",
    [string]$AppName = "finiteorg",
    [switch]$Deploy = $false
)

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "Azure CLI 'az' not found."
    exit 1
}

$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$tmpZip = "$env:TEMP\deploy_$timestamp.zip"

Write-Host "Creating deployment zip..."
Write-Host ""

# Compress with directory structure preserved
# Include root files (*.py, *.txt, *.md) and all folders (templates, static)
Compress-Archive -Path @("app.py", "requirements.txt", "*.md", "templates", "static") `
                 -DestinationPath $tmpZip -Force

Write-Host "Zip contents:"
# List what's in the zip
[System.IO.Compression.ZipFile]::OpenRead($tmpZip).Entries | ForEach-Object {
    if ($_.Length -gt 0) {
        Write-Host "  $($_.FullName)"
    }
}

Write-Host ""
$zipSize = (Get-Item $tmpZip).Length / 1KB
Write-Host "Zip file created: $tmpZip"
Write-Host "Size: $([Math]::Round($zipSize)) KB"
Write-Host ""

if ($Deploy) {
    Write-Host "Deploying to Azure..."
    az webapp deployment source config-zip --resource-group $ResourceGroup --name $AppName --src $tmpZip
    Write-Host "Deployment complete!"
    Remove-Item -Path $tmpZip -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "ZIP READY FOR INSPECTION"
    Write-Host "To deploy, run: .\deploy_to_app_service.ps1 -Deploy"
    Write-Host ""
    Write-Host "Zip file kept at: $tmpZip"
}

exit 0

exit 0
