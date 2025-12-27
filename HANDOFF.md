# 📱 Admin Mobile App – Backend API Handoff

## Project Overview
This backend supports an Admin Mobile App for managing snack orders and UPI payments.

Admins can:
- View incoming orders
- Verify UPI payments
- Approve payments
- Manage menu items
- Switch UPI accounts
- Receive push notifications when a user submits payment

Backend implementation is complete and stable.

## 🔐 Authentication

### Admin Login
POST /api/admin/login/

Request
{
  "username": "admin_username",
  "password": "admin_password"
}

Response
{
  "token": "AUTH_TOKEN"
}

All subsequent requests must include:
Authorization: Token AUTH_TOKEN

## 📦 Orders APIs

### List Orders (Admin Home Screen)
GET /api/admin/orders/

Response
[
  {
    "id": 33,
    "lab_name": "CCL",
    "system_number": "12",
    "total_amount": "20.00",
    "status": "Pending",
    "created_at": "2025-01-10T10:30:00Z"
  }
]

### Order Detail (Tap on Order)
GET /api/admin/orders/<order_id>/

Response
{
  "id": 33,
  "lab_name": "CCL",
  "system_number": "12",
  "total_amount": "20.00",
  "status": "Pending",
  "payment_status": "PENDING_VERIFICATION",
  "items": [
    {
      "name": "Chicken Puffs",
      "quantity": 1,
      "price": "20.00"
    }
  ]
}

Payment Status Values
CREATED – user has not paid
PENDING_VERIFICATION – user clicked "I have paid"
PAID – admin approved payment

### Approve Payment (Admin Action)
POST /api/admin/orders/<order_id>/approve-payment/

Response
{
  "status": "PAID"
}

This marks payment as PAID and order as Completed.

## 🍔 Menu Management APIs

### List Menu Items
GET /api/admin/menu/

Response
[
  {
    "id": 1,
    "name": "Lays",
    "price": 20,
    "stock": 10,
    "is_available": true
  }
]

### Update Menu Item
PATCH /api/admin/menu/<item_id>/

Request
{
  "price": 25,
  "stock": 8,
  "is_available": true
}

## 💳 UPI Management APIs

### List / Create UPI Accounts
GET /api/admin/upi/
POST /api/admin/upi/

Create Request
{
  "upi_id": "canteen@upi",
  "qr_code": "<image>"
}

### Activate UPI Account
PATCH /api/admin/upi/<upi_id>/activate/

Only one UPI account is active at a time.

## 🔔 Push Notifications

Notification is sent ONLY when:
User clicks "I have paid"
(payment_status becomes PENDING_VERIFICATION)

Notifications are not sent on order creation.

Notification Payload (Firebase)
{
  "notification": {
    "title": "Payment Submitted",
    "body": "Order #33 | Lab CCL | ₹20"
  },
  "data": {
    "order_id": "33",
    "event": "PAYMENT_PENDING"
  }
}

App Behavior
- Notification arrives even if app is closed
- On tap, open Order Detail screen using order_id

## 📱 Device Registration for Push

Register Device (After Login)
POST /api/admin/register-device/

Request
{
  "device_token": "FCM_DEVICE_TOKEN",
  "platform": "android"
}

Unregister Device (On Logout)
POST /api/admin/unregister-device/

Request
{
  "device_token": "FCM_DEVICE_TOKEN"
}

## 🔥 Firebase Responsibility Split

Backend
- Firebase Admin SDK initialized
- Sends push notifications
- Stores admin device tokens

Mobile App
- Firebase Android SDK setup
- Obtain FCM device token
- Call register/unregister APIs
- Handle notification UI and navigation

## ⚠️ Important Notes
- Token authentication is mandatory
- All admin APIs require admin/staff account
- Push payload always includes order_id
- Backend does not require polling for alerts

## ✅ Backend Status
- Complete
- Tested
- Production-ready
- No further backend changes required

End of document
