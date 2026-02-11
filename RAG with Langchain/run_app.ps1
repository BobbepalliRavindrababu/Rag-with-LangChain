# Run RAG Web Application
# Double-click this file to start the web UI

Write-Host "Starting RAG Document Q&A System..." -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Install streamlit if not already installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
python -m pip install streamlit --quiet

Write-Host ""
Write-Host "Launching web application..." -ForegroundColor Green
Write-Host "The browser will open automatically." -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

# Run streamlit
streamlit run app.py

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
pause
