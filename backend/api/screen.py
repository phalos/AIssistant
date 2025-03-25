from fastapi import APIRouter, HTTPException
import cv2
import numpy as np
import base64
import logging
from PIL import ImageGrab
import io

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/screen")
async def capture_screen():
    """
    Capture the screen and return the image data
    """
    try:
        # Capture the screen
        screenshot = ImageGrab.grab()
        
        # Convert PIL Image to numpy array
        screenshot_np = np.array(screenshot)
        
        # Convert RGB to BGR (OpenCV format)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Process the image (basic processing for now)
        # In future versions, we can add more advanced image analysis here
        gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        
        # Encode the processed image to base64 for sending over API
        _, buffer = cv2.imencode('.jpg', screenshot_cv)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        
        # Return the image data
        return {
            "success": True,
            "image_data": jpg_as_text,
            "width": screenshot.width,
            "height": screenshot.height
        }
    except Exception as e:
        logger.error(f"Error capturing screen: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 