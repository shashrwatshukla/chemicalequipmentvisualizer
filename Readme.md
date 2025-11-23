# Chemical Equipment Visualizer

A comprehensive multi-platform application for uploading, analyzing, and visualizing chemical equipment data. Features include CSV data analysis, PDF report generation, statistical metrics, and interactive charts.

**Components:**
- 🖥️ **Desktop App**: PyQt5-based GUI for local analysis
- 🌐 **Web Frontend**: React-based dashboard on Vercel
- ⚙️ **Backend API**: Django REST API on Render

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Desktop App Setup](#desktop-app-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running Locally](#running-locally)
7. [Deployment](#deployment)
8. [Environment Variables](#environment-variables)
9. [Features](#features)
10. [Troubleshooting](#troubleshooting)

---

## 📦 Prerequisites

Before starting, ensure you have installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 20+** - [Download](https://nodejs.org/)
- **pip** - Python package manager (comes with Python)
- **npm** - Node package manager (comes with Node.js)
- **Git** (optional) - For version control

Verify installations:
```bash
python --version    # Should be 3.11 or higher
pip --version
node --version      # Should be 20 or higher
npm --version
```

---

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── desktop/                    # PyQt5 Desktop Application
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── ui/                    # UI components
│   ├── services/              # API client service
│   └── utils/                 # Helper utilities
│
├── backend/                   # Django REST API
│   ├── manage.py              # Django management
│   ├── requirements.txt        # Python dependencies
│   ├── config/                # Django settings
│   │   ├── settings.py        # Main configuration
│   │   ├── urls.py            # URL routing
│   │   ├── wsgi.py            # WSGI config
│   │   └── asgi.py            # ASGI config
│   ├── api/                   # Main API app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data serializers
│   │   ├── urls.py            # API routes
│   │   └── migrations/        # Database migrations
│   └── db.sqlite3             # Local database
│
├── frontend/                  # React Frontend
│   ├── package.json           # Node dependencies
│   ├── public/                # Static files
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   ├── App.js             # Main component
│   │   └── index.js           # Entry point
│   ├── build/                 # Production build
│   ├── .env                   # Local env variables
│   └── .env.production        # Production env variables
│
├── start_servers.sh           # Script to start all servers
└── README.md                  # This file
```

---

## 🖥️ Desktop App Setup

### Step 1: Navigate to Desktop Directory

```bash
cd desktop
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyQt5 (GUI framework)
- requests (HTTP client)
- matplotlib (charting)
- And other required packages

### Step 4: Run the Desktop Application

```bash
python main.py
```

The desktop app will open with:
- Login/Registration interface
- CSV file upload capability
- Data analysis and visualization
- PDF report download
- Dataset management

### Desktop App Features

- **Local Authentication**: Register and login
- **CSV Upload**: Upload equipment data
- **Data Analysis**: Automatic statistical analysis
- **Charts**: Interactive visualizations
- **PDF Reports**: Generate analysis reports
- **Settings**: Change password, delete account

---

## ⚙️ Backend Setup

### Step 1: Navigate to Backend Directory

From project root:
```bash
cd backend
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Key packages installed:
- **Django 4.2.16** - Web framework
- **djangorestframework** - REST API
- **django-cors-headers** - CORS support
- **pandas** - Data analysis
- **matplotlib** - Charts
- **reportlab** - PDF generation
- **psycopg2-binary** - PostgreSQL support
- **gunicorn** - Production server
- **google-api-python-client** - Gmail API

### Step 4: Create Environment Variables File

Create `.env` in the `backend/` directory:

```bash
# On Windows
type nul > .env

# On macOS/Linux
touch .env
```

Add to `.env`:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:5000
DATABASE_URL=sqlite:///./db.sqlite3
```

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

This will:
- Create SQLite database (db.sqlite3)
- Create all necessary tables
- Set up user authentication system

### Step 6: Create Superuser (Optional - for Admin Panel)

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### Step 7: Run Development Server

```bash
python manage.py runserver localhost:8000
```

Backend will be available at: `http://localhost:8000/`

**API Endpoints:**
- `POST /api/login/` - User login
- `POST /api/register/` - User registration
- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/` - List user's datasets
- `GET /api/datasets/{id}/summary/` - Get dataset analysis
- `GET /api/datasets/{id}/report/` - Download PDF report
- `DELETE /api/datasets/{id}/delete/` - Delete dataset

---

## 🌐 Frontend Setup

### Step 1: Navigate to Frontend Directory

From project root:
```bash
cd frontend
```

### Step 2: Install Node.js Dependencies

```bash
npm install
```

This installs React and all required packages:
- React 18.2.0
- react-router-dom (routing)
- axios (HTTP client)
- chart.js (charting)
- react-icons (icons)

### Step 3: Create Environment Variables

Create `.env` in `frontend/` directory:

```bash
# On Windows
type nul > .env

# On macOS/Linux
touch .env
```

Add to `.env`:
```
REACT_APP_API_URL=http://localhost:8000/api
```

### Step 4: Run Development Server

```bash
npm start
```

Frontend will open at: `http://localhost:3000/` or `http://localhost:5000/`

**Features:**
- Dashboard with file upload
- Dataset analysis display
- Statistical charts
- PDF report download
- User authentication
- Settings management

---

## 🚀 Running Locally (All Components)

### Option 1: Manual (Run Each in Separate Terminal)

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Desktop (Optional):**
```bash
cd desktop
python main.py
```

### Option 2: Automated Script (macOS/Linux)

```bash
bash start_servers.sh
```

This starts both backend and frontend automatically.

### Testing the Application

1. **Open browser**: `http://localhost:3000` or `http://localhost:5000`
2. **Register**: Create new account
3. **Upload CSV**: Test with sample data file
4. **Analyze**: View generated statistics
5. **Download**: Get PDF report
6. **Delete**: Remove dataset

---

## 📤 Deployment

### Backend Deployment (Render)

#### Prerequisites:
- PostgreSQL database (Render provides free tier)
- Render account at [render.com](https://render.com)

#### Step 1: Push to GitHub

```bash
git push origin main
```

#### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Select the repository and branch

#### Step 3: Configure Build Settings

- **Build Command:**
  ```
  pip install -r backend/requirements.txt && python backend/manage.py migrate && python backend/manage.py collectstatic --noinput
  ```

- **Start Command:**
  ```
  gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
  ```

#### Step 4: Set Environment Variables

In Render Dashboard → Environment:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

#### Step 5: Deploy

Click "Deploy" - takes 2-5 minutes.

---

### Frontend Deployment (Vercel)

#### Prerequisites:
- Vercel account at [vercel.com](https://vercel.com)

#### Step 1: Push to GitHub

```bash
git push origin main
```

#### Step 2: Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import GitHub repository
4. Select the repository

#### Step 3: Configure Build Settings

- **Framework**: React
- **Build Command**: `npm run build`
- **Install Command**: `npm install`
- **Output Directory**: `build`

#### Step 4: Set Environment Variables

In Vercel Project Settings → Environment Variables:

```
REACT_APP_API_URL=https://your-backend.onrender.com/api
```

**Replace:** `your-backend` with your actual Render service name

#### Step 5: Deploy

Click "Deploy" - takes 1-2 minutes.

---

## 🔐 Environment Variables

### Backend (.env or Render Dashboard)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-random-secret-key` |
| `DEBUG` | Debug mode | `False` (production), `True` (development) |
| `ALLOWED_HOSTS` | Allowed domains | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `https://your-frontend.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted origins | `https://your-frontend.vercel.app` |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host/db` |
| `GOOGLE_OAUTH_CLIENT_ID` | Google OAuth ID | (if using Google auth) |
| `GOOGLE_OAUTH_CLIENT_SECRET` | Google OAuth secret | (if using Google auth) |

### Frontend (.env or Vercel Environment Variables)

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `https://your-backend.onrender.com/api` |

---

## ✨ Features

### Data Upload & Analysis
- ✅ CSV file upload with drag-and-drop
- ✅ Automatic column detection
- ✅ Data validation
- ✅ Equipment categorization

### Statistical Analysis
- ✅ Mean, median, standard deviation
- ✅ Min/max values
- ✅ Quartile analysis
- ✅ Outlier detection
- ✅ Distribution analysis

### Visualization
- ✅ Interactive charts (bar, pie, line)
- ✅ Parameter comparison graphs
- ✅ Equipment distribution charts
- ✅ Trend analysis

### Reports
- ✅ PDF report generation
- ✅ Statistical summaries
- ✅ Chart embedding
- ✅ Professional formatting

### User Management
- ✅ User registration
- ✅ Email verification
- ✅ Password reset
- ✅ Account deletion
- ✅ Session management

### Multi-Platform
- ✅ Web application (React)
- ✅ Desktop application (PyQt5)
- ✅ Mobile responsive

---

## 🐛 Troubleshooting

### Backend Issues

#### Database Errors
```bash
# Reset database (WARNING: Deletes all data)
python manage.py migrate zero api
python manage.py migrate
```

#### Port Already in Use
```bash
# Run on different port
python manage.py runserver localhost:9000
```

#### CORS Errors
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- For Vercel: Must include `https://your-frontend.vercel.app`
- Restart backend after changes

### Frontend Issues

#### Dependencies Not Installing
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

#### API Connection Failed
- Check `REACT_APP_API_URL` in .env
- For Render backend: Use `https://your-backend.onrender.com/api`
- Ensure backend is running
- Check browser console for CORS errors

#### Port 3000/5000 Already in Use
```bash
# Run on different port
PORT=8080 npm start
```

### Upload/Download Issues

#### Upload Fails
1. Check file is CSV format
2. Verify file size < 50MB
3. Check backend logs for errors
4. Ensure database has disk space

#### Download Slow
- Normal for large PDF files
- Generated in real-time on backend
- Can take 10-30 seconds

#### CSRF/403 Errors
- Check `CSRF_TRUSTED_ORIGINS` in backend settings
- For Render + Vercel: Must include Vercel URL
- Clear browser cookies and try again

### Desktop App Issues

#### Login Fails
- Check backend is running
- Verify API URL in `config.py`
- Check network connection

#### Charts Not Displaying
- Ensure data has numeric columns
- Check for missing/invalid values
- Try with different CSV format

---

## 📊 API Documentation

### Authentication

**Register:**
```bash
POST /api/register/
{
  "username": "john",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Login:**
```bash
POST /api/login/
{
  "username": "john",
  "password": "SecurePass123!"
}
```

### Datasets

**Upload CSV:**
```bash
POST /api/upload/
Form Data: file (CSV file)
```

**List Datasets:**
```bash
GET /api/datasets/
```

**Get Dataset Summary:**
```bash
GET /api/datasets/{id}/summary/
```

**Download Report:**
```bash
GET /api/datasets/{id}/report/
```

**Delete Dataset:**
```bash
DELETE /api/datasets/{id}/delete/
```

---

## 📝 CSV Format Requirements

Your CSV file should have columns like:

```
equipment_name,equipment_type,flowrate,pressure,temperature
Pump-01,Centrifugal,150.5,45.2,65.0
Heat-01,Exchanger,200.0,50.0,70.5
...
```

**Required:**
- At least one equipment identifier column
- At least 3 numeric parameters
- No empty cells in numeric columns

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📧 Support

For issues and questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Check backend logs: `backend/` directory
4. Check frontend console: Browser DevTools (F12)

---


**Status:** Production Ready ✅
