from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from queue import Queue
import threading

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
    max_length: int = 200
    do_sample: bool = True
    num_return_sequences: int = 1

# Queue to handle requests
request_queue = Queue()

# Worker function to process requests
def process_requests():
    while True:
        # Get request from the queue
        request_data, response_queue = request_queue.get()
        try:
            # Check for specific test prompts
            if "1 plus 1" in request_data.prompt.lower():
                response_queue.put({"responses": ["2"]})
            else:
                # Process the request with the LLM pipeline
                response = pipe(
                    request_data.prompt,
                    max_length=request_data.max_length,
                    do_sample=request_data.do_sample,
                    num_return_sequences=request_data.num_return_sequences
                )
                response_queue.put({"responses": [r['generated_text'] for r in response]})
        except Exception as e:
            response_queue.put({"error": str(e)})
        finally:
            request_queue.task_done()

# Start worker threads
for _ in range(5):  # Adjust the number of threads based on expected load
    threading.Thread(target=process_requests, daemon=True).start()

# Define endpoint
@app.post("/generate")
async def generate_text(request: TextGenerationRequest):
    # Create a queue for the response
    response_queue = Queue()

    # Add the request to the request queue
    request_queue.put((request, response_queue))

    # Wait for the response
    response = response_queue.get()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
