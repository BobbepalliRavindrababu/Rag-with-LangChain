"""
Email Notification System for Tenant Management
Sends email notifications for payments, reminders, and announcements
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from typing import List, Dict
import os


class EmailNotifier:
    """Handle email notifications for tenants"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587,
                 sender_email: str = "", sender_password: str = ""):
        """Initialize email notifier"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.test_mode = not sender_email or not sender_password
        
        if self.test_mode:
            print("⚠️  Email notifier in TEST MODE (no actual emails will be sent)")
    
    def send_email(self, to_email: str, subject: str, body: str, html: bool = False) -> bool:
        """Send an email"""
        if self.test_mode:
            print(f"📧 [TEST MODE] Email to: {to_email}")
            print(f"   Subject: {subject}")
            print(f"   Body: {body[:100]}...")
            return True
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_payment_confirmation(self, tenant: Dict, payment_data: Dict) -> bool:
        """Send payment confirmation email"""
        subject = f"Payment Confirmation - {payment_data.get('payment_month')}"
        
        body = f"""
Dear {tenant.get('name')},

Thank you for your payment!

Payment Details:
- Amount: ₹{payment_data.get('amount', 'N/A')}
- Month: {payment_data.get('payment_month')}
- Transaction Number: {payment_data.get('transaction_number')}
- Payment Date: {payment_data.get('payment_date')}
- Room Number: {tenant.get('room_no')}
- PG: {tenant.get('pg_new')}

Your payment has been successfully recorded in our system.

If you have any questions, please contact the management.

Best regards,
PG Management Team
        """
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
        <h2 style="color: #4CAF50;">Payment Confirmation</h2>
        <p>Dear <strong>{tenant.get('name')}</strong>,</p>
        <p>Thank you for your payment!</p>
        
        <div style="background-color: #f9f9f9; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0;">
            <h3 style="margin-top: 0;">Payment Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0;"><strong>Amount:</strong></td>
                    <td style="padding: 8px 0;">₹{payment_data.get('amount', 'N/A')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Month:</strong></td>
                    <td style="padding: 8px 0;">{payment_data.get('payment_month')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Transaction Number:</strong></td>
                    <td style="padding: 8px 0;">{payment_data.get('transaction_number')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Payment Date:</strong></td>
                    <td style="padding: 8px 0;">{payment_data.get('payment_date')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Room Number:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('room_no')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>PG:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('pg_new')}</td>
                </tr>
            </table>
        </div>
        
        <p>Your payment has been successfully recorded in our system.</p>
        <p>If you have any questions, please contact the management.</p>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <p style="margin: 0;">Best regards,</p>
            <p style="margin: 5px 0 0 0;"><strong>PG Management Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(tenant.get('email'), subject, html_body, html=True)
    
    def send_welcome_email(self, tenant: Dict) -> bool:
        """Send welcome email to new tenant"""
        subject = f"Welcome to {tenant.get('pg_new')}!"
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
        <h2 style="color: #2196F3;">Welcome!</h2>
        <p>Dear <strong>{tenant.get('name')}</strong>,</p>
        <p>Welcome to <strong>{tenant.get('pg_new')}</strong>!</p>
        
        <div style="background-color: #e3f2fd; padding: 20px; border-left: 4px solid #2196F3; margin: 20px 0;">
            <h3 style="margin-top: 0;">Your Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0;"><strong>Room Number:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('room_no')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Email:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('email')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Joining Date:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('joining_date', 'N/A')}</td>
                </tr>
            </table>
        </div>
        
        <p>We hope you have a comfortable stay with us. If you need any assistance, please don't hesitate to contact the management.</p>
        
        <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 0;"><strong>Important:</strong> Please make sure to pay your rent on time each month. You will receive a payment confirmation email after each payment.</p>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <p style="margin: 0;">Best regards,</p>
            <p style="margin: 5px 0 0 0;"><strong>PG Management Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(tenant.get('email'), subject, html_body, html=True)
    
    def send_payment_reminder(self, tenant: Dict, month: str) -> bool:
        """Send payment reminder email"""
        subject = f"Payment Reminder - {month}"
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
        <h2 style="color: #FF9800;">Payment Reminder</h2>
        <p>Dear <strong>{tenant.get('name')}</strong>,</p>
        <p>This is a friendly reminder to pay your rent for <strong>{month}</strong>.</p>
        
        <div style="background-color: #fff3e0; padding: 20px; border-left: 4px solid #FF9800; margin: 20px 0;">
            <h3 style="margin-top: 0;">Your Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0;"><strong>Room Number:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('room_no')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>PG:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('pg_new')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0;"><strong>Last Payment:</strong></td>
                    <td style="padding: 8px 0;">{tenant.get('payment_date', 'No payment record')}</td>
                </tr>
            </table>
        </div>
        
        <p>Please make your payment at the earliest and share the transaction details with management.</p>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <p style="margin: 0;">Best regards,</p>
            <p style="margin: 5px 0 0 0;"><strong>PG Management Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(tenant.get('email'), subject, html_body, html=True)
    
    def send_bulk_announcement(self, tenants: List[Dict], subject: str, message: str) -> int:
        """Send bulk announcement to all tenants"""
        sent_count = 0
        
        for tenant in tenants:
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
        <h2 style="color: #2196F3;">Announcement</h2>
        <p>Dear <strong>{tenant.get('name')}</strong>,</p>
        
        <div style="background-color: #f9f9f9; padding: 20px; border-left: 4px solid #2196F3; margin: 20px 0;">
            {message}
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <p style="margin: 0;">Best regards,</p>
            <p style="margin: 5px 0 0 0;"><strong>PG Management Team</strong></p>
        </div>
    </div>
</body>
</html>
            """
            
            if self.send_email(tenant.get('email'), subject, html_body, html=True):
                sent_count += 1
        
        return sent_count


# Test the email notifier
if __name__ == "__main__":
    # Initialize in test mode (no actual emails sent)
    notifier = EmailNotifier()
    
    test_tenant = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'room_no': '101',
        'pg_new': 'Sunrise PG',
        'joining_date': '2026-01-01'
    }
    
    test_payment = {
        'amount': 5000,
        'payment_month': 'February 2026',
        'transaction_number': 'TXN123456',
        'payment_date': '2026-02-01'
    }
    
    # Test welcome email
    print("\nTesting Welcome Email:")
    notifier.send_welcome_email(test_tenant)
    
    # Test payment confirmation
    print("\nTesting Payment Confirmation:")
    notifier.send_payment_confirmation(test_tenant, test_payment)
    
    # Test payment reminder
    print("\nTesting Payment Reminder:")
    notifier.send_payment_reminder(test_tenant, "March 2026")
