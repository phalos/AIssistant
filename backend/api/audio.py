import speech_recognition as sr
from fastapi import APIRouter, HTTPException, UploadFile, File
import tempfile
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/listen")
async def process_audio(audio_file: UploadFile = File(...)):
    """
    Process audio file and convert to text using Whisper API
    """
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            # Write the uploaded file content to the temporary file
            content = await audio_file.read()
            temp_audio.write(content)
            temp_path = temp_audio.name
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Process the audio file
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            
            # Use Whisper API for transcription
            try:
                text = recognizer.recognize_whisper(audio_data)
                logger.info(f"Transcribed text: {text}")
                return {"text": text, "success": True}
            except sr.UnknownValueError:
                logger.warning("Whisper API could not understand audio")
                return {"text": "", "success": False, "error": "Could not understand audio"}
            except sr.RequestError as e:
                logger.error(f"Could not request results from Whisper API; {e}")
                raise HTTPException(status_code=500, detail=f"API request error: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if 'temp_path' in locals():
            os.unlink(temp_path) 