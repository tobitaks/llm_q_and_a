# LLM Q&A Service

A simple web application that allows users to ask questions and receive answers powered by LLMs (supports Anthropic, OpenAI, and Google Gemini).

## Project Structure

```
llm_q_and_a/
├── main.py              # FastAPI application
├── templates/
│   └── index.html       # Frontend
├── requirements.txt     # Python dependencies
├── setup.sh             # Automated setup script
├── DEPLOYMENT.md        # Ubuntu deployment guide
└── README.md            # This file
```

## Features

- Web interface for asking questions
- REST API endpoint (`POST /api/ask`)
- Structured JSON logging for observability
- Request tracing with unique request IDs

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **LLM:** LangChain (supports multiple providers)
- **Logging:** structlog (JSON format)
- **Frontend:** Vanilla HTML/JS

## Supported LLM Providers

| Provider | API Key | Model |
|----------|---------|-------|
| Anthropic | `ANTHROPIC_API_KEY` | claude-3-haiku-20240307 |
| OpenAI | `OPENAI_API_KEY` | gpt-3.5-turbo |
| Google | `GOOGLE_API_KEY` | gemini-1.5-flash (free tier) |

Set one API key in `.env` and the app auto-detects which provider to use.

## Getting Started (Development)

1. **Clone and setup**
   ```bash
   git clone https://github.com/tobitaks/llm_q_and_a.git
   cd llm_q_and_a
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure API key**
   ```bash
   cp .env.example .env
   # Edit .env and set ONE of: ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY
   ```

3. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Open the app**

   Navigate to `http://localhost:8000`

For production deployment on Ubuntu Server, see [DEPLOYMENT.md](DEPLOYMENT.md).

## API Usage

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of France?"}'
```

Response:

```json
{
  "answer": "The capital of France is Paris."
}
```

## Assumptions

- **No database required** - This is a stateless Q&A service
- **No authentication** - Open access for simplicity
- **Single-user focus** - No session management or user tracking
- **Internet access required** - Needs to reach LLM provider's API

## Trade-offs

- **Vanilla JS frontend** — No framework overhead. Easy to understand and modify.
- **structlog for logging** — Provides structured JSON logs out of the box, making logs easily parseable by log aggregation tools.
- **Synchronous LLM calls** — Uses sync endpoints for simplicity. For higher concurrency, could switch to async with `await chain.ainvoke()`.

## Log Events

All logs are JSON to stdout with these events:

| Event | Description |
|-------|-------------|
| `request_received` | Logged when a question is received |
| `llm_invocation` | Logged before calling the LLM |
| `response_generated` | Logged after LLM responds (includes latency, tokens) |
| `error` | Logged on exceptions (includes stack trace) |


```
