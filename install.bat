@echo off
chcp 65001 >nul

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Run as Administrator
    pause
    exit /b
)

set "INSTALLDIR=%APPDATA%\RobotLang"
mkdir "%INSTALLDIR%" 2>nul
copy /Y "%~dp0robot.exe" "%INSTALLDIR%\robot.exe"
setx PATH "%INSTALLDIR%;%PATH%"
assoc .bot=RobotLang.bot
ftype RobotLang.bot="%INSTALLDIR%\robot.exe" "%%1"

echo Installed.
pause