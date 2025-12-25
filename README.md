# 🚀 Portfolio Backend API

Django REST Framework backend for portfolio website with email notifications and call scheduling.

## ✨ Features

- 📧 **Contact Form API** - Handle contact form submissions
- 📞 **Call Scheduling** - Schedule calls with automatic email notifications
- ⚡ **Async Email** - Celery-based asynchronous email sending
- 🔔 **Reminders** - Automatic call reminders 24 hours before scheduled time
- 🛡️ **CORS Enabled** - Ready for frontend integration
- 📊 **Admin Panel** - Django admin for managing messages and schedules

## 🛠️ Tech Stack

- **Framework:** Django 5.2.8
- **API:** Django REST Framework 3.16.1
- **Task Queue:** Celery 5.5.3
- **Message Broker:** Redis 7.1.0
- **Database:** SQLite (development) / PostgreSQL (production)

## 📦 Installation

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create `.env` file:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=your-admin-email@gmail.com

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 4. Gmail App Password Setup

1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate App Password: https://myaccount.google.com/apppasswords
4. Use the generated password in `EMAIL_HOST_PASSWORD`

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

API will be available at: http://localhost:8000

## 🔧 Redis & Celery Setup

### Install Redis

**Windows:**
```bash
# Download from: https://github.com/microsoftarchive/redis/releases
# Or use WSL/Docker
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### Run Celery Worker

Open a new terminal:

```bash
# Windows
celery -A portfolio_backend worker -l info --pool=solo

# Mac/Linux
celery -A portfolio_backend worker -l info
```

### Run Celery Beat (for scheduled tasks)

Open another terminal:

```bash
celery -A portfolio_backend beat -l info
```

## 📡 API Endpoints

### Contact Form

**POST** `/api/contact/`

Submit a contact message:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "project": "Web Development",
  "message": "I need help with my project..."
}
```

Response:
```json
{
  "success": true,
  "message": "Thank you for your message! I will get back to you soon.",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "project": "Web Development",
    "message": "I need help with my project...",
    "created_at": "2025-01-01T10:00:00Z",
    "is_read": false
  }
}
```

### Call Scheduling

**POST** `/api/schedule-call/`

Schedule a call:

```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "preferred_date": "2025-01-15",
  "preferred_time": "14:00:00",
  "timezone": "EST",
  "topic": "Project Discussion",
  "message": "I'd like to discuss my project requirements..."
}
```

Response:
```json
{
  "success": true,
  "message": "Call scheduled successfully! You will receive a confirmation email shortly.",
  "data": {
    "id": 1,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "preferred_date": "2025-01-15",
    "preferred_time": "14:00:00",
    "timezone": "EST",
    "topic": "Project Discussion",
    "message": "I'd like to discuss my project requirements...",
    "status": "pending",
    "created_at": "2025-01-01T10:00:00Z",
    "is_upcoming": true
  }
}
```

**GET** `/api/schedule-call/upcoming/`

Get all upcoming calls.

## 🎯 Admin Panel

Access admin panel at: http://localhost:8000/admin

Features:
- View and manage contact messages
- View and manage call schedules
- Mark messages as read/unread
- Update call status (pending, confirmed, completed, cancelled)
- Search and filter functionality

## 📧 Email Notifications

### Contact Form Emails

1. **Admin Notification** - Sent to admin email with contact details
2. **User Confirmation** - Sent to user confirming message received

### Call Schedule Emails

1. **Admin Notification** - Sent to admin with call details
2. **User Confirmation** - Sent to user with call details
3. **Reminder Email** - Sent 24 hours before scheduled call (via Celery Beat)

## 🚀 Deployment

### Environment Variables

Set these in production:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Run with Gunicorn

```bash
gunicorn portfolio_backend.wsgi:application --bind 0.0.0.0:8000
```

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to Railway/Render

1. Connect GitHub repository
2. Add environment variables
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn portfolio_backend.wsgi:application`

## 🧪 Testing

### Test Email Configuration

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email.',
    'from@example.com',
    ['to@example.com'],
)
```

### Test Celery

```bash
python manage.py shell
```

```python
from contact.tasks import send_contact_email
result = send_contact_email.delay(1)
print(result.status)
```

## 📝 Project Structure

```
backend/
├── portfolio_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── contact/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py
│   ├── admin.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

## 🐛 Troubleshooting

### Emails Not Sending

1. Check Gmail App Password is correct
2. Verify 2FA is enabled on Google Account
3. Check Celery worker is running
4. Check Redis is running

### Celery Not Working

```bash
# Check Redis connection
redis-cli ping
# Should return: PONG

# Check Celery worker logs
celery -A portfolio_backend worker -l debug
```

### CORS Errors

Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`

## 📞 Support

Need help? Contact:
- LinkedIn: [Shoaib Shoukat](https://www.linkedin.com/in/shoaib-shoukat-722999228/)
- GitHub: [@ShoaibShoukat2](https://github.com/ShoaibShoukat2)

---

Made with 💙 by Shoaib Shoukat
