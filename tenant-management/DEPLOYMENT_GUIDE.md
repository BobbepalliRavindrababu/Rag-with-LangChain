# 🚀 Production Deployment Guide

## Overview

This guide helps you deploy the Tenant Management System for real-time production use in your PG (Paying Guest) accommodation.

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Python 3.7 or higher installed
- [ ] Access to a computer that can run 24/7 (optional but recommended)
- [ ] Gmail account (for email notifications - optional)
- [ ] Basic understanding of running Python applications

---

## 🏗️ Deployment Options

### Option 1: Local Computer (Easiest)
**Best for:** Small PGs (1-50 tenants), personal use  
**Cost:** Free  
**Uptime:** When your computer is on  

### Option 2: Local Server/Raspberry Pi
**Best for:** Medium PGs (50-200 tenants), 24/7 access  
**Cost:** ~$50-200 (one-time hardware)  
**Uptime:** 24/7  

### Option 3: Cloud Hosting (VPS)
**Best for:** Large PGs (200+ tenants), internet access  
**Cost:** $5-20/month  
**Uptime:** 24/7 from anywhere  

---

## 📋 Option 1: Local Computer Deployment

### Step 1: System Requirements

**Minimum:**
- CPU: Any modern processor
- RAM: 2 GB
- Storage: 100 MB
- OS: Windows 7+, macOS 10.12+, Ubuntu 16.04+

**Recommended:**
- CPU: Dual-core 2.0 GHz+
- RAM: 4 GB
- Storage: 500 MB
- OS: Windows 10, macOS 12+, Ubuntu 20.04+

### Step 2: Install Python

**Windows:**
1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python3

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

Verify installation:
```bash
python3 --version
```

### Step 3: Download/Extract Project

If you have the code:
```bash
cd path/to/tenant-management
```

If using git:
```bash
git clone <repository-url>
cd Rag-with-LangChain/tenant-management
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If you get permission errors:
```bash
pip install --user -r requirements.txt
```

Or:
```bash
pip3 install -r requirements.txt
```

### Step 5: Configure Application

**5.1 Change Secret Key**

Edit `app.py`, find line ~13:
```python
app.secret_key = 'your-secret-key-here-change-in-production'
```

Generate a random key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as your secret key.

**5.2 Configure Email (Optional)**

Edit `app.py`, find line ~15:
```python
email_notifier = EmailNotifier()  # Test mode
```

Change to:
```python
email_notifier = EmailNotifier(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="your-email@gmail.com",
    sender_password="your-app-password"
)
```

**Getting Gmail App Password:**
1. Enable 2-Factor Authentication: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords
3. Select "Mail" → "Other (Custom name)"
4. Copy the 16-character password

### Step 6: Test Installation

```bash
python app.py
```

You should see:
```
🏠 Tenant Management System
============================================================
📊 Database initialized
📍 Server starting at http://localhost:5000
```

Open browser: http://localhost:5000

**✅ If you see the dashboard, installation is successful!**

### Step 7: Create First Tenant (Test)

1. Click "Add Tenant"
2. Fill in test data
3. Click "Add Tenant"
4. Verify tenant appears in list

**✅ System is working!**

---

## 🌐 Option 2: Network Access (Same WiFi)

Make the application accessible from any device on your local network.

### Step 1: Find Your Computer's IP

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your active connection (e.g., 192.168.1.100)

**Mac/Linux:**
```bash
ifconfig
# or
hostname -I
```

### Step 2: Configure App for Network Access

Edit `app.py`, change the last line (around line 378):

**Before:**
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

**After:**
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Note: Changed `debug=True` to `debug=False` for production.

### Step 3: Configure Firewall

**Windows:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Click "Change settings"
4. Click "Allow another app"
5. Browse to Python executable
6. Allow "Private" network

**Mac:**
```bash
# Firewall should allow by default
# If blocked, go to System Preferences → Security → Firewall Options
```

**Linux:**
```bash
sudo ufw allow 5000/tcp
# or
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
```

### Step 4: Start Application

```bash
python app.py
```

### Step 5: Access from Other Devices

On any device on the same WiFi:
```
http://YOUR_IP:5000

