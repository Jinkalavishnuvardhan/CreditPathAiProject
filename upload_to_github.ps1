# CreditPathAI - Upload to GitHub Script
# This script will upload your code to GitHub

$gitPath = "C:\Program Files\Git\bin\git.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CreditPathAI GitHub Upload Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Get GitHub username
Write-Host "STEP 1: GitHub Account Setup" -ForegroundColor Yellow
Write-Host ""
$username = Read-Host "Enter your GitHub username"
Write-Host ""

# Step 2: Configure Git
Write-Host "STEP 2: Configuring Git..." -ForegroundColor Yellow
& $gitPath config --global user.name "$username"
& $gitPath config --global user.email "$username@users.noreply.github.com"
Write-Host "✓ Git configured!" -ForegroundColor Green
Write-Host ""

# Step 3: Initialize repository
Write-Host "STEP 3: Initializing Git repository..." -ForegroundColor Yellow
& $gitPath init
Write-Host "✓ Repository initialized!" -ForegroundColor Green
Write-Host ""

# Step 4: Add all files
Write-Host "STEP 4: Adding all files..." -ForegroundColor Yellow
& $gitPath add .
Write-Host "✓ Files added!" -ForegroundColor Green
Write-Host ""

# Step 5: Create commit
Write-Host "STEP 5: Creating commit..." -ForegroundColor Yellow
& $gitPath commit -m "Initial commit - CreditPathAI"
Write-Host "✓ Commit created!" -ForegroundColor Green
Write-Host ""

# Step 6: Set branch name
Write-Host "STEP 6: Setting branch to 'main'..." -ForegroundColor Yellow
& $gitPath branch -M main
Write-Host "✓ Branch set!" -ForegroundColor Green
Write-Host ""

# Step 7: Add remote
Write-Host "STEP 7: Connecting to GitHub..." -ForegroundColor Yellow
$repoUrl = "https://github.com/$username/CreditPathAI.git"
Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan
& $gitPath remote add origin $repoUrl
Write-Host "✓ Connected to GitHub!" -ForegroundColor Green
Write-Host ""

# Step 8: Push to GitHub
Write-Host "STEP 8: Uploading to GitHub..." -ForegroundColor Yellow
Write-Host "You may be asked for your GitHub credentials..." -ForegroundColor Cyan
Write-Host ""
& $gitPath push -u origin main
Write-Host ""
Write-Host "✓ Upload complete!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SUCCESS! Code uploaded to GitHub!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Deploy to Render.com" -ForegroundColor Yellow
Write-Host "Go to: https://render.com" -ForegroundColor Cyan
Write-Host ""
