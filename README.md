# PWA Restaurant Order Management System

This project is a Progressive Web Application (PWA) for managing restaurant orders, designed with an iOS-style UI/UX and built with modern web technologies. It prioritizes a mobile-first user experience.

## Features

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS v4 (mobile-first)
- **State Management**: Zustand for cart and global data
- **Animations**: Framer Motion for smooth transitions and fluid navigation
- **Components**: Modern, iOS-style components (e.g., TabBar navigation)
- **PWA Optimization**: `manifest.json` and `service-worker.js` for installability and offline capabilities
- **API Connection**: Consumes REST API for product loading
- **Checkout**: Simulated checkout (e.g., via WhatsApp or API)

### Backend (FastAPI)
- **Framework**: FastAPI
- **Database**: MongoDB Atlas integration
- **Authentication**: JWT-protected endpoints (for admin)
- **API Endpoints**: CRUD operations for products, order creation

### PWA Compatibility
- Optimized for PWA Builder for easy deployment to app stores.

## Project Structure

```
pwa-restaurant-app/
├── backend/         # FastAPI backend
├── frontend/        # Next.js frontend
└── README.md        # Project documentation
└── setup.sh         # Automated setup script
```

## Getting Started (Local Installation)

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- npm or yarn
- pip
- MongoDB Atlas account (for database)

### Automated Setup

### Automated Setup

The `setup.sh` (for Linux/macOS) or `setup.ps1` (for Windows PowerShell) script will automate the installation of dependencies and create necessary environment files.

#### For Linux/macOS (Bash)

1.  **Navigate to the project directory:**
    ```bash
    cd pwa-restaurant-app
    ```

2.  **Give execute permissions to the setup script and run it:**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

#### For Windows (PowerShell)

1.  **Open PowerShell as Administrator** (right-click PowerShell icon and select "Run as Administrator").
2.  **Navigate to the project directory:**
    ```powershell
    Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app"
    ```
3.  **Allow script execution (if not already enabled - run once):**
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
4.  **Run the setup script:**
    ```powershell
    .\setup.ps1
    ```

Both scripts will:
- Create a Python virtual environment for the backend and install dependencies.
- Install Node.js dependencies for the frontend.
- Create `.env` (for backend) and `.env.local` (for frontend) files with example content.

### Manual Configuration (Important!)

After running the setup script, you *must* manually edit the environment files with your actual credentials.

#### Backend (`backend/.env`)

Create/edit the `.env` file in the `backend/` directory with your MongoDB Atlas connection string and a strong secret key:

```
MONGO_URI=mongodb+srv://<your_username>:<your_password>@cluster.mongodb.net/your_database_name?retryWrites=true&w=majority
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
```
**Replace `<your_username>`, `<your_password>`, and `your_database_name` with your actual MongoDB Atlas credentials.**

#### Frontend (`frontend/.env.local`)

Create/edit the `.env.local` file in the `frontend/` directory to specify the backend API URL:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Running the Applications

#### For Linux/macOS (Bash)

1.  **Start the Backend (in a new terminal):**
    ```bash
    cd backend
    source venv/bin/activate
    uvicorn main:app --reload --port 8000
    ```

2.  **Start the Frontend (in another new terminal):**
    ```bash
    cd frontend
    npm run dev
    ```

#### For Windows (PowerShell)

1.  **Start the Backend (in a new PowerShell window):**
    ```powershell
    Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app\backend"
    .\venv\Scripts\Activate.ps1
    uvicorn main:app --reload --port 8000
    ```

2.  **Start the Frontend (in another new PowerShell window):**
    ```powershell
    Set-Location -Path "C:\Users\johan\Documents\Proyectos\pwa-restaurant-app\frontend"
    npm run dev
    ```

### Manual Configuration (if needed)

#### Backend (`backend/.env`)

Create a `.env` file in the `backend/` directory with your MongoDB Atlas connection string and a secret key:

```
MONGO_URI=mongodb+srv://<your_username>:<your_password>@cluster.mongodb.net/your_database_name?retryWrites=true&w=majority
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
```
**Replace `<your_username>`, `<your_password>`, and `your_database_name` with your actual MongoDB Atlas credentials.**

#### Frontend (`frontend/.env.local`)

Create a `.env.local` file in the `frontend/` directory to specify the backend API URL:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Running the Applications

1.  **Start the Backend (in a new terminal):**
    ```bash
    cd backend
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    uvicorn main:app --reload --port 8000
    ```
    The backend API will be accessible at `http://localhost:8000`.

2.  **Start the Frontend (in another new terminal):**
    ```bash
    cd frontend
    npm run dev
    ```
    The frontend application will be accessible at `http://localhost:3000`.

## Testing the PWA

1.  Open your browser (preferably Chrome in mobile view) and navigate to `http://localhost:3000`.
2.  Look for the "Add to Home Screen" or "Install app" prompt to install the PWA.
3.  After installation, try disconnecting from the internet to verify offline functionality (products should still be visible if cached).

## Deployment Suggestions

- **Frontend**: Vercel
- **Backend**: Railway or Render
- **Database**: MongoDB Atlas

## PWA Builder Integration

Once your frontend is deployed, you can use [PWA Builder](https://www.pwabuilder.com/) to generate packages for various app stores (Android, Windows, etc.) by providing your deployed frontend URL.

---
Enjoy building your PWA restaurant order management system!
