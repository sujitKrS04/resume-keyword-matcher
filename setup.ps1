# Resume Keyword Matcher - Windows Setup Script
# Run this script in PowerShell to set up the application

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  Resume Keyword Matcher - Setup Script" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9+ first." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠ Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/n)"
    if ($response -eq "y") {
        Remove-Item -Recurse -Force "venv"
        python -m venv venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    } else {
        Write-Host "Using existing virtual environment" -ForegroundColor Cyan
    }
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Install requirements
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install some dependencies" -ForegroundColor Red
    exit 1
}

# Create .env file
Write-Host "`nSetting up environment file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠ .env file already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to overwrite it? (y/n)"
    if ($response -eq "y") {
        Copy-Item ".env.example" ".env" -Force
        Write-Host "✓ .env file created" -ForegroundColor Green
    } else {
        Write-Host "Keeping existing .env file" -ForegroundColor Cyan
    }
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
}

# Final instructions
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Next steps:`n" -ForegroundColor Yellow
Write-Host "1. Edit the .env file and add your Gemini API key" -ForegroundColor White
Write-Host "   Get your free API key from:" -ForegroundColor Gray
Write-Host "   https://makersuite.google.com/app/apikey`n" -ForegroundColor Cyan

Write-Host "2. Run the application:" -ForegroundColor White
Write-Host "   streamlit run app.py`n" -ForegroundColor Cyan

Write-Host "3. Open your browser and visit:" -ForegroundColor White
Write-Host "   http://localhost:8501`n" -ForegroundColor Cyan

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Happy resume optimizing! 🚀" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Cyan

# Ask if user wants to run the app now
$runNow = Read-Host "Would you like to run the application now? (y/n)"
if ($runNow -eq "y") {
    Write-Host "`nStarting application...`n" -ForegroundColor Yellow
    streamlit run app.py
}
