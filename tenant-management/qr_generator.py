"""
QR Code Generator for Tenant Management
Generates QR codes for tenant onboarding and checkout
"""
import qrcode
import json
import os
from datetime import datetime
from typing import Dict
import base64
from io import BytesIO


class QRCodeGenerator:
    """Generate QR codes for tenant operations"""
    
    def __init__(self, qr_dir: str = "static/qrcodes"):
        """Initialize QR code generator"""
        self.qr_dir = qr_dir
        os.makedirs(qr_dir, exist_ok=True)
    
    def generate_onboarding_qr(self, base_url: str = "http://localhost:5000") -> str:
        """Generate QR code for new tenant onboarding"""
        # Create onboarding URL
        onboarding_data = {
            'type': 'onboarding',
            'url': f"{base_url}/tenant/add",
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(onboarding_data))
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to file
        filename = f"onboarding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.qr_dir, filename)
        img.save(filepath)
        
        print(f"✅ Onboarding QR code generated: {filepath}")
        return filepath
    
    def generate_checkout_qr(self, tenant_id: int, base_url: str = "http://localhost:5000") -> str:
        """Generate QR code for tenant checkout"""
        # Create checkout URL
        checkout_data = {
            'type': 'checkout',
            'tenant_id': tenant_id,
            'url': f"{base_url}/tenant/delete/{tenant_id}",
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(checkout_data))
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="red", back_color="white")
        
        # Save to file
        filename = f"checkout_{tenant_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.qr_dir, filename)
        img.save(filepath)
        
        print(f"✅ Checkout QR code generated: {filepath}")
        return filepath
    
    def generate_tenant_info_qr(self, tenant_data: Dict) -> str:
        """Generate QR code with tenant information"""
        # Create tenant info data
        qr_data = {
            'type': 'tenant_info',
            'data': tenant_data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="blue", back_color="white")
        
        # Save to file
        tenant_id = tenant_data.get('id', 'unknown')
        filename = f"tenant_{tenant_id}_info.png"
        filepath = os.path.join(self.qr_dir, filename)
        img.save(filepath)
        
        return filepath
    
    def generate_payment_qr(self, tenant_id: int, amount: float, month: str, base_url: str = "http://localhost:5000") -> str:
        """Generate QR code for payment"""
        payment_data = {
            'type': 'payment',
            'tenant_id': tenant_id,
            'amount': amount,
            'month': month,
            'url': f"{base_url}/payment/add/{tenant_id}",
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(payment_data))
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="green", back_color="white")
        
        # Save to file
        filename = f"payment_{tenant_id}_{month}.png"
        filepath = os.path.join(self.qr_dir, filename)
        img.save(filepath)
        
        return filepath
    
    def qr_to_base64(self, qr_path: str) -> str:
        """Convert QR code image to base64 string"""
        with open(qr_path, 'rb') as img_file:
            img_data = img_file.read()
            base64_str = base64.b64encode(img_data).decode('utf-8')
            return f"data:image/png;base64,{base64_str}"
    
    def generate_qr_to_base64(self, data: str, color: str = "black") -> str:
        """Generate QR code and return as base64 string"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=color, back_color="white")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}"


# Test the QR code generator
if __name__ == "__main__":
    qr_gen = QRCodeGenerator()
    
    # Generate onboarding QR
    onboarding_qr = qr_gen.generate_onboarding_qr()
    print(f"Onboarding QR: {onboarding_qr}")
    
    # Generate checkout QR
    checkout_qr = qr_gen.generate_checkout_qr(tenant_id=1)
    print(f"Checkout QR: {checkout_qr}")
    
    # Generate tenant info QR
    test_tenant = {
        'id': 1,
        'name': 'John Doe',
        'room_no': '101',
        'email': 'john@example.com'
    }
    info_qr = qr_gen.generate_tenant_info_qr(test_tenant)
    print(f"Tenant Info QR: {info_qr}")
