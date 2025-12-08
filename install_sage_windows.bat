@echo off
REM ================================================
REM Sage AI Civilization - Windows Installation
REM Minimal Viable Fork (for demos and testing)
REM ================================================
REM Version: 1.0
REM Date: 2025-12-04

echo.
echo ================================================
echo  Sage AI Civilization - Windows Installation
echo  Minimal Viable Fork
echo ================================================
echo.
echo This script will install:
echo  - Claude Code CLI (if not present)
echo  - Sage civilization repository
echo  - Basic configuration files
echo.
echo Prerequisites required:
echo  - Git (https://git-scm.com/download/win)
echo  - Node.js 18+ (https://nodejs.org)
echo  - Anthropic API key (https://console.anthropic.com)
echo.
echo Installation time: 8-10 minutes
echo.
pause

REM ================================================
REM STEP 1: Check Prerequisites
REM ================================================
echo.
echo [STEP 1/5] Checking prerequisites...
echo.

REM Check Git
echo Checking Git...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git not found!
    echo.
    echo Please install Git first:
    echo   1. Visit: https://git-scm.com/download/win
    echo   2. Download and run the installer
    echo   3. Accept default settings
    echo   4. Restart this script after installation
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
echo [OK] %GIT_VERSION%

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found!
    echo.
    echo Please install Node.js first:
    echo   1. Visit: https://nodejs.org
    echo   2. Download the LTS version (18+)
    echo   3. Run the installer
    echo   4. Restart this script after installation
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo [OK] Node.js %NODE_VERSION%

REM Check Node.js version is 18+
for /f "tokens=1 delims=v." %%i in ('node --version') do set NODE_MAJOR=%%i
if %NODE_MAJOR% LSS 18 (
    echo [ERROR] Node.js version is too old!
    echo You have: %NODE_VERSION%
    echo Required: v18 or higher
    echo.
    echo Please upgrade Node.js:
    echo   Visit: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo.
echo All prerequisites satisfied!

REM ================================================
REM STEP 2: Check/Install Claude Code
REM ================================================
echo.
echo [STEP 2/5] Checking Claude Code CLI...
echo.

claude --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Claude Code not found. Installing...
    echo.
    echo This may take 2-3 minutes...
    npm install -g @anthropic-ai/claude-code
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Claude Code!
        echo.
        echo Try manual installation:
        echo   1. Open Command Prompt as Administrator
        echo   2. Run: npm install -g @anthropic-ai/claude-code
        echo   3. Restart this script
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Claude Code installed successfully!
) else (
    for /f "tokens=*" %%i in ('claude --version') do set CLAUDE_VERSION=%%i
    echo [OK] Claude Code found (%CLAUDE_VERSION%)
)

REM ================================================
REM STEP 3: Clone Repository
REM ================================================
echo.
echo [STEP 3/5] Cloning Sage repository...
echo.

if exist sage-civilization (
    echo [WARNING] sage-civilization directory already exists!
    echo.
    set /p OVERWRITE="Do you want to use existing directory? (Y/N): "
    if /i "%OVERWRITE%"=="N" (
        echo.
        echo Please manually delete or rename the sage-civilization directory
        echo Then restart this script.
        echo.
        pause
        exit /b 1
    )
    echo [OK] Using existing directory
    cd sage-civilization
) else (
    echo Cloning from GitHub...
    git clone https://github.com/aicivsage/sage-civilization.git
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to clone repository!
        echo.
        echo Possible causes:
        echo   - No internet connection
        echo   - GitHub is down
        echo   - Repository URL changed
        echo.
        echo Try manual clone:
        echo   git clone https://github.com/aicivsage/sage-civilization.git
        echo.
        pause
        exit /b 1
    )
    cd sage-civilization
    echo [OK] Repository cloned successfully!
)

REM ================================================
REM STEP 4: Configure Environment
REM ================================================
echo.
echo [STEP 4/5] Configuring environment...
echo.

if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul 2>&1
        echo [OK] Created .env from template
    ) else (
        echo Creating basic .env file...
        (
            echo # Sage AI Civilization - Environment Configuration
            echo ANTHROPIC_API_KEY=your-api-key-here
            echo CIVILIZATION_NAME=Sage
            echo.
            echo # Get your API key from: https://console.anthropic.com
        ) > .env
        echo [OK] Created basic .env file
    )
) else (
    echo [OK] .env file already exists
)

REM ================================================
REM STEP 5: Verify Installation
REM ================================================
echo.
echo [STEP 5/5] Verifying installation...
echo.

set ERRORS=0

if exist .claude (
    echo [OK] .claude directory found
) else (
    echo [ERROR] .claude directory missing!
    set ERRORS=1
)

if exist memories (
    echo [OK] memories directory found
) else (
    echo [ERROR] memories directory missing!
    set ERRORS=1
)

if exist tools (
    echo [OK] tools directory found
) else (
    echo [ERROR] tools directory missing!
    set ERRORS=1
)

if exist .claude\CLAUDE.md (
    echo [OK] Constitutional document found
) else (
    echo [ERROR] .claude\CLAUDE.md missing!
    set ERRORS=1
)

if %ERRORS% NEQ 0 (
    echo.
    echo [WARNING] Installation incomplete!
    echo Some required files are missing.
    echo Try re-cloning the repository.
    echo.
)

REM ================================================
REM INSTALLATION COMPLETE
REM ================================================
echo.
echo ================================================
echo  Installation Complete!
echo ================================================
echo.

if %ERRORS% EQU 0 (
    echo [SUCCESS] All components installed and verified!
) else (
    echo [WARNING] Installation completed with errors
)

echo.
echo ================================================
echo  IMPORTANT: Next Steps
echo ================================================
echo.
echo 1. GET YOUR API KEY
echo    - Visit: https://console.anthropic.com
echo    - Create account or sign in
echo    - Go to: Settings ^> API Keys
echo    - Create new key and copy it
echo.
echo 2. ADD API KEY TO .env FILE
echo    - Open: sage-civilization\.env
echo    - Replace "your-api-key-here" with your actual key
echo    - Save and close the file
echo.
echo 3. LAUNCH CLAUDE CODE
echo    - Open Command Prompt
echo    - Navigate to: sage-civilization directory
echo    - Run: claude
echo    - Follow authentication prompts
echo.
echo 4. VERIFY INSTALLATION
echo    - Run: verify_installation.bat
echo    - Check for GO status
echo.
echo ================================================
echo  For detailed instructions, see:
echo  INSTALLATION-GUIDE-WINDOWS.md
echo ================================================
echo.
echo Current directory: %CD%
echo.
pause
