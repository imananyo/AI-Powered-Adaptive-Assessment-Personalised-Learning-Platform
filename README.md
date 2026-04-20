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
git branch -M main
git push -u origin main

Final Checklist Before Pushing

.env file should NOT be committed (it is already in .gitignore)
All folders have __init__.py
You have tested the app once (docker-compose up or local run)
OpenAI key is in .env (not in code)
