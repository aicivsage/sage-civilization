# ================================================
# Sage AI Civilization - Windows Installation
# PowerShell Version (Enhanced)
# ================================================
# Version: 1.0
# Date: 2025-12-04
# Requires: PowerShell 5.1+

# Set strict mode for better error handling
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Function to write colored output
function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "INFO"
    )

    switch ($Type) {
        "SUCCESS" { Write-Host "[OK] $Message" -ForegroundColor Green }
        "ERROR" { Write-Host "[ERROR] $Message" -ForegroundColor Red }
        "WARNING" { Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
        "INFO" { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
        "STEP" { Write-Host "`n[STEP] $Message" -ForegroundColor Magenta }
        default { Write-Host $Message }
    }
}

# Function to check command availability
function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Function to compare versions
function Compare-Version {
    param(
        [string]$Version,
        [int]$MinMajor
    )

    if ($Version -match '^v?(\d+)') {
        [int]$major = $Matches[1]
        return $major -ge $MinMajor
    }
    return $false
}

# Main installation script
try {
    # Header
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host " Sage AI Civilization - Windows Installation" -ForegroundColor Cyan
    Write-Host " PowerShell Enhanced Version" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This script will install:" -ForegroundColor White
    Write-Host " - Claude Code CLI (if not present)" -ForegroundColor Gray
    Write-Host " - Sage civilization repository" -ForegroundColor Gray
    Write-Host " - Basic configuration files" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Prerequisites required:" -ForegroundColor White
    Write-Host " - Git (https://git-scm.com/download/win)" -ForegroundColor Gray
    Write-Host " - Node.js 18+ (https://nodejs.org)" -ForegroundColor Gray
    Write-Host " - Anthropic API key (https://console.anthropic.com)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Installation time: 8-10 minutes" -ForegroundColor Yellow
    Write-Host ""

    $continue = Read-Host "Press ENTER to continue or Ctrl+C to cancel"

    # ================================================
    # STEP 1: Check Prerequisites
    # ================================================
    Write-Status "Checking prerequisites..." "STEP"
    Write-Host ""

    $prerequisitesFailed = $false

    # Check Git
    Write-Status "Checking Git..." "INFO"
    if (Test-Command "git") {
        $gitVersion = git --version
        Write-Status $gitVersion "SUCCESS"
    } else {
        Write-Status "Git not found!" "ERROR"
        Write-Host ""
        Write-Host "Please install Git first:" -ForegroundColor Yellow
        Write-Host "  1. Visit: https://git-scm.com/download/win" -ForegroundColor Gray
        Write-Host "  2. Download and run the installer" -ForegroundColor Gray
        Write-Host "  3. Accept default settings" -ForegroundColor Gray
        Write-Host "  4. Restart PowerShell after installation" -ForegroundColor Gray
        $prerequisitesFailed = $true
    }

    # Check Node.js
    Write-Status "Checking Node.js..." "INFO"
    if (Test-Command "node") {
        $nodeVersion = node --version
        Write-Status "Node.js $nodeVersion" "SUCCESS"

        # Check version
        if (-not (Compare-Version $nodeVersion 18)) {
            Write-Status "Node.js version is too old!" "ERROR"
            Write-Host "You have: $nodeVersion" -ForegroundColor Yellow
            Write-Host "Required: v18 or higher" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Please upgrade Node.js:" -ForegroundColor Yellow
            Write-Host "  Visit: https://nodejs.org" -ForegroundColor Gray
            $prerequisitesFailed = $true
        }
    } else {
        Write-Status "Node.js not found!" "ERROR"
        Write-Host ""
        Write-Host "Please install Node.js first:" -ForegroundColor Yellow
        Write-Host "  1. Visit: https://nodejs.org" -ForegroundColor Gray
        Write-Host "  2. Download the LTS version (18+)" -ForegroundColor Gray
        Write-Host "  3. Run the installer" -ForegroundColor Gray
        Write-Host "  4. Restart PowerShell after installation" -ForegroundColor Gray
        $prerequisitesFailed = $true
    }

    # Check npm
    if (Test-Command "npm") {
        $npmVersion = npm --version
        Write-Status "npm $npmVersion" "SUCCESS"
    } else {
        Write-Status "npm not found (should come with Node.js)" "WARNING"
    }

    if ($prerequisitesFailed) {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Red
        Write-Host " Prerequisites check failed!" -ForegroundColor Red
        Write-Host " Install missing prerequisites and re-run script" -ForegroundColor Red
        Write-Host "================================================" -ForegroundColor Red
        exit 1
    }

    Write-Host ""
    Write-Status "All prerequisites satisfied!" "SUCCESS"

    # ================================================
    # STEP 2: Check/Install Claude Code
    # ================================================
    Write-Status "Checking Claude Code CLI..." "STEP"
    Write-Host ""

    if (Test-Command "claude") {
        $claudeVersion = claude --version
        Write-Status "Claude Code found ($claudeVersion)" "SUCCESS"
    } else {
        Write-Status "Claude Code not found. Installing..." "INFO"
        Write-Host ""
        Write-Host "This may take 2-3 minutes..." -ForegroundColor Yellow

        try {
            npm install -g @anthropic-ai/claude-code
            Write-Host ""
            Write-Status "Claude Code installed successfully!" "SUCCESS"
        } catch {
            Write-Status "Failed to install Claude Code!" "ERROR"
            Write-Host ""
            Write-Host "Try manual installation:" -ForegroundColor Yellow
            Write-Host "  1. Open PowerShell as Administrator" -ForegroundColor Gray
            Write-Host "  2. Run: npm install -g @anthropic-ai/claude-code" -ForegroundColor Gray
            Write-Host "  3. Restart this script" -ForegroundColor Gray
            exit 1
        }
    }

    # ================================================
    # STEP 3: Clone Repository
    # ================================================
    Write-Status "Cloning Sage repository..." "STEP"
    Write-Host ""

    if (Test-Path "sage-civilization") {
        Write-Status "sage-civilization directory already exists!" "WARNING"
        Write-Host ""
        $overwrite = Read-Host "Do you want to use existing directory? (Y/N)"

        if ($overwrite -ne "Y" -and $overwrite -ne "y") {
            Write-Host ""
            Write-Host "Please manually delete or rename the sage-civilization directory" -ForegroundColor Yellow
            Write-Host "Then restart this script." -ForegroundColor Yellow
            exit 1
        }

        Write-Status "Using existing directory" "SUCCESS"
        Set-Location sage-civilization
    } else {
        Write-Status "Cloning from GitHub..." "INFO"

        try {
            git clone https://github.com/aicivsage/sage-civilization.git
            Set-Location sage-civilization
            Write-Status "Repository cloned successfully!" "SUCCESS"
        } catch {
            Write-Status "Failed to clone repository!" "ERROR"
            Write-Host ""
            Write-Host "Possible causes:" -ForegroundColor Yellow
            Write-Host "  - No internet connection" -ForegroundColor Gray
            Write-Host "  - GitHub is down" -ForegroundColor Gray
            Write-Host "  - Repository URL changed" -ForegroundColor Gray
            Write-Host ""
            Write-Host "Try manual clone:" -ForegroundColor Yellow
            Write-Host "  git clone https://github.com/aicivsage/sage-civilization.git" -ForegroundColor Gray
            exit 1
        }
    }

    # ================================================
    # STEP 4: Configure Environment
    # ================================================
    Write-Status "Configuring environment..." "STEP"
    Write-Host ""

    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Status "Created .env from template" "SUCCESS"
        } else {
            Write-Status "Creating basic .env file..." "INFO"

            $envContent = @"
# Sage AI Civilization - Environment Configuration
ANTHROPIC_API_KEY=your-api-key-here
CIVILIZATION_NAME=Sage

# Get your API key from: https://console.anthropic.com
"@
            $envContent | Out-File -FilePath ".env" -Encoding UTF8
            Write-Status "Created basic .env file" "SUCCESS"
        }
    } else {
        Write-Status ".env file already exists" "SUCCESS"
    }

    # ================================================
    # STEP 5: Verify Installation
    # ================================================
    Write-Status "Verifying installation..." "STEP"
    Write-Host ""

    $errors = 0

    # Check directories
    if (Test-Path ".claude") {
        Write-Status ".claude directory found" "SUCCESS"
    } else {
        Write-Status ".claude directory missing!" "ERROR"
        $errors++
    }

    if (Test-Path "memories") {
        Write-Status "memories directory found" "SUCCESS"
    } else {
        Write-Status "memories directory missing!" "ERROR"
        $errors++
    }

    if (Test-Path "tools") {
        Write-Status "tools directory found" "SUCCESS"
    } else {
        Write-Status "tools directory missing!" "ERROR"
        $errors++
    }

    # Check constitutional document
    if (Test-Path ".claude\CLAUDE.md") {
        Write-Status "Constitutional document found" "SUCCESS"
    } else {
        Write-Status ".claude\CLAUDE.md missing!" "ERROR"
        $errors++
    }

    if ($errors -gt 0) {
        Write-Host ""
        Write-Status "Installation incomplete!" "WARNING"
        Write-Host "Some required files are missing." -ForegroundColor Yellow
        Write-Host "Try re-cloning the repository." -ForegroundColor Yellow
    }

    # ================================================
    # INSTALLATION COMPLETE
    # ================================================
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host " Installation Complete!" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""

    if ($errors -eq 0) {
        Write-Status "All components installed and verified!" "SUCCESS"
    } else {
        Write-Status "Installation completed with $errors error(s)" "WARNING"
    }

    Write-Host ""
    Write-Host "================================================" -ForegroundColor Yellow
    Write-Host " IMPORTANT: Next Steps" -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. GET YOUR API KEY" -ForegroundColor White
    Write-Host "   - Visit: https://console.anthropic.com" -ForegroundColor Gray
    Write-Host "   - Create account or sign in" -ForegroundColor Gray
    Write-Host "   - Go to: Settings > API Keys" -ForegroundColor Gray
    Write-Host "   - Create new key and copy it" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. ADD API KEY TO .env FILE" -ForegroundColor White
    Write-Host "   - Open: sage-civilization\.env" -ForegroundColor Gray
    Write-Host "   - Replace 'your-api-key-here' with your actual key" -ForegroundColor Gray
    Write-Host "   - Save and close the file" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. LAUNCH CLAUDE CODE" -ForegroundColor White
    Write-Host "   - Open PowerShell" -ForegroundColor Gray
    Write-Host "   - Navigate to: sage-civilization directory" -ForegroundColor Gray
    Write-Host "   - Run: claude" -ForegroundColor Gray
    Write-Host "   - Follow authentication prompts" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. VERIFY INSTALLATION" -ForegroundColor White
    Write-Host "   - Run: .\verify_installation.bat" -ForegroundColor Gray
    Write-Host "   - Check for GO status" -ForegroundColor Gray
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host " For detailed instructions, see:" -ForegroundColor Cyan
    Write-Host " INSTALLATION-GUIDE-WINDOWS.md" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Current directory: $PWD" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host " Installation Failed!" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please report this error:" -ForegroundColor Yellow
    Write-Host "  https://github.com/aicivsage/sage-civilization/issues" -ForegroundColor Gray
    exit 1
}
