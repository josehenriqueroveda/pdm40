import os
from fastapi import FastAPI
from fastapi import Request
from fastapi import HTTPException
from openai import OpenAIError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models.pdm_request import PDMRequest
from app.agents.pdm_writer import PDMWriter
from app.core.security import request_limiter

load_dotenv()
openai_key = os.getenv("OPEN_AI_KEY")
REQUEST_LIMIT = os.getenv("REQUEST_LIMIT", "100/day")
limiter = request_limiter.get_limiter()
pdm_writer = PDMWriter(api_key=openai_key)

app = FastAPI(
    title="PDM40 API",
    description="API for an AI agent to read the description of the requested material and adapt the name to SAP's 40-character PDM standard.",
    version="0.1.0",
    openapi_url="/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the PDM40 API!"}


@app.get("/health", tags=["Monitoring"])
async def status():
    return {"local_status": "ok", "openAI_status": "https://status.openai.com/"}


@app.post("/pdm", tags=["PDM"])
@limiter.limit(REQUEST_LIMIT)
async def get_pdm(payload: PDMRequest, request: Request):
    try:
        pdm = pdm_writer.write_pdm(payload.description)
        if pdm is None:
            raise HTTPException(status_code=500, detail="Failed to generate PDM.")
        return {"pdm": pdm}
    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"Error on OpenAI API: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error.")
