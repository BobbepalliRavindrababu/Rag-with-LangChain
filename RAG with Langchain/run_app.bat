@echo off
echo Starting RAG Document Q&A System...
echo =================================
echo.

cd /d "%~dp0"

echo Checking dependencies...
python -m pip install streamlit --quiet

echo.
echo Launching web application...
echo The browser will open automatically.
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

echo.
echo Application stopped.
pause
