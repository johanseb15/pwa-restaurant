## About this Project

This project is a Progressive Web Application (PWA) for a restaurant, built with a Next.js frontend and a FastAPI backend.

## How to Run

To run this project, you need to run the frontend and backend applications in separate terminals.

### Backend

1.  Navigate to the `backend` directory.
2.  Activate the virtual environment: `source venv/bin/activate` (or `.\venv\Scripts\Activate.ps1` on Windows).
3.  Run the development server: `uvicorn main:app --reload --port 8000`.

### Frontend

1.  Navigate to the `frontend` directory.
2.  Install dependencies: `npm install`.
3.  Run the development server: `npm run dev`.

## Coding Style

- **Backend**: Follows standard Python/FastAPI conventions.
- **Frontend**: Follows standard TypeScript/Next.js conventions. Adhere to the existing coding style in the files.
- Use Tailwind CSS for styling.
- Use Zustand for state management.
