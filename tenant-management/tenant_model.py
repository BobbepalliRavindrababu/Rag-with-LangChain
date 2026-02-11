"""
Tenant Management System - Database Model
Handles all database operations for tenant management
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os


class TenantDatabase:
    """Database handler for tenant management"""
    
    def __init__(self, db_path: str = "data/tenants.db"):
        """Initialize database connection"""
        self.db_path = db_path
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tenants table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                room_no TEXT NOT NULL,
                pg_old TEXT,
                pg_new TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                transaction_number TEXT,
                payment_date TEXT,
                joining_date TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Payment history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER NOT NULL,
                transaction_number TEXT NOT NULL,
                payment_date TEXT NOT NULL,
                amount REAL,
                payment_month TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (tenant_id) REFERENCES tenants (id)
            )
        """)
        
        # Email logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id INTEGER,
                email_to TEXT NOT NULL,
                subject TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (tenant_id) REFERENCES tenants (id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def add_tenant(self, tenant_data: Dict) -> int:
        """Add a new tenant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO tenants (
                name, room_no, pg_old, pg_new, email, phone,
                transaction_number, payment_date, joining_date,
                is_active, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tenant_data.get('name'),
            tenant_data.get('room_no'),
            tenant_data.get('pg_old', ''),
            tenant_data.get('pg_new'),
            tenant_data.get('email'),
            tenant_data.get('phone', ''),
            tenant_data.get('transaction_number', ''),
            tenant_data.get('payment_date', ''),
            tenant_data.get('joining_date', now),
            True,
            now,
            now
        ))
        
        tenant_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Tenant added successfully with ID: {tenant_id}")
        return tenant_id
    
    def get_tenant(self, tenant_id: int) -> Optional[Dict]:
        """Get a tenant by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_tenant_by_email(self, email: str) -> Optional[Dict]:
        """Get a tenant by email"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tenants WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_all_tenants(self, active_only: bool = True) -> List[Dict]:
        """Get all tenants"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute("SELECT * FROM tenants WHERE is_active = 1 ORDER BY room_no")
        else:
            cursor.execute("SELECT * FROM tenants ORDER BY room_no")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_tenant(self, tenant_id: int, update_data: Dict) -> bool:
        """Update tenant information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in update_data.items():
            if key not in ['id', 'created_at']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        fields.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(tenant_id)
        
        query = f"UPDATE tenants SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        return rows_affected > 0
    
    def delete_tenant(self, tenant_id: int) -> bool:
        """Soft delete a tenant (mark as inactive)"""
        return self.update_tenant(tenant_id, {'is_active': False})
    
    def add_payment(self, tenant_id: int, payment_data: Dict) -> int:
        """Add a payment record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO payment_history (
                tenant_id, transaction_number, payment_date,
                amount, payment_month, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tenant_id,
            payment_data.get('transaction_number'),
            payment_data.get('payment_date'),
            payment_data.get('amount'),
            payment_data.get('payment_month'),
            payment_data.get('notes', ''),
            datetime.now().isoformat()
        ))
        
        payment_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        # Update tenant's last payment info (after closing the connection)
        self.update_tenant(tenant_id, {
            'transaction_number': payment_data.get('transaction_number'),
            'payment_date': payment_data.get('payment_date')
        })
        
        return payment_id
    
    def get_payment_history(self, tenant_id: int) -> List[Dict]:
        """Get payment history for a tenant"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM payment_history 
            WHERE tenant_id = ? 
            ORDER BY payment_date DESC
        """, (tenant_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def log_email(self, email_data: Dict):
        """Log an email sent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO email_logs (
                tenant_id, email_to, subject, sent_at, status
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            email_data.get('tenant_id'),
            email_data.get('email_to'),
            email_data.get('subject'),
            datetime.now().isoformat(),
            email_data.get('status', 'sent')
        ))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tenants WHERE is_active = 1")
        active_tenants = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tenants WHERE is_active = 0")
        inactive_tenants = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM payment_history")
        total_payments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT pg_new) FROM tenants WHERE is_active = 1")
        active_pgs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'active_tenants': active_tenants,
            'inactive_tenants': inactive_tenants,
            'total_payments': total_payments,
            'active_pgs': active_pgs
        }


# Test the database
if __name__ == "__main__":
    db = TenantDatabase("data/tenants.db")
    
    # Test adding a tenant
    test_tenant = {
        'name': 'John Doe',
        'room_no': '101',
        'pg_old': '',
        'pg_new': 'Sunrise PG',
        'email': 'john.doe@example.com',
        'phone': '+91-9876543210',
        'transaction_number': 'TXN123456',
        'payment_date': '2026-02-01',
        'joining_date': '2026-01-01'
    }
    
    tenant_id = db.add_tenant(test_tenant)
    print(f"Added tenant with ID: {tenant_id}")
    
    # Get all tenants
    tenants = db.get_all_tenants()
    print(f"\nTotal active tenants: {len(tenants)}")
    
    # Get stats
    stats = db.get_stats()
    print(f"\nDatabase stats: {stats}")
