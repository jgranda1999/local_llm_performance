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
    max_length: int = 200
    do_sample: bool = True
    num_return_sequences: int = 1

# Define endpoint
@app.post("/generate")
def generate_text(request: TextGenerationRequest):
    try:
        response = pipe(
            request.prompt,
            max_length=request.max_length,
            do_sample=request.do_sample,
            num_return_sequences=request.num_return_sequences
        )
        return {"responses": [r['generated_text'] for r in response]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
