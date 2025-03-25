from fastapi import APIRouter, HTTPException, Body
import openai
import logging
from pydantic import BaseModel
from typing import List

router = APIRouter()
logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class ResponseRequest(BaseModel):
    messages: List[Message]
    screen_context: str = None
    audio_context: str = None

@router.post("/respond")
async def generate_response(request: ResponseRequest = Body(...)):
    """
    Generate AI response based on input messages and context
    """
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        system_message = "You are Kyle, an AI assistant inspired by Jarvis from Iron Man. Be helpful, concise, and friendly."
        
        if request.screen_context:
            system_message += f"\n\nScreen context: {request.screen_context}"
        
        if request.audio_context:
            system_message += f"\n\nAudio context: {request.audio_context}"
        
        messages.insert(0, {"role": "system", "content": system_message})
        
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content
        logger.info(f"Generated response: {response_text[:50]}...")
        
        return {
            "success": True,
            "response": response_text,
            "usage": response.usage
        }
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=str(e))