from fastapi import FastAPI, HTTPException, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from dotenv import load_dotenv
from .utils.memory import MemoryManager
from .api.response import ResponseRequest

# Import routers
from .api.audio import router as audio_router
from .api.screen import router as screen_router
from .api.response import router as response_router
from .utils.config import API_HOST, API_PORT, DEBUG, LOG_LEVEL, validate_config

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate configuration
validate_config()

# Initialize FastAPI app
app = FastAPI(title="Kyle Assistant API", 
              description="Backend API for Kyle AI Assistant",
              version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(audio_router, tags=["Audio"])
app.include_router(screen_router, tags=["Screen"])
app.include_router(response_router, tags=["Response"])

# Initialize MemoryManager
memory_manager = MemoryManager()

# Basic routes
@app.get("/")
async def root():
    return {"message": "Welcome to Kyle Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# TODO: Implement these endpoints
@app.post("/listen")
async def listen(audio_file: UploadFile = File(...)):
    """Process audio input and convert to text"""
    # Store message in memory
    memory_manager.store_message("user", "Audio input processed")
    return {"message": "Audio processing endpoint - Not implemented yet"}

@app.post("/screen")
async def screen_capture():
    """Capture and analyze screen content"""
    return {"message": "Screen capture endpoint - Not implemented yet"}

@app.post("/respond")
async def generate_response(request: ResponseRequest = Body(...)):
    """Generate AI response based on input"""
    response = await response_router.generate_response(request)
    response_text = response.get("response")
    # Store assistant response in memory
    memory_manager.store_message("assistant", response_text)
    return {
        "success": True,
        "response": response_text,
        "usage": response.get("usage")
    }

if __name__ == "__main__":
    logger.info(f"Starting Kyle Assistant API on {API_HOST}:{API_PORT}")
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=DEBUG) 