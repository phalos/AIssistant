@echo off

:: Activate the Python virtual environment
call .venv\Scripts\activate

:: Start the backend server
echo Starting backend server...
start uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload

:: Start the frontend server
echo Starting frontend server...
cd frontend
npm start 