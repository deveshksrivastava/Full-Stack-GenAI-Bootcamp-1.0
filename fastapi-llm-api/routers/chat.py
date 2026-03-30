import os
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class ChatRequest(BaseModel):
    message: str
    system: Optional[str] = "You are a helpful assistant."
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 1024


class ChatResponse(BaseModel):
    response: str
    model: str
    input_tokens: int
    output_tokens: int


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        message = client.messages.create(
            model=request.model,
            max_tokens=request.max_tokens,
            system=request.system,
            messages=[{"role": "user", "content": request.message}],
        )
        return ChatResponse(
            response=message.content[0].text,
            model=message.model,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid Anthropic API key")
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


class StreamRequest(BaseModel):
    message: str
    system: Optional[str] = "You are a helpful assistant."
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 1024


from fastapi.responses import StreamingResponse


@router.post("/chat/stream")
def chat_stream(request: StreamRequest):
    def generate():
        with client.messages.stream(
            model=request.model,
            max_tokens=request.max_tokens,
            system=request.system,
            messages=[{"role": "user", "content": request.message}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    return StreamingResponse(generate(), media_type="text/plain")
