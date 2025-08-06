# PowerShell script for PWA Restaurant App setup

# Exit immediately if a command exits with a non-zero status.
$ErrorActionPreference = "Stop"

Write-Host "Starting PWA Restaurant App setup..."

# --- Backend Setup (FastAPI) ---
Write-Host "Setting up backend..."
Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app\backend"

# Create a virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "Installing backend dependencies..."
pip install fastapi uvicorn python-dotenv motor python-jose bcrypt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating backend .env file..."
    @"
MONGO_URI=mongodb+srv://<your_username>:<your_password>@cluster.mongodb.net/your_database_name?retryWrites=true&w=majority
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
"@ | Set-Content -Path ".env"
    Write-Host "Please update backend\.env with your MongoDB Atlas URI and a strong secret key."
}

Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app" # Go back to pwa-restaurant-app root

# --- Frontend Setup (Next.js) ---
Write-Host "Setting up frontend..."
Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app\frontend"

# Install Node.js dependencies
Write-Host "Installing frontend dependencies..."
npm install

# Create .env.local file if it doesn't exist
if (-not (Test-Path ".env.local")) {
    Write-Host "Creating frontend .env.local file..."
    @"
NEXT_PUBLIC_API_URL=http://localhost:8000/api
"@ | Set-Content -Path ".env.local"
    Write-Host "Frontend .env.local created."
}

Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app" # Go back to pwa-restaurant-app root

Write-Host "Setup complete! Follow the instructions below and in README.md to run the applications."
Write-Host "Remember to update your .env files with actual credentials."
