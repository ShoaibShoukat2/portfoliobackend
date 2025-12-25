# 🚀 Backend Setup Guide

Complete step-by-step guide to set up the Django backend.

## 📋 Prerequisites

- Python 3.8+ installed
- pip (Python package manager)
- Redis (for Celery)
- Gmail account (for email notifications)

## 🔧 Step 1: Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

## 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Step 3: Environment Configuration

Create `.env` file in backend folder:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=your-admin-email@gmail.com

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📧 Step 4: Gmail App Password Setup

1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Enable "2-Step Verification" if not already enabled
4. After enabling 2FA, go back to Security
5. Click on "App passwords" (you'll see this only after enabling 2FA)
6. Select "Mail" and "Other (Custom name)"
7. Enter "Portfolio Backend" as the name
8. Click "Generate"
9. Copy the 16-digit password (no spaces)
10. Paste it in `.env` as `EMAIL_HOST_PASSWORD`

**Important:** Never share or commit this password!

## 🗄️ Step 5: Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

## 👤 Step 6: Create Admin User

```bash
python manage.py createsuperuser

# Enter:
# - Username: admin (or your choice)
# - Email: your-email@gmail.com
# - Password: (choose a strong password)
```

## 🚀 Step 7: Run Development Server

```bash
python manage.py runserver
```

Server will start at: http://localhost:8000

Test it by visiting: http://localhost:8000/admin

## 📮 Step 8: Redis Setup (for Celery)

### Windows:

**Option 1: Using WSL (Recommended)**
```bash
# Install WSL if not already installed
wsl --install

# In WSL terminal:
sudo apt-get update
sudo apt-get install redis-server
redis-server
```

**Option 2: Using Docker**
```bash
docker run -d -p 6379:6379 redis:alpine
```

**Option 3: Download Windows Port**
- Download from: https://github.com/microsoftarchive/redis/releases
- Extract and run `redis-server.exe`

### Mac:

```bash
brew install redis
brew services start redis
```

### Linux:

```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### Test Redis:

```bash
redis-cli ping
# Should return: PONG
```

## ⚡ Step 9: Run Celery Worker

Open a **new terminal** (keep Django server running):

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Run Celery worker
# Windows:
celery -A portfolio_backend worker -l info --pool=solo

# Mac/Linux:
celery -A portfolio_backend worker -l info
```

## 🕐 Step 10: Run Celery Beat (Optional - for scheduled tasks)

Open **another new terminal**:

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Run Celery beat
celery -A portfolio_backend beat -l info
```

## ✅ Step 11: Test Everything

### Test 1: Admin Panel
1. Go to: http://localhost:8000/admin
2. Login with superuser credentials
3. You should see "Contact Messages" and "Call Schedules"

### Test 2: API Endpoints
Visit: http://localhost:8000/
You should see API information

### Test 3: Email Configuration
```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email from Django.',
    'your-email@gmail.com',
    ['your-email@gmail.com'],
)
```

Check your email inbox!

### Test 4: Contact Form API

Using curl:
```bash
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "project": "Test Project",
    "message": "This is a test message"
  }'
```

Or use Postman/Insomnia to test the API.

## 🔗 Step 12: Connect Frontend

Update frontend `.env`:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

Restart your React development server.

## 🎯 Running Everything Together

You need **4 terminals**:

**Terminal 1: Django Server**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2: Redis**
```bash
redis-server
```

**Terminal 3: Celery Worker**
```bash
cd backend
venv\Scripts\activate
celery -A portfolio_backend worker -l info --pool=solo
```

**Terminal 4: Frontend (React)**
```bash
cd frontend
npm start
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Issue: "Redis connection refused"
- Make sure Redis is running: `redis-cli ping`
- Check REDIS_URL in `.env`

### Issue: "Email not sending"
- Verify Gmail App Password is correct
- Check 2FA is enabled
- Check Celery worker is running
- Look at Celery worker logs for errors

### Issue: "CORS errors"
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`
- Restart Django server

### Issue: "Database locked"
```bash
python manage.py migrate --run-syncdb
```

## 📊 Monitoring

### View Celery Tasks
```bash
# In Django shell
python manage.py shell

from contact.tasks import send_contact_email
result = send_contact_email.delay(1)
print(result.status)
```

### View Logs
- Django logs: Check terminal running `runserver`
- Celery logs: Check terminal running Celery worker
- Redis logs: Check terminal running Redis

## 🚀 Production Deployment

See `README.md` for production deployment instructions.

## 📞 Need Help?

If you encounter any issues:
1. Check the error message carefully
2. Verify all environment variables are set
3. Ensure all services (Django, Redis, Celery) are running
4. Check the logs for detailed error information

Contact:
- LinkedIn: [Shoaib Shoukat](https://www.linkedin.com/in/shoaib-shoukat-722999228/)
- GitHub: [@ShoaibShoukat2](https://github.com/ShoaibShoukat2)

---

Happy Coding! 💻✨
