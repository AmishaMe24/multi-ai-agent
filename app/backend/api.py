from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
app = FastAPI(title="Multi AI Agent", version="1.0.0")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received chat request with model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400, detail="Model not allowed")
    try:
        response = get_response_from_ai_agents(
            model_name=request.model_name,
            system_prompt=request.system_prompt,
            query=request.messages,
            allow_search=request.allow_search
        )
        logger.info(f"Response generated for model: {request.model_name}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, 
                            detail=str(CustomException("Failed to get AI response", error_detail=e)))

