from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import traceback

from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger


logger = get_logger(__name__)

app = FastAPI(
    title="Multi AI Agent",
    version="1.0.0"
)


class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


@app.get("/")
def root():
    return {
        "status": "Backend is running",
        "service": "Multi AI Agent API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat_endpoint(request: RequestState):

    logger.info(
        f"Received request for model: {request.model_name}"
    )

    # ---------------------------------------------------------
    # Validate model
    # ---------------------------------------------------------

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid model name: {request.model_name}"
        )

    # ---------------------------------------------------------
    # Validate messages
    # ---------------------------------------------------------

    if not request.messages:

        raise HTTPException(
            status_code=400,
            detail="At least one message is required."
        )

    query = request.messages[-1]

    try:

        logger.info(
            f"Processing query: {query}"
        )

        response = get_response_from_ai_agents(
            llm_id=request.model_name,
            query=query,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )

        logger.info(
            f"Successfully generated response "
            f"using {request.model_name}"
        )

        return {
            "response": response
        }

    except Exception as e:

        logger.error(
            "Error occurred while generating AI response",
            exc_info=True
        )

        print("\n" + "=" * 80)
        print("ERROR IN /chat ENDPOINT")
        print("=" * 80)
        traceback.print_exc()
        print("=" * 80 + "\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )