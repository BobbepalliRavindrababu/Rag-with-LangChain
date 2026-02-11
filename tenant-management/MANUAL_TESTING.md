# Manual Testing Checklist

## Pre-requisites
- [ ] Python 3.7+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Application running (`python app.py`)
- [ ] Browser open to `http://localhost:5000`

## 1. Homepage/Dashboard Testing

### Test 1.1: Access Homepage
- [ ] Navigate to `http://localhost:5000`
- [ ] Verify page loads without errors
- [ ] Check that dashboard displays with statistics
- [ ] Verify navigation menu is visible
- [ ] Check responsive design (resize browser window)

**Expected Results:**
- Homepage loads successfully
- Statistics show: Active Tenants, Active PGs, Total Payments, Past Tenants
- Navigation menu shows: Home, Tenants, Add Tenant, Onboarding QR, Send Announcement

### Test 1.2: Dashboard Statistics
- [ ] Verify "Active Tenants" count is accurate
- [ ] Check "Active PGs" count
- [ ] Confirm "Total Payments" count
- [ ] Validate "Past Tenants" count

## 2. Add Tenant Functionality

### Test 2.1: Access Add Tenant Form
- [ ] Click "Add Tenant" in navigation
- [ ] Verify form loads with all fields
- [ ] Check all required fields are marked with *

**Expected Fields:**
- Full Name *
- Room Number *
- Previous PG (optional)
- Current PG *
- Email Address *
- Phone Number (optional)
- Joining Date *
- Initial Transaction Number (optional)
- Initial Payment Date (optional)

### Test 2.2: Add New Tenant (Valid Data)
- [ ] Fill in all required fields:
  - Name: "Test Tenant 1"
  - Room No: "101"
  - Current PG: "Test PG"
  - Email: "test1@example.com"
  - Joining Date: Today's date
- [ ] Click "Add Tenant" button
- [ ] Verify success message appears
- [ ] Verify redirected to tenant details page
- [ ] Check welcome email log (if configured)

### Test 2.3: Add Tenant (Missing Required Field)
- [ ] Leave "Name" field empty
- [ ] Try to submit form
- [ ] Verify browser validation prevents submission
- [ ] Fill in "Name", leave "Email" empty
- [ ] Try to submit form
- [ ] Verify validation error

### Test 2.4: Add Tenant (Duplicate Email)
- [ ] Try to add tenant with existing email
- [ ] Verify appropriate error message
- [ ] Confirm tenant is not duplicated

## 3. View Tenants

### Test 3.1: View All Tenants List
- [ ] Click "Tenants" in navigation
- [ ] Verify all tenants are displayed
- [ ] Check table columns: ID, Name, Room No, PG, Email, Phone, Last Payment, Status, Actions

### Test 3.2: Filter Active Tenants
- [ ] Click "Active Tenants" button
- [ ] Verify only active tenants are shown
- [ ] Confirm inactive tenants are hidden

### Test 3.3: Filter All Tenants
- [ ] Click "All Tenants" button
- [ ] Verify both active and inactive tenants are shown
- [ ] Check that status column shows correctly

## 4. View Tenant Details

### Test 4.1: Access Tenant Details
- [ ] From tenants list, click "View" for a tenant
- [ ] Verify tenant details page loads
- [ ] Check all information is displayed correctly:
  - Name
  - Room Number
  - Current PG
  - Previous PG (if any)
  - Email
  - Phone
  - Joining Date
  - Last Payment Date
  - Last Transaction Number
  - Status

### Test 4.2: View Payment History
- [ ] Scroll to "Payment History" section
- [ ] Verify payment records are displayed
- [ ] Check columns: Payment Month, Amount, Transaction Number, Payment Date, Notes

### Test 4.3: View Checkout QR Code
- [ ] Scroll to "Checkout QR Code" section
- [ ] Verify QR code is displayed
- [ ] Check QR code is scannable (use phone camera)

## 5. Update Tenant Information

### Test 5.1: Access Update Form
- [ ] From tenant details page, click "Edit Details"
- [ ] Verify update form loads with current data pre-filled

### Test 5.2: Update Tenant
- [ ] Change "Name" to "Updated Name"
- [ ] Change "Room No" to "102"
- [ ] Click "Update Tenant"
- [ ] Verify success message
- [ ] Confirm changes are saved
- [ ] Verify redirect to tenant details page

## 6. Payment Management

### Test 6.1: Add Payment
- [ ] From tenant details, click "Add Payment"
- [ ] Fill in payment details:
  - Payment Month: Current month
  - Amount: 5000
  - Transaction Number: "TEST123"
  - Payment Date: Today's date
  - Notes: "Test payment"
- [ ] Click "Record Payment"
- [ ] Verify success message
- [ ] Check payment appears in history
- [ ] Verify tenant's last payment info updated
- [ ] Check email confirmation log

### Test 6.2: View Payment History
- [ ] From tenant details, scroll to payment history
- [ ] Verify all payments are listed
- [ ] Check most recent payment is at top
- [ ] Confirm all payment details are correct

## 7. QR Code Generation

### Test 7.1: Generate Onboarding QR
- [ ] Click "Onboarding QR" in navigation
- [ ] Verify QR code is displayed
- [ ] Check description text is present
- [ ] Click "Print QR Code" button
- [ ] Verify print dialog opens

### Test 7.2: Scan Onboarding QR
- [ ] Use phone camera to scan onboarding QR
- [ ] Verify URL is readable (should contain /tenant/add)
- [ ] Test scanning with QR reader app

### Test 7.3: Generate Checkout QR
- [ ] From tenant details, click "Generate Checkout QR"
- [ ] Verify checkout QR is displayed
- [ ] Check tenant name is shown in description
- [ ] Scan QR to verify URL (should contain /tenant/delete/{id})

## 8. Email Notifications

### Test 8.1: Send Payment Reminders
- [ ] From homepage, click "Send Payment Reminders"
- [ ] Verify confirmation message
- [ ] Check email logs (in database or test mode output)

### Test 8.2: Send Bulk Announcement
- [ ] Click "Send Announcement" in navigation
- [ ] Verify announcement form loads
- [ ] Enter subject: "Test Announcement"
- [ ] Enter message: "This is a test message"
- [ ] Click "Send to All Tenants"
- [ ] Confirm with OK in dialog
- [ ] Verify success message with count
- [ ] Check email logs

## 9. Delete/Remove Tenant

### Test 9.1: Remove Tenant
- [ ] From tenant details, click "Remove Tenant"
- [ ] Verify confirmation dialog appears
- [ ] Click OK to confirm
- [ ] Verify success message
- [ ] Check tenant is marked as inactive
- [ ] Verify tenant no longer in active list
- [ ] Confirm tenant still in "All Tenants" list with inactive status

### Test 9.2: Verify Soft Delete
- [ ] View "All Tenants"
- [ ] Find the removed tenant
- [ ] Verify status shows "Inactive"
- [ ] Confirm tenant data is preserved
- [ ] Check payment history is still accessible

## 10. Navigation Testing

### Test 10.1: Menu Navigation
- [ ] Click each menu item:
  - [ ] Home
  - [ ] Tenants
  - [ ] Add Tenant
  - [ ] Onboarding QR
  - [ ] Send Announcement
- [ ] Verify each page loads correctly
- [ ] Check no broken links

### Test 10.2: Breadcrumb Navigation
- [ ] Navigate through tenant workflow
- [ ] Use "Back" button to return
- [ ] Verify history works correctly

## 11. Error Handling

### Test 11.1: Invalid URLs
- [ ] Try to access `/tenant/9999` (non-existent tenant)
- [ ] Verify error message or redirect
- [ ] Check application doesn't crash

### Test 11.2: Invalid Form Data
- [ ] Try to enter invalid email format
- [ ] Submit form with negative payment amount
- [ ] Enter text in numeric fields
- [ ] Verify validation errors

## 12. UI/UX Testing

### Test 12.1: Visual Consistency
- [ ] Check all pages have consistent header
- [ ] Verify navigation menu is always visible
- [ ] Confirm footer appears on all pages
- [ ] Check color scheme is consistent

### Test 12.2: Responsive Design
- [ ] Resize browser to mobile width (320px)
- [ ] Verify layout adjusts appropriately
- [ ] Test on tablet width (768px)
- [ ] Check desktop view (1920px)

### Test 12.3: Button Functionality
- [ ] Verify all buttons have hover effects
- [ ] Check button text is readable
- [ ] Confirm buttons respond to clicks
- [ ] Test button states (active, disabled)

## 13. Data Validation

### Test 13.1: Email Validation
- [ ] Try invalid email formats:
  - [ ] "notanemail"
  - [ ] "missing@domain"
  - [ ] "@example.com"
- [ ] Verify validation errors

### Test 13.2: Date Validation
- [ ] Try future dates where inappropriate
- [ ] Enter invalid date formats
- [ ] Verify proper validation

### Test 13.3: Numeric Validation
- [ ] Enter negative numbers for amount
- [ ] Try decimal values with too many places
- [ ] Enter text in numeric fields
- [ ] Verify validation

## 14. Performance Testing

### Test 14.1: Page Load Time
- [ ] Measure homepage load time (should be < 2s)
- [ ] Check tenant list load with 100+ tenants
- [ ] Verify QR generation time

### Test 14.2: Database Operations
- [ ] Add 10 tenants quickly
- [ ] Verify no delays or errors
- [ ] Check database file size growth

## 15. Security Testing

### Test 15.1: SQL Injection
- [ ] Try entering SQL in form fields:
  - `' OR '1'='1`
  - `'; DROP TABLE tenants; --`
- [ ] Verify system handles safely

### Test 15.2: XSS Testing
- [ ] Try entering HTML/JS in fields:
  - `<script>alert('XSS')</script>`
  - `<img src=x onerror=alert('XSS')>`
- [ ] Verify output is escaped

## Testing Summary

### Statistics
- Total Test Cases: ____ 
- Passed: ____
- Failed: ____
- Blocked: ____

### Issues Found
1. _______________
2. _______________
3. _______________

### Notes
- _______________
- _______________
- _______________

### Sign-off
- Tester Name: ______________
- Date: ______________
- Signature: ______________

---

## Quick Test (5 Minutes)

For a quick sanity check, perform these essential tests:

1. [ ] Access homepage
2. [ ] Add a new tenant
3. [ ] View tenant details
4. [ ] Add a payment
5. [ ] Generate onboarding QR
6. [ ] Remove the tenant

If all these pass, the system is likely working correctly.
