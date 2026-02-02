import os
import time
import uuid
import traceback
from contextvars import ContextVar

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Context variable for request ID
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(0),
    context_class=dict,
    cache_logger_on_first_use=True,
)

# Create a logger instance
logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(title="LLM Q&A Service")

# Set up templates
templates = Jinja2Templates(directory="templates")


def get_llm():
    """Initialize LLM based on available API key."""
    if os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-3-haiku-20240307"), "claude-3-haiku-20240307"
    elif os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-3.5-turbo"), "gpt-3.5-turbo"
    elif os.getenv("GOOGLE_API_KEY"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash"), "gemini-1.5-flash"
    else:
        raise ValueError(
            "No API key found. Set one of: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY"
        )


# Initialize LLM
llm, model_name = get_llm()

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])
chain = prompt | llm


# Request model
class QuestionRequest(BaseModel):
    question: str


# Response model
class AnswerResponse(BaseModel):
    answer: str


# Middleware to add request ID
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Root route - serve frontend
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# API endpoint
@app.post("/api/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    request_id = request_id_var.get()

    try:
        # Log request received
        logger.info(
            "request_received",
            request_id=request_id,
            input_length=len(req.question)
        )

        # Log LLM invocation
        logger.info(
            "llm_invocation",
            request_id=request_id,
            model=model_name
        )

        # Call LLM and measure latency
        start = time.perf_counter()
        response = chain.invoke({"question": req.question})
        latency_ms = (time.perf_counter() - start) * 1000

        # Extract token usage from response metadata
        token_usage = response.response_metadata.get("usage", {})

        # Log response generated
        logger.info(
            "response_generated",
            request_id=request_id,
            latency_ms=round(latency_ms, 2),
            token_usage=token_usage
        )

        return AnswerResponse(answer=response.content)

    except Exception as e:
        # Log error with stack trace
        logger.error(
            "error",
            request_id=request_id,
            error_type=type(e).__name__,
            error_message=str(e),
            stack_trace=traceback.format_exc()
        )
        raise
