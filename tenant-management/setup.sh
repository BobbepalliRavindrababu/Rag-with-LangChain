#!/bin/bash

# Tenant Management System - Quick Start Script

echo "=========================================="
echo "🏠 Tenant Management System Setup"
echo "=========================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "✅ Python $(python3 --version) found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🗄️  Initializing database..."
python3 -c "from tenant_model import TenantDatabase; db = TenantDatabase('data/tenants.db'); print('✅ Database initialized')"

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "  python3 app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "📖 For more information, see README.md"
echo ""
