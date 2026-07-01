@echo off
title Yojana Sahayak - AI Government Scheme Chatbot
echo.
echo  ==========================================
echo   Yojana Sahayak - Starting...
echo  ==========================================
echo.
cd /d "%~dp0"
echo  Opening at: http://localhost:8501
echo  Press Ctrl+C to stop the server
echo.
C:\Users\hp\anaconda3\python.exe -X utf8 -m streamlit run app.py --server.port 8501
pause