Example: http://192.168.1.100:5000
```

**✅ Now accessible from phones, tablets, other computers!**

---

## 🔒 Production Security Setup

### 1. Change Default Settings

**Secret Key:** (MUST DO)
```python
# In app.py
app.secret_key = 'CHANGE-THIS-TO-RANDOM-STRING-67890'
```

Generate secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Disable Debug Mode

In `app.py`, change:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### 3. Set Up Regular Backups

**Create backup script (backup.sh):**
```bash
#!/bin/bash
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR
cp data/tenants.db "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).db"
echo "Backup created"
```

**Make executable:**
```bash
chmod +x backup.sh
```

**Run daily with cron (Linux/Mac):**
```bash
crontab -e
# Add this line:
0 2 * * * /path/to/tenant-management/backup.sh
```

**Windows Task Scheduler:**
Create `backup.bat`:
```batch
@echo off
set BACKUP_DIR=backups
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%
copy data\tenants.db "%BACKUP_DIR%\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db"
echo Backup created
```

Schedule in Task Scheduler to run daily.

### 4. Secure Email Credentials

**Option A: Environment Variables**

Create `.env` file:
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Update `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
email_notifier = EmailNotifier(
    smtp_server=os.getenv('SMTP_SERVER'),
    smtp_port=int(os.getenv('SMTP_PORT')),
    sender_email=os.getenv('SENDER_EMAIL'),
    sender_password=os.getenv('SENDER_PASSWORD')
)
```

Add `.env` to `.gitignore`!

### 5. Access Control

For multi-user access, consider adding basic authentication:

```bash
pip install Flask-HTTPAuth
```

Add to `app.py`:
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "your-password-here"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Add @auth.login_required to routes
@app.route('/')
@auth.login_required
def index():
    # ...
```

---

## 🚀 Running as a Service (24/7)

### Linux (systemd)

Create `/etc/systemd/system/tenant-mgmt.service`:
```ini
[Unit]
Description=Tenant Management System
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/tenant-management
ExecStart=/usr/bin/python3 /path/to/tenant-management/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable tenant-mgmt
sudo systemctl start tenant-mgmt
sudo systemctl status tenant-mgmt
```

### Windows (NSSM)

1. Download NSSM: https://nssm.cc/download
2. Run as administrator:
```cmd
nssm install TenantManagement
```
3. Configure:
   - Path: C:\Python39\python.exe
   - Startup directory: C:\path\to\tenant-management
   - Arguments: app.py
4. Start service:
```cmd
nssm start TenantManagement
```

### macOS (launchd)

Create `~/Library/LaunchAgents/com.tenantmgmt.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.tenantmgmt</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/tenant-management/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.tenantmgmt.plist
```

---

## 🌍 Option 3: Cloud Deployment

### Using PythonAnywhere (Easiest Cloud)

1. Sign up: https://www.pythonanywhere.com (Free tier available)
2. Upload files via Files tab
3. Create web app → Flask → Python 3.9
4. Configure WSGI file
5. Reload web app

**Cost:** Free for 1 app, $5/month for custom domain

### Using DigitalOcean/AWS/Heroku

See respective cloud provider documentation for Flask deployment.

---

## 📊 Monitoring and Maintenance

### Daily Tasks
- [ ] Check application is running
- [ ] Verify new tenant additions
- [ ] Monitor payment recordings

### Weekly Tasks
- [ ] Review database size
- [ ] Check backup creation
- [ ] Test QR code generation

### Monthly Tasks
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Archive old backups
- [ ] Review inactive tenants

---

## 🆘 Troubleshooting

### Application Won't Start

**Error: "Address already in use"**
```bash
# Find process using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
python app.py --port=5001
```

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

### Can't Access from Network

1. Verify firewall allows port 5000
2. Check `host='0.0.0.0'` in app.py
3. Confirm IP address is correct
4. Try accessing from same computer first: http://localhost:5000

### Email Not Sending

1. Check email credentials in app.py
2. Verify Gmail App Password is correct
3. Check internet connection
4. Look for error messages in console

### Database Issues

**"Database is locked"**
- Only one instance should be running
- Restart application

**"Database corrupted"**
- Restore from backup
- Check disk space

---

## 📈 Scaling Guidelines

### 1-50 Tenants
- Any computer works
- Local deployment fine
- Backups: Daily

### 50-200 Tenants
- Dedicated computer recommended
- Consider 24/7 operation
- Backups: Daily + Weekly archives

### 200+ Tenants
- Consider cloud hosting
- Use PostgreSQL instead of SQLite
- Professional backup solution
- Load balancing if needed

---

## ✅ Production Readiness Checklist

Before going live:

- [ ] Changed secret key
- [ ] Disabled debug mode
- [ ] Configured email (if using)
- [ ] Set up backups
- [ ] Tested on local network
- [ ] Created first test tenant
- [ ] Recorded test payment
- [ ] Generated QR codes
- [ ] Verified all features work
- [ ] Documented admin credentials
- [ ] Trained staff on usage

---

## 🎉 You're Ready for Production!

The system is tested, secure, and ready for real-time use.

**Start now:**
```bash
cd tenant-management
python app.py
```

**Access at:** http://localhost:5000

**Need help?** Check other documentation files or refer to the troubleshooting section.
