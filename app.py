import asyncio
import signal
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Initialize FastAPI app
app = FastAPI()

# Load model and tokenizer
model_name = "openlm-research/open_llama_3b"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
offload_folder = r"D:\Offloader"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    offload_folder=offload_folder
)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Define request model
class TextGenerationRequest(BaseModel):
    prompt: str
    max_length: int = 500
    do_sample: bool = True
    num_return_sequences: int = 1
    truncation: bool = True

# Define health check endpoint
@app.get("/health", summary="Health Check")
async def health_check():
    return {"status": "healthy"}

# Define text generation endpoint
@app.post("/generate", summary="Generate Text")
async def generate_text(request: TextGenerationRequest):
    try:
        # Run blocking pipeline call in a separate thread to avoid blocking event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: pipe(
                request.prompt,
                max_length=request.max_length,
                do_sample=request.do_sample,
                num_return_sequences=request.num_return_sequences,
                truncation=request.truncation
            )
        )
        return {"responses": [r['generated_text'] for r in response]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add signal handling for graceful shutdown
def graceful_shutdown(signum, frame):
    print("Received shutdown signal, shutting down gracefully...")
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, graceful_shutdown)

# You can now run the app with Uvicorn:
# uvicorn app:app --host 0.0.0.0 --port 8000
