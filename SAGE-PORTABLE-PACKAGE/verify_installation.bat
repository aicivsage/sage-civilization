@echo off
REM ================================================
REM Sage AI Civilization - Installation Verification
REM ================================================
REM Version: 1.0
REM Date: 2025-12-04

echo.
echo ================================================
echo  Sage Installation Verification
echo ================================================
echo.

set CHECKS_PASSED=0
set CHECKS_TOTAL=0

REM ================================================
REM CHECK 1: Git
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 1/10] Git installation...
git --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
    echo [PASS] %GIT_VERSION%
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] Git not found
)

REM ================================================
REM CHECK 2: Node.js
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 2/10] Node.js installation...
node --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo [PASS] Node.js %NODE_VERSION%
    set /a CHECKS_PASSED+=1

    REM Check version is 18+
    for /f "tokens=1 delims=v." %%i in ('node --version') do set NODE_MAJOR=%%i
    if %NODE_MAJOR% LSS 18 (
        echo [WARN] Node.js version is below recommended (18+)
    )
) else (
    echo [FAIL] Node.js not found
)

REM ================================================
REM CHECK 3: Claude Code CLI
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 3/10] Claude Code CLI...
claude --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('claude --version') do set CLAUDE_VERSION=%%i
    echo [PASS] Claude Code installed (%CLAUDE_VERSION%)
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] Claude Code not found
)

REM ================================================
REM CHECK 4: Repository Directory
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 4/10] Repository directory...
if exist .claude (
    echo [PASS] .claude directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .claude directory missing - are you in sage-civilization folder?
)

REM ================================================
REM CHECK 5: Constitutional Document
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 5/10] Constitutional document...
if exist .claude\CLAUDE.md (
    echo [PASS] .claude\CLAUDE.md exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .claude\CLAUDE.md missing
)

REM ================================================
REM CHECK 6: Memories Directory
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 6/10] Memories directory...
if exist memories (
    echo [PASS] memories directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] memories directory missing
)

REM ================================================
REM CHECK 7: Tools Directory
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 7/10] Tools directory...
if exist tools (
    echo [PASS] tools directory exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] tools directory missing
)

REM ================================================
REM CHECK 8: Environment File
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 8/10] Environment configuration...
if exist .env (
    echo [PASS] .env file exists
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] .env file missing
)

REM ================================================
REM CHECK 9: API Key Configured
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 9/10] API key configuration...
if exist .env (
    findstr /C:"ANTHROPIC_API_KEY=sk-ant-" .env >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [PASS] API key appears to be configured
        set /a CHECKS_PASSED+=1
    ) else (
        findstr /C:"your-api-key-here" .env >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo [FAIL] API key not configured (still has placeholder)
        ) else (
            findstr /C:"ANTHROPIC_API_KEY=" .env >nul 2>&1
            if %ERRORLEVEL% EQU 0 (
                echo [WARN] API key value looks unusual - verify it's correct
                set /a CHECKS_PASSED+=1
            ) else (
                echo [FAIL] ANTHROPIC_API_KEY not found in .env
            )
        )
    )
) else (
    echo [FAIL] .env file missing
)

REM ================================================
REM CHECK 10: Agent Manifests
REM ================================================
set /a CHECKS_TOTAL+=1
echo [CHECK 10/10] Agent manifests...
if exist .claude\agents (
    dir /b .claude\agents\*.md >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        for /f %%i in ('dir /b .claude\agents\*.md ^| find /c /v ""') do set AGENT_COUNT=%%i
        echo [PASS] Found %AGENT_COUNT% agent manifests
        set /a CHECKS_PASSED+=1
    ) else (
        echo [FAIL] No agent manifests found in .claude\agents
    )
) else (
    echo [FAIL] .claude\agents directory missing
)

REM ================================================
REM RESULTS
REM ================================================
echo.
echo ================================================
echo  Verification Results
echo ================================================
echo.
echo Checks Passed: %CHECKS_PASSED% / %CHECKS_TOTAL%
echo.

if %CHECKS_PASSED% EQU %CHECKS_TOTAL% (
    echo [GO] Installation verified successfully!
    echo.
    echo You are ready to launch Sage:
    echo   1. Open Command Prompt
    echo   2. Navigate to: %CD%
    echo   3. Run: claude
    echo   4. Follow authentication prompts
    echo.
    echo ================================================
    exit /b 0
) else if %CHECKS_PASSED% GEQ 8 (
    echo [CAUTION] Most checks passed, but some issues detected
    echo.
    echo Review failed checks above and fix before proceeding.
    echo Common fixes:
    echo   - Missing API key: Edit .env and add your key
    echo   - Missing directories: Re-run install_sage_windows.bat
    echo.
    echo ================================================
    exit /b 1
) else (
    echo [NO-GO] Installation incomplete!
    echo.
    echo Too many checks failed. Please:
    echo   1. Review failed checks above
    echo   2. Re-run: install_sage_windows.bat
    echo   3. Verify all prerequisites are installed
    echo.
    echo ================================================
    exit /b 1
)
