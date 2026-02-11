#!/bin/bash

# Quick Test Runner for Tenant Management System

echo "╔══════════════════════════════════════════════════════════╗"
echo "║    Tenant Management System - Test Runner               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if in correct directory
if [ ! -f "test_suite.py" ]; then
    echo "❌ Error: test_suite.py not found"
    echo "Please run this script from the tenant-management directory"
    exit 1
fi

echo "1️⃣  Running Database Tests..."
echo "─────────────────────────────────────────────────────────"
python3 tenant_model.py
if [ $? -eq 0 ]; then
    echo "✅ Database tests PASSED"
else
    echo "❌ Database tests FAILED"
fi

echo ""
echo "2️⃣  Running QR Code Tests..."
echo "─────────────────────────────────────────────────────────"
python3 qr_generator.py
if [ $? -eq 0 ]; then
    echo "✅ QR code tests PASSED"
else
    echo "❌ QR code tests FAILED"
fi

echo ""
echo "3️⃣  Running Email Tests..."
echo "─────────────────────────────────────────────────────────"
python3 email_notifier.py
if [ $? -eq 0 ]; then
    echo "✅ Email tests PASSED"
else
    echo "❌ Email tests FAILED"
fi

echo ""
echo "4️⃣  Running Complete Test Suite..."
echo "─────────────────────────────────────────────────────────"
python3 test_suite.py
if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║           ✅ ALL TESTS PASSED! ✅                       ║"
    echo "╚══════════════════════════════════════════════════════════╝"
else
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║           ❌ SOME TESTS FAILED ❌                      ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    exit 1
fi

echo ""
echo "Test artifacts created:"
echo "  - data/tenants.db"
echo "  - static/qrcodes/*.png"
echo ""
