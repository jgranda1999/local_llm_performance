import asyncio
import signal
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
import requests

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API Key (Make sure to set this securely in production)
API_KEY =  ":)"
MODEL = "gpt-4o-mini"
API_URL = "https://api.openai.com/v1/chat/completions"

# Define health check endpoint
@app.get("/health", summary="Health Check")
async def health_check():
    return {"status": "healthy"}

class TextGenerationRequest(BaseModel):
    prompt: str

@app.post("/generate", summary="Generate Text")
async def generate_text(request: TextGenerationRequest):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Answer my questions."},
            {"role": "user", "content": request.prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        completion = response.json()

        ai_response = completion['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    return {"response": ai_response}

# Add signal handling for graceful shutdown
def graceful_shutdown(signum, frame):
    print("Received shutdown signal, shutting down gracefully...")
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, graceful_shutdown)

# You can now run the app with Uvicorn:
# uvicorn app:app --host 127.0.0.1 --port 8001
