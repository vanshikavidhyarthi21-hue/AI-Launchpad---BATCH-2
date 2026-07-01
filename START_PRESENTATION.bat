@echo off
title Yojana Sahayak Presentation Launcher
echo.
echo  ==========================================
echo   Yojana Sahayak - Presentation
echo  ==========================================
echo.
cd /d "%~dp0"
echo  Opening presentation deck in your default browser...
start "" "yojana_sahayak_presentation.html"
echo  Done! Click "Play Presentation" at the top of the browser page for the voice-guided tour.
echo.
timeout /t 5
