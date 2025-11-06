# ==========================
# TensorFlow Setup Script
# For Windows 10/11 - CPU version
# ==========================
# Step 1: Install Python 3.10 (if not installed)
Write-Host "Checking for Python 3.10 installation..." -ForegroundColor Cyan
$python310 = (Get-Command python3.10 -ErrorAction SilentlyContinue)

if (-not $python310) {
    Write-Host "Python 3.10 not found. Downloading installer..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe" -OutFile "$env:TEMP\python310.exe"
    Write-Host "Installing Python 3.10..." -ForegroundColor Yellow
    Start-Process "$env:TEMP\python310.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
} else {
    Write-Host "Python 3.10 already installed." -ForegroundColor Green
}

# Step 2: Create a TensorFlow virtual environment
Write-Host "Creating virtual environment 'tfenv'..." -ForegroundColor Cyan
python3.10 -m venv "$env:USERPROFILE\tfenv"

# Step 3: Activate environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$env:USERPROFILE\tfenv\Scripts\activate.ps1"

# Step 4: Upgrade pip and core tools
Write-Host "Upgrading pip, setuptools, and wheel..." -ForegroundColor Cyan
pip install --upgrade pip setuptools wheel

# Step 5: Install TensorFlow (CPU version)
Write-Host "Installing TensorFlow 2.12 (CPU)..." -ForegroundColor Cyan
pip install tensorflow==2.12

# Step 6: Optional - Install extra ML tools
Write-Host "Installing common ML packages (numpy, matplotlib, pandas, scikit-learn)..." -ForegroundColor Cyan
pip install numpy pandas matplotlib scikit-learn

# Step 7: Verify installation
Write-Host "Verifying TensorFlow installation..." -ForegroundColor Cyan
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

Write-Host "✅ TensorFlow environment setup complete!" -ForegroundColor Green
Write-Host "To activate later, run:" -ForegroundColor Yellow
Write-Host "    & `$env:USERPROFILE\tfenv\Scripts\activate.ps1" -ForegroundColor Yellow
