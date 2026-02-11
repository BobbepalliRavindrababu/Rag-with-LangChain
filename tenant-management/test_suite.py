"""
Comprehensive Test Suite for Tenant Management System
Tests all core modules and integration points
"""
import unittest
import os
import sys
import tempfile
import shutil
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from tenant_model import TenantDatabase
from qr_generator import QRCodeGenerator
from email_notifier import EmailNotifier


class TestTenantDatabase(unittest.TestCase):
    """Test cases for tenant database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        self.db = TenantDatabase(self.test_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db.name):
            os.remove(self.test_db.name)
    
    def test_database_initialization(self):
        """Test database tables are created"""
        # Check that database file exists
        self.assertTrue(os.path.exists(self.test_db.name))
        # Verify by getting stats (will fail if tables don't exist)
        stats = self.db.get_stats()
        self.assertIsNotNone(stats)
        self.assertEqual(stats['active_tenants'], 0)
    
    def test_add_tenant(self):
        """Test adding a tenant"""
        tenant_data = {
            'name': 'Test Tenant',
            'room_no': '101',
            'pg_old': '',
            'pg_new': 'Test PG',
            'email': 'test@example.com',
            'phone': '1234567890',
            'transaction_number': 'TEST123',
            'payment_date': '2026-02-01',
            'joining_date': '2026-01-01'
        }
        
        tenant_id = self.db.add_tenant(tenant_data)
        self.assertIsNotNone(tenant_id)
        self.assertGreater(tenant_id, 0)
        
        # Verify tenant was added
        tenant = self.db.get_tenant(tenant_id)
        self.assertIsNotNone(tenant)
        self.assertEqual(tenant['name'], 'Test Tenant')
        self.assertEqual(tenant['email'], 'test@example.com')
    
    def test_get_tenant_by_email(self):
        """Test retrieving tenant by email"""
        tenant_data = {
            'name': 'Email Test',
            'room_no': '102',
            'pg_new': 'Test PG',
            'email': 'email@example.com'
        }
        
        tenant_id = self.db.add_tenant(tenant_data)
        tenant = self.db.get_tenant_by_email('email@example.com')
        
        self.assertIsNotNone(tenant)
        self.assertEqual(tenant['id'], tenant_id)
        self.assertEqual(tenant['name'], 'Email Test')
    
    def test_get_all_tenants(self):
        """Test getting all tenants"""
        # Add multiple tenants
        for i in range(3):
            self.db.add_tenant({
                'name': f'Tenant {i}',
                'room_no': f'10{i}',
                'pg_new': 'Test PG',
                'email': f'tenant{i}@example.com'
            })
        
        tenants = self.db.get_all_tenants()
        self.assertEqual(len(tenants), 3)
    
    def test_update_tenant(self):
        """Test updating tenant information"""
        tenant_id = self.db.add_tenant({
            'name': 'Original Name',
            'room_no': '103',
            'pg_new': 'Test PG',
            'email': 'update@example.com'
        })
        
        # Update tenant
        success = self.db.update_tenant(tenant_id, {
            'name': 'Updated Name',
            'room_no': '104'
        })
        
        self.assertTrue(success)
        
        # Verify update
        tenant = self.db.get_tenant(tenant_id)
        self.assertEqual(tenant['name'], 'Updated Name')
        self.assertEqual(tenant['room_no'], '104')
    
    def test_delete_tenant(self):
        """Test soft delete (marking tenant as inactive)"""
        tenant_id = self.db.add_tenant({
            'name': 'Delete Test',
            'room_no': '105',
            'pg_new': 'Test PG',
            'email': 'delete@example.com'
        })
        
        # Delete tenant
        success = self.db.delete_tenant(tenant_id)
        self.assertTrue(success)
        
        # Verify tenant is inactive
        tenant = self.db.get_tenant(tenant_id)
        self.assertFalse(tenant['is_active'])
        
        # Verify tenant not in active list
        active_tenants = self.db.get_all_tenants(active_only=True)
        tenant_ids = [t['id'] for t in active_tenants]
        self.assertNotIn(tenant_id, tenant_ids)
    
    def test_add_payment(self):
        """Test adding payment record"""
        tenant_id = self.db.add_tenant({
            'name': 'Payment Test',
            'room_no': '106',
            'pg_new': 'Test PG',
            'email': 'payment@example.com'
        })
        
        payment_data = {
            'transaction_number': 'PAY123',
            'payment_date': '2026-02-01',
            'amount': 5000.00,
            'payment_month': '2026-02',
            'notes': 'Test payment'
        }
        
        payment_id = self.db.add_payment(tenant_id, payment_data)
        self.assertIsNotNone(payment_id)
        self.assertGreater(payment_id, 0)
        
        # Verify payment history
        history = self.db.get_payment_history(tenant_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['amount'], 5000.00)
    
    def test_get_stats(self):
        """Test statistics retrieval"""
        # Add some test data
        self.db.add_tenant({
            'name': 'Stats Test 1',
            'room_no': '107',
            'pg_new': 'PG A',
            'email': 'stats1@example.com'
        })
        
        self.db.add_tenant({
            'name': 'Stats Test 2',
            'room_no': '108',
            'pg_new': 'PG B',
            'email': 'stats2@example.com'
        })
        
        stats = self.db.get_stats()
        self.assertEqual(stats['active_tenants'], 2)
        self.assertEqual(stats['active_pgs'], 2)
    
    def test_log_email(self):
        """Test email logging"""
        tenant_id = self.db.add_tenant({
            'name': 'Email Log Test',
            'room_no': '109',
            'pg_new': 'Test PG',
            'email': 'emaillog@example.com'
        })
        
        self.db.log_email({
            'tenant_id': tenant_id,
            'email_to': 'emaillog@example.com',
            'subject': 'Test Email',
            'status': 'sent'
        })
        
        # Email logging doesn't have a getter, so just verify no exception


class TestQRCodeGenerator(unittest.TestCase):
    """Test cases for QR code generation"""
    
    def setUp(self):
        """Set up test QR directory"""
        self.test_dir = tempfile.mkdtemp()
        self.qr_gen = QRCodeGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_directory_creation(self):
        """Test QR directory is created"""
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_generate_onboarding_qr(self):
        """Test onboarding QR code generation"""
        qr_path = self.qr_gen.generate_onboarding_qr()
        
        self.assertIsNotNone(qr_path)
        self.assertTrue(os.path.exists(qr_path))
        self.assertTrue(qr_path.endswith('.png'))
        
        # Check file size (should be reasonable)
        file_size = os.path.getsize(qr_path)
        self.assertGreater(file_size, 0)
        self.assertLess(file_size, 50000)  # Less than 50KB
    
    def test_generate_checkout_qr(self):
        """Test checkout QR code generation"""
        tenant_id = 123
        qr_path = self.qr_gen.generate_checkout_qr(tenant_id)
        
        self.assertIsNotNone(qr_path)
        self.assertTrue(os.path.exists(qr_path))
        self.assertIn(str(tenant_id), qr_path)
    
    def test_generate_tenant_info_qr(self):
        """Test tenant info QR code generation"""
        tenant_data = {
            'id': 1,
            'name': 'Test Tenant',
            'room_no': '101',
            'email': 'test@example.com'
        }
        
        qr_path = self.qr_gen.generate_tenant_info_qr(tenant_data)
        
        self.assertIsNotNone(qr_path)
        self.assertTrue(os.path.exists(qr_path))
    
    def test_qr_to_base64(self):
        """Test QR code to base64 conversion"""
        qr_path = self.qr_gen.generate_onboarding_qr()
        base64_str = self.qr_gen.qr_to_base64(qr_path)
        
        self.assertIsNotNone(base64_str)
        self.assertTrue(base64_str.startswith('data:image/png;base64,'))
    
    def test_generate_qr_to_base64_direct(self):
        """Test direct QR generation to base64"""
        test_data = "Test QR Data"
        base64_str = self.qr_gen.generate_qr_to_base64(test_data)
        
        self.assertIsNotNone(base64_str)
        self.assertTrue(base64_str.startswith('data:image/png;base64,'))


class TestEmailNotifier(unittest.TestCase):
    """Test cases for email notification system"""
    
    def setUp(self):
        """Set up email notifier in test mode"""
        self.notifier = EmailNotifier()  # Test mode (no credentials)
    
    def test_test_mode_initialization(self):
        """Test that notifier initializes in test mode"""
        self.assertTrue(self.notifier.test_mode)
    
    def test_send_email_test_mode(self):
        """Test sending email in test mode"""
        success = self.notifier.send_email(
            to_email='test@example.com',
            subject='Test Email',
            body='This is a test email'
        )
        
        # In test mode, should always return True
        self.assertTrue(success)
    
    def test_send_welcome_email(self):
        """Test welcome email generation"""
        tenant = {
            'name': 'Test Tenant',
            'email': 'test@example.com',
            'room_no': '101',
            'pg_new': 'Test PG',
            'joining_date': '2026-01-01'
        }
        
        success = self.notifier.send_welcome_email(tenant)
        self.assertTrue(success)
    
    def test_send_payment_confirmation(self):
        """Test payment confirmation email"""
        tenant = {
            'name': 'Test Tenant',
            'email': 'test@example.com',
            'room_no': '101',
            'pg_new': 'Test PG'
        }
        
        payment_data = {
            'amount': 5000,
            'payment_month': 'February 2026',
            'transaction_number': 'TEST123',
            'payment_date': '2026-02-01'
        }
        
        success = self.notifier.send_payment_confirmation(tenant, payment_data)
        self.assertTrue(success)
    
    def test_send_payment_reminder(self):
        """Test payment reminder email"""
        tenant = {
            'name': 'Test Tenant',
            'email': 'test@example.com',
            'room_no': '101',
            'pg_new': 'Test PG',
            'payment_date': '2026-01-01'
        }
        
        success = self.notifier.send_payment_reminder(tenant, 'February 2026')
        self.assertTrue(success)
    
    def test_send_bulk_announcement(self):
        """Test bulk announcement sending"""
        tenants = [
            {'name': 'Tenant 1', 'email': 'tenant1@example.com'},
            {'name': 'Tenant 2', 'email': 'tenant2@example.com'},
            {'name': 'Tenant 3', 'email': 'tenant3@example.com'}
        ]
        
        sent_count = self.notifier.send_bulk_announcement(
            tenants,
            'Test Announcement',
            'This is a test message'
        )
        
        self.assertEqual(sent_count, 3)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db_file.close()
        self.test_qr_dir = tempfile.mkdtemp()
        
        self.db = TenantDatabase(self.test_db_file.name)
        self.qr_gen = QRCodeGenerator(self.test_qr_dir)
        self.notifier = EmailNotifier()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_db_file.name):
            os.remove(self.test_db_file.name)
        if os.path.exists(self.test_qr_dir):
            shutil.rmtree(self.test_qr_dir)
    
    def test_complete_tenant_workflow(self):
        """Test complete tenant onboarding workflow"""
        # 1. Add tenant
        tenant_data = {
            'name': 'Integration Test',
            'room_no': '201',
            'pg_new': 'Integration PG',
            'email': 'integration@example.com'
        }
        
        tenant_id = self.db.add_tenant(tenant_data)
        self.assertIsNotNone(tenant_id)
        
        # 2. Send welcome email
        tenant = self.db.get_tenant(tenant_id)
        success = self.notifier.send_welcome_email(tenant)
        self.assertTrue(success)
        
        # 3. Generate QR codes
        onboarding_qr = self.qr_gen.generate_onboarding_qr()
        checkout_qr = self.qr_gen.generate_checkout_qr(tenant_id)
        
        self.assertTrue(os.path.exists(onboarding_qr))
        self.assertTrue(os.path.exists(checkout_qr))
    
    def test_payment_workflow(self):
        """Test complete payment workflow"""
        # 1. Add tenant
        tenant_id = self.db.add_tenant({
            'name': 'Payment Integration',
            'room_no': '202',
            'pg_new': 'Payment PG',
            'email': 'payment_int@example.com'
        })
        
        # 2. Add payment
        payment_data = {
            'transaction_number': 'INT123',
            'payment_date': '2026-02-01',
            'amount': 5000.00,
            'payment_month': '2026-02'
        }
        
        payment_id = self.db.add_payment(tenant_id, payment_data)
        self.assertIsNotNone(payment_id)
        
        # 3. Send confirmation email
        tenant = self.db.get_tenant(tenant_id)
        success = self.notifier.send_payment_confirmation(tenant, payment_data)
        self.assertTrue(success)
        
        # 4. Verify payment history
        history = self.db.get_payment_history(tenant_id)
        self.assertEqual(len(history), 1)


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTenantDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestQRCodeGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestEmailNotifier))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("TENANT MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 70)
    print()
    
    success = run_tests()
    
    if success:
        print("\n✅ ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED!")
        sys.exit(1)
