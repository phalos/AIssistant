# Kyle Assistant

## Project Overview
Kyle is an AI-powered personal assistant inspired by Jarvis from Iron Man. It features conversational AI, screen awareness, audio analysis, long-term memory capabilities, and a user-friendly interface.

## Features (Planned)
- Conversational AI using GPT-4 Turbo
- Screen awareness and analysis using OpenCV
- Audio transcription and processing with Whisper API
- Long-term memory with vector database storage
- Voice customization and synthesis
- User-friendly interface built with React/Electron

## Project Structure
- `/backend` - Python-based API server
- `/frontend` - React/Electron user interface
- `/documentation` - Project documentation and guides

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up environment variables (create a .env file)

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Development Status
This project is currently in Phase 1 (MVP) development. See the planning.txt file for detailed development status. 