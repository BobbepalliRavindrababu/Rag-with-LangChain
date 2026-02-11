# Tenant Management System

A comprehensive web-based system for managing PG (Paying Guest) tenants with features for tracking payments, generating QR codes, and sending email notifications.

## 🌟 Features

### Core Features
- ✅ **Tenant Management**: Add, update, view, and remove tenants
- ✅ **Payment Tracking**: Record payments with transaction numbers and dates
- ✅ **Payment History**: Complete history of all tenant payments
- ✅ **Room Management**: Track room numbers and PG assignments
- ✅ **Email Notifications**: Automated emails for payments, reminders, and announcements
- ✅ **QR Code Generation**: 
  - Onboarding QR for new tenants
  - Checkout QR for departing tenants
  - Tenant-specific QR codes
- ✅ **Dashboard**: Real-time statistics and quick access to tenant information
- ✅ **Search & Filter**: Find tenants quickly by various criteria

### Email Features
- 📧 Welcome emails for new tenants
- 📧 Payment confirmation emails
- 📧 Payment reminder emails
- 📧 Bulk announcement system

### Additional Features
- 📊 Statistics dashboard
- 🔍 Active/inactive tenant filtering
- 📱 Mobile-responsive design
- 🎨 Modern, intuitive UI
- 💾 SQLite database (no external database required)
- 🔒 Soft delete (tenants marked as inactive, not deleted)

## 📋 Tenant Information Tracked

- Name
- Room Number
- PG (Old) - Previous PG if transferred
- PG (New) - Current PG
- Email ID
- Phone Number (optional)
- Transaction Number
- Payment Date (last month)
- Payment History (all months)
- Joining Date
- Status (Active/Inactive)

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or navigate to the directory**:
```bash
cd tenant-management
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Access the application**:
Open your browser and go to: `http://localhost:5000`

## 💻 Usage

### Adding a New Tenant

1. Click on **"➕ Add Tenant"** in the navigation menu
2. Fill in the tenant details:
   - Full Name (required)
   - Room Number (required)
   - Previous PG (optional)
   - Current PG (required)
   - Email Address (required)
   - Phone Number (optional)
   - Joining Date (required)
   - Initial payment details (optional)
3. Click **"💾 Add Tenant"**
4. A welcome email will be sent automatically

### Recording a Payment

1. Go to tenant details page
2. Click **"💰 Add Payment"**
3. Enter payment details:
   - Payment Month
   - Amount
   - Transaction Number
   - Payment Date
   - Notes (optional)
4. Click **"💾 Record Payment"**
5. A payment confirmation email will be sent

### Generating QR Codes

#### Onboarding QR Code (For New Tenants):
1. Click **"📱 Onboarding QR"** in navigation
2. QR code will be displayed
3. Print or share the QR code
4. New tenants can scan to access the registration form

#### Checkout QR Code (For Departing Tenants):
1. Go to tenant details page
2. Click **"📱 Generate Checkout QR"**
3. QR code specific to that tenant will be displayed
4. Scanning this QR marks the tenant as inactive

### Sending Emails

#### Payment Reminders:
1. From the home page
2. Click **"📧 Send Payment Reminders"**
3. All active tenants will receive a reminder email

#### Bulk Announcements:
1. Click **"📧 Send Announcement"** in navigation
2. Enter subject and message
3. Click **"📧 Send to All Tenants"**
4. All active tenants will receive the announcement

### Viewing Tenant Information

1. From home page or tenants list
2. Click **"View"** next to any tenant
3. See complete tenant details including:
   - Personal information
   - Current payment status
   - Complete payment history
   - Checkout QR code

## 📁 Project Structure

```
tenant-management/
│
├── app.py                 # Main Flask application
├── tenant_model.py        # Database models and operations
├── qr_generator.py        # QR code generation
├── email_notifier.py      # Email notification system
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_tenant.html
│   ├── tenant_details.html
│   ├── tenants.html
│   ├── add_payment.html
│   ├── update_tenant.html
│   ├── qr_display.html
│   └── announcement.html
│
├── static/               # Static files
│   ├── css/             # Stylesheets (if any)
│   ├── js/              # JavaScript files (if any)
│   └── qrcodes/         # Generated QR codes
│
└── data/                # Database storage
    └── tenants.db       # SQLite database (auto-created)
```

## 🔧 Configuration

### Email Configuration

To enable real email sending (default is test mode):

Edit `app.py` and update the `EmailNotifier` initialization:

```python
email_notifier = EmailNotifier(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="your-email@gmail.com",
    sender_password="your-app-password"
)
```

**Note**: For Gmail, you need to:
1. Enable 2-factor authentication
2. Create an "App Password" 
3. Use the app password in the configuration

### Database Location

By default, the database is stored in `data/tenants.db`. To change:

Edit `app.py`:
```python
db = TenantDatabase("path/to/your/database.db")
```

## 📊 Database Schema

### Tenants Table
- id (Primary Key)
- name
- room_no
- pg_old
- pg_new
- email (Unique)
- phone
- transaction_number
- payment_date
- joining_date
- is_active (Boolean)
- created_at
- updated_at

### Payment History Table
- id (Primary Key)
- tenant_id (Foreign Key)
- transaction_number
- payment_date
- amount
- payment_month
- notes
- created_at

### Email Logs Table
- id (Primary Key)
- tenant_id (Foreign Key)
- email_to
- subject
- sent_at
- status

## 🎯 API Endpoints

The system also provides REST API endpoints:

- `GET /api/stats` - Get system statistics
- `GET /api/tenants` - Get all tenants (JSON)
- `GET /api/tenant/<id>` - Get specific tenant details (JSON)

Example:
```bash
curl http://localhost:5000/api/stats
```

## 🔐 Security Considerations

1. **Secret Key**: Change the `app.secret_key` in `app.py` for production
2. **Email Credentials**: Never commit email credentials to version control
3. **Database Backup**: Regularly backup the `data/tenants.db` file
4. **HTTPS**: Use HTTPS in production environments
5. **Access Control**: Add authentication for production use

## 🐛 Troubleshooting

### Issue: "No module named 'flask'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: QR codes not displaying
**Solution**: Ensure the `static/qrcodes` directory exists and has write permissions

### Issue: Emails not sending
**Solution**: Check email configuration and ensure SMTP settings are correct

### Issue: Database errors
**Solution**: Delete `data/tenants.db` and restart the application (data will be lost)

## 🚀 Enhancements & Future Features

Potential improvements:
- [ ] User authentication and role-based access
- [ ] SMS notifications
- [ ] Rent amount tracking per tenant
- [ ] Due date reminders (automatic)
- [ ] Expense tracking
- [ ] Receipt generation (PDF)
- [ ] Mobile app
- [ ] WhatsApp integration
- [ ] Multiple PG management
- [ ] Advanced reporting and analytics
- [ ] Export to Excel/CSV
- [ ] Backup and restore functionality

## 📝 Testing

To test the system with sample data:

```bash
# Run tenant_model.py to create test data
python tenant_model.py

# Run qr_generator.py to test QR generation
python qr_generator.py

# Run email_notifier.py to test email system (test mode)
python email_notifier.py
```

## 📄 License

This project is created for educational and practical use. Feel free to modify and use as needed.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

## 🎉 Credits

Built with:
- Flask (Web framework)
- SQLite (Database)
- QRCode library (QR generation)
- Python's built-in email libraries

---

**Happy Tenant Management! 🏠**

Last Updated: February 2026
