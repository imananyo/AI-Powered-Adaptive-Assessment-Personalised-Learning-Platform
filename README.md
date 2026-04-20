# AI-Powered-Adaptive-Assessment-Personalised-Learning-Platform
An intelligent backend platform that automates question generation, AI grading, and personalised student recommendations.
STEP 1: Prepare Project Folder

Create a new folder on your laptop:Bashmkdir eduforge-ai
cd eduforge-ai
Copy all the files I gave you earlier (app folder, docker-compose.yml, requirements.txt, alembic, etc.) into this folder.


STEP 2: Create Virtual Environment & Install Packages
Bash# Create virtual environment
python -m venv venv

# Activate it:
# → Mac / Linux
source venv/bin/activate

# → Windows (Command Prompt)
venv\Scripts\activate

# → Windows (PowerShell)
venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements.txt

STEP 3: Create .env File
Create a file named .env in the root folder and paste this:
envAPP_NAME=EduForge AI
ENV=development
DEBUG=True
OPENAI_API_KEY=sk-your-real-openai-key-here

DATABASE_URL=postgresql://user:password@localhost:5432/ai_db
REDIS_URL=redis://localhost:6379

STEP 4: Run the Project (Choose ONE method)
Method A: Easiest – Using Docker (Recommended)
Bashdocker-compose up --build
→ Open browser → http://localhost:8000/docs
To stop:
Bashdocker-compose down

Method B: Run Locally (Without Docker)
Mac & Linux
Bash# 1. Start PostgreSQL & Redis
brew services start postgresql     # Mac
brew services start redis

# Linux
sudo systemctl start postgresql
sudo systemctl start redis-server

# 2. Create database
sudo -u postgres psql -c "CREATE DATABASE ai_db;"
sudo -u postgres psql -c "CREATE USER user WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ai_db TO user;"

# 3. Run migration
alembic upgrade head

# 4. Start Celery (new terminal)
celery -A app.workers.celery_work worker --loglevel=info

# 5. Start FastAPI (another terminal)
uvicorn app.main:app --reload --port 8000
Windows
Bash# 1. Start PostgreSQL & Redis from Services (services.msc)

# 2. Create database using pgAdmin or:
psql -U postgres
CREATE DATABASE ai_db;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE ai_db TO user;
\q

# 3. Run migration
alembic upgrade head

# 4. Start Celery (new terminal)
celery -A app.workers.celery_work worker --loglevel=info

# 5. Start FastAPI (another terminal)
uvicorn app.main:app --reload --port 8000

STEP 5: Push Project to GitHub

Go to github.com → Click New repository
Repository name: eduforge-ai
Description: AI-Powered Adaptive Assessment Platform using FastAPI + OpenAI
Make it Public or Private
Do NOT initialize with README

In your terminal (inside eduforge-ai folder) run:

Bash# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit - EduForge AI complete project"

# Add your GitHub repo

git remote add origin https://github.com/YOUR-USERNAME/eduforge-ai.git

# Push to GitHub
git init
git add .
git commit -m "Initial commit - EduForge AI - Complete AI Assessment Platform"

git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/eduforge-ai.git
git push -u origin main
git branch -M main
git push -u origin main

Final Checklist Before Pushing



#!/bin/bash
# =============================================
#  One-Click Run Script (Mac/Linux)
# =============================================

echo "🚀 Starting EduForge AI..."

# Activate virtual environment
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found! Run: python -m venv venv"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file not found! Please create it first."
    exit 1
fi

echo "🔄 Running database migrations..."
alembic upgrade head

echo ""
echo "Choose how you want to run the project:"
echo "1. Docker (Recommended - Easiest)"
echo "2. Local (Manual - Celery + FastAPI)"
echo "3. Exit"
read -p "Enter your choice (1/2/3): " choice

case $choice in
    1)
        echo "🐳 Starting with Docker..."
        docker-compose up --build
        ;;
    2)
        echo "⚡ Starting Celery Worker in background..."
        celery -A app.workers.celery_work worker --loglevel=info &
        CELERY_PID=$!
        
        echo "🌐 Starting FastAPI Server..."
        echo "📍 API will be available at http://localhost:8000/docs"
        uvicorn app.main:app --reload --port 8000
        
        # Kill Celery when server stops
        kill $CELERY_PID
        ;;
    3)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice!"
        ;;
esac

.env file should NOT be committed (it is already in .gitignore)
All folders have __init__.py
You have tested the app once (docker-compose up or local run)
OpenAI key is in .env (not in code) 


@echo off
:: =============================================
:: One-Click Run Script (Windows)
:: =============================================

echo.
echo 🚀 Starting EduForge AI...
echo.

:: Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo ✅ Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found! Run: python -m venv venv
    pause
    exit /b
)

:: Check for .env file
if not exist .env (
    echo ❌ .env file not found! Please create it first.
    pause
    exit /b
)

echo 🔄 Running database migrations...
alembic upgrade head

echo.
echo Choose how you want to run the project:
echo 1. Docker (Recommended - Easiest)
echo 2. Local (Manual - Celery + FastAPI)
echo 3. Exit
set /p choice="Enter your choice (1/2/3): "

if %choice%==1 (
    echo 🐳 Starting with Docker...
    docker-compose up --build
) else if %choice%==2 (
    echo ⚡ Starting Celery Worker...
    start cmd /k "celery -A app.workers.celery_work worker --loglevel=info"
    
    echo 🌐 Starting FastAPI Server...
    echo 📍 API will be available at http://localhost:8000/docs
    uvicorn app.main:app --reload --port 8000
) else if %choice%==3 (
    echo 👋 Exiting...
) else (
    echo ❌ Invalid choice!
)

pause

How to Use These Files

Copy the run.sh content and save it as run.sh in your project root.
Copy the run.bat content and save it as run.bat in your project root.
Make run.sh executable (Mac/Linux only):

Bashchmod +x run.sh

Run the script:


Mac/Linux: ./run.sh
Windows: Double-click run.bat or run it in Command Prompt. 


#!/bin/bash
# =============================================
# EduForge AI - One-Click Run Script (Mac/Linux)
# =============================================

echo "🚀 EduForge AI - One Click Launcher"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found! Run: python -m venv venv"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file not found! Please create it first."
    exit 1
fi

echo "🔄 Running database migrations..."
alembic upgrade head

echo ""
echo "Select Run Mode:"
echo "1. Docker Mode (Recommended)"
echo "2. Development Mode (Celery + FastAPI in separate windows)"
echo "3. Local Server Only"
echo "4. Exit"
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🐳 Starting with Docker Compose..."
        docker-compose up --build
        ;;
    2)
        echo "⚡ Starting Development Mode..."
        echo "Starting Celery Worker in new terminal..."
        osascript -e 'tell app "Terminal" to do script "cd '"$PWD"' && source venv/bin/activate && celery -A app.workers.celery_work worker --loglevel=info"' &
        
        sleep 3
        echo "🌐 Starting FastAPI Server..."
        echo "📍 Server will be live at http://localhost:8000/docs"
        uvicorn app.main:app --reload --port 8000
        ;;
    3)
        echo "🌐 Starting FastAPI Server Only..."
        uvicorn app.main:app --reload --port 8000
        ;;
    4)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid option!"
        ;;
esac
