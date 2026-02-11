#!/bin/bash

# Production Startup Script for Tenant Management System
# This script starts the application with production settings

echo "╔══════════════════════════════════════════════════════════╗"
echo "║    Tenant Management System - Production Startup        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then 
    echo "⚠️  Warning: Running as root is not recommended"
    echo "Consider creating a dedicated user for the application"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo "❗ Please edit .env file with your settings before continuing"
        echo ""
        read -p "Press Enter to edit .env now, or Ctrl+C to exit..."
        ${EDITOR:-nano} .env
    else
        echo "❌ .env.example not found"
        exit 1
    fi
fi

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencies not installed"
    read -p "Install now? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Failed to install dependencies"
            exit 1
        fi
        echo "✅ Dependencies installed"
    else
        echo "❌ Cannot start without dependencies"
        exit 1
    fi
else
    echo "✅ Dependencies OK"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p static/qrcodes
mkdir -p backups
mkdir -p logs
echo "✅ Directories ready"

# Check database
if [ ! -f "data/tenants.db" ]; then
    echo "🗄️  Database not found, will be created on first run"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
fi

# Set production mode
export FLASK_ENV=production

# Create backup before starting
if [ -f "data/tenants.db" ]; then
    echo "💾 Creating backup..."
    BACKUP_FILE="backups/backup_$(date +%Y%m%d_%H%M%S).db"
    cp data/tenants.db "$BACKUP_FILE"
    echo "✅ Backup created: $BACKUP_FILE"
fi

# Check if already running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5000 is already in use"
    echo "Another instance may be running"
    read -p "Kill existing process and continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PID=$(lsof -t -i:5000)
        kill $PID
        sleep 2
        echo "✅ Existing process killed"
    else
        echo "❌ Cannot start - port in use"
        exit 1
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              Starting Application...                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Access the application at:"
echo "   • Local: http://localhost:5000"
echo "   • Network: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
python3 app.py

# Cleanup on exit
echo ""
echo "👋 Application stopped"
