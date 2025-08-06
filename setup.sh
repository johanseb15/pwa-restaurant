#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting PWA Restaurant App setup..."

# --- Backend Setup (FastAPI) ---
echo "Setting up backend..."
cd backend

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing backend dependencies..."
pip install fastapi uvicorn python-dotenv motor python-jose bcrypt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat << EOF > .env
MONGO_URI=mongodb+srv://<your_username>:<your_password>@cluster.mongodb.net/your_database_name?retryWrites=true&w=majority
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
EOF
    echo "Please update backend/.env with your MongoDB Atlas URI and a strong secret key."
fi

cd .. # Go back to pwa-restaurant-app root

# --- Frontend Setup (Next.js) ---
echo "Setting up frontend..."
cd frontend

# Install Node.js dependencies
echo "Installing frontend dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating frontend .env.local file..."
    cat << EOF > .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF
    echo "Frontend .env.local created."
fi

cd .. # Go back to pwa-restaurant-app root

echo "Setup complete! Follow the instructions in README.md to run the applications."
echo "Remember to update your .env files with actual credentials."
