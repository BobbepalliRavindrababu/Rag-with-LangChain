"""
Tenant Management System - Web Application
Flask-based web interface for managing PG tenants
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from tenant_model import TenantDatabase
from qr_generator import QRCodeGenerator
from email_notifier import EmailNotifier
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Initialize components
db = TenantDatabase("data/tenants.db")
qr_gen = QRCodeGenerator("static/qrcodes")
email_notifier = EmailNotifier()  # Test mode by default


@app.route('/')
def index():
    """Home page"""
    stats = db.get_stats()
    tenants = db.get_all_tenants()
    return render_template('index.html', stats=stats, tenants=tenants)


@app.route('/tenants')
def list_tenants():
    """List all tenants"""
    active_only = request.args.get('active', 'true').lower() == 'true'
    tenants = db.get_all_tenants(active_only=active_only)
    return render_template('tenants.html', tenants=tenants, active_only=active_only)


@app.route('/tenant/add', methods=['GET', 'POST'])
def add_tenant():
    """Add a new tenant"""
    if request.method == 'POST':
        try:
            tenant_data = {
                'name': request.form['name'],
                'room_no': request.form['room_no'],
                'pg_old': request.form.get('pg_old', ''),
                'pg_new': request.form['pg_new'],
                'email': request.form['email'],
                'phone': request.form.get('phone', ''),
                'transaction_number': request.form.get('transaction_number', ''),
                'payment_date': request.form.get('payment_date', ''),
                'joining_date': request.form.get('joining_date', datetime.now().strftime('%Y-%m-%d'))
            }
            
            tenant_id = db.add_tenant(tenant_data)
            
            # Get tenant details
            tenant = db.get_tenant(tenant_id)
            
            # Send welcome email
            email_notifier.send_welcome_email(tenant)
            
            # Log email
            db.log_email({
                'tenant_id': tenant_id,
                'email_to': tenant['email'],
                'subject': f"Welcome to {tenant['pg_new']}!",
                'status': 'sent'
            })
            
            flash(f'Tenant {tenant_data["name"]} added successfully!', 'success')
            return redirect(url_for('tenant_details', tenant_id=tenant_id))
            
        except Exception as e:
            flash(f'Error adding tenant: {str(e)}', 'error')
            return redirect(url_for('add_tenant'))
    
    return render_template('add_tenant.html')


@app.route('/tenant/<int:tenant_id>')
def tenant_details(tenant_id):
    """View tenant details"""
    tenant = db.get_tenant(tenant_id)
    if not tenant:
        flash('Tenant not found', 'error')
        return redirect(url_for('list_tenants'))
    
    payment_history = db.get_payment_history(tenant_id)
    
    # Generate QR codes
    checkout_qr_path = qr_gen.generate_checkout_qr(tenant_id)
    checkout_qr = qr_gen.qr_to_base64(checkout_qr_path)
    
    return render_template('tenant_details.html', 
                         tenant=tenant, 
                         payment_history=payment_history,
                         checkout_qr=checkout_qr)


@app.route('/tenant/update/<int:tenant_id>', methods=['GET', 'POST'])
def update_tenant(tenant_id):
    """Update tenant information"""
    tenant = db.get_tenant(tenant_id)
    if not tenant:
        flash('Tenant not found', 'error')
        return redirect(url_for('list_tenants'))
    
    if request.method == 'POST':
        try:
            update_data = {
                'name': request.form['name'],
                'room_no': request.form['room_no'],
                'pg_old': request.form.get('pg_old', ''),
                'pg_new': request.form['pg_new'],
                'email': request.form['email'],
                'phone': request.form.get('phone', '')
            }
            
            db.update_tenant(tenant_id, update_data)
            flash('Tenant information updated successfully!', 'success')
            return redirect(url_for('tenant_details', tenant_id=tenant_id))
            
        except Exception as e:
            flash(f'Error updating tenant: {str(e)}', 'error')
    
    return render_template('update_tenant.html', tenant=tenant)


@app.route('/tenant/delete/<int:tenant_id>', methods=['POST', 'GET'])
def delete_tenant(tenant_id):
    """Delete (deactivate) a tenant"""
    tenant = db.get_tenant(tenant_id)
    if not tenant:
        flash('Tenant not found', 'error')
        return redirect(url_for('list_tenants'))
    
    db.delete_tenant(tenant_id)
    flash(f'Tenant {tenant["name"]} has been removed from active list', 'success')
    return redirect(url_for('list_tenants'))


@app.route('/payment/add/<int:tenant_id>', methods=['GET', 'POST'])
def add_payment(tenant_id):
    """Add payment for a tenant"""
    tenant = db.get_tenant(tenant_id)
    if not tenant:
        flash('Tenant not found', 'error')
        return redirect(url_for('list_tenants'))
    
    if request.method == 'POST':
        try:
            payment_data = {
                'transaction_number': request.form['transaction_number'],
                'payment_date': request.form['payment_date'],
                'amount': float(request.form['amount']),
                'payment_month': request.form['payment_month'],
                'notes': request.form.get('notes', '')
            }
            
            payment_id = db.add_payment(tenant_id, payment_data)
            
            # Send payment confirmation email
            email_notifier.send_payment_confirmation(tenant, payment_data)
            
            # Log email
            db.log_email({
                'tenant_id': tenant_id,
                'email_to': tenant['email'],
                'subject': f"Payment Confirmation - {payment_data['payment_month']}",
                'status': 'sent'
            })
            
            flash('Payment recorded successfully!', 'success')
            return redirect(url_for('tenant_details', tenant_id=tenant_id))
            
        except Exception as e:
            flash(f'Error recording payment: {str(e)}', 'error')
    
    return render_template('add_payment.html', tenant=tenant)


@app.route('/qr/onboarding')
def generate_onboarding_qr():
    """Generate onboarding QR code"""
    base_url = request.url_root.rstrip('/')
    qr_path = qr_gen.generate_onboarding_qr(base_url)
    qr_base64 = qr_gen.qr_to_base64(qr_path)
    return render_template('qr_display.html', 
                         qr_code=qr_base64, 
                         qr_type='Onboarding',
                         description='Scan this QR code to add a new tenant')


@app.route('/qr/checkout/<int:tenant_id>')
def generate_checkout_qr(tenant_id):
    """Generate checkout QR code for a specific tenant"""
    tenant = db.get_tenant(tenant_id)
    if not tenant:
        flash('Tenant not found', 'error')
        return redirect(url_for('list_tenants'))
    
    base_url = request.url_root.rstrip('/')
    qr_path = qr_gen.generate_checkout_qr(tenant_id, base_url)
    qr_base64 = qr_gen.qr_to_base64(qr_path)
    return render_template('qr_display.html', 
                         qr_code=qr_base64, 
                         qr_type='Checkout',
                         description=f'Scan to checkout: {tenant["name"]} (Room {tenant["room_no"]})')


@app.route('/emails/send-reminders', methods=['POST'])
def send_reminders():
    """Send payment reminders to all tenants"""
    tenants = db.get_all_tenants()
    month = request.form.get('month', datetime.now().strftime('%B %Y'))
    
    sent_count = 0
    for tenant in tenants:
        if email_notifier.send_payment_reminder(tenant, month):
            sent_count += 1
            db.log_email({
                'tenant_id': tenant['id'],
                'email_to': tenant['email'],
                'subject': f"Payment Reminder - {month}",
                'status': 'sent'
            })
    
    flash(f'Payment reminders sent to {sent_count} tenants', 'success')
    return redirect(url_for('index'))


@app.route('/emails/announcement', methods=['GET', 'POST'])
def send_announcement():
    """Send bulk announcement to all tenants"""
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        
        tenants = db.get_all_tenants()
        sent_count = email_notifier.send_bulk_announcement(tenants, subject, message)
        
        for tenant in tenants:
            db.log_email({
                'tenant_id': tenant['id'],
                'email_to': tenant['email'],
                'subject': subject,
                'status': 'sent'
            })
        
        flash(f'Announcement sent to {sent_count} tenants', 'success')
        return redirect(url_for('index'))
    
    tenants = db.get_all_tenants()
    return render_template('announcement.html', tenant_count=len(tenants))


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = db.get_stats()
    return jsonify(stats)


@app.route('/api/tenants')
def api_tenants():
    """API endpoint for tenant list"""
    active_only = request.args.get('active', 'true').lower() == 'true'
    tenants = db.get_all_tenants(active_only=active_only)
    return jsonify(tenants)


@app.route('/api/tenant/<int:tenant_id>')
def api_tenant(tenant_id):
    """API endpoint for tenant details"""
    tenant = db.get_tenant(tenant_id)
    if tenant:
        return jsonify(tenant)
    return jsonify({'error': 'Tenant not found'}), 404


if __name__ == '__main__':
    print("=" * 60)
    print("🏠 Tenant Management System")
    print("=" * 60)
    print("\n📊 Database initialized")
    print(f"📍 Server starting at http://localhost:5000")
    print("\n🎯 Features:")
    print("  • Tenant management (add, update, delete)")
    print("  • Payment tracking")
    print("  • QR code generation for onboarding/checkout")
    print("  • Email notifications")
    print("  • Payment reminders")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
