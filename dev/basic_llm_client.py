import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load model and tokenizer
model_name = "openlm-research/open_llama_3b"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
offload_folder = r"C:\Offloader"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    offload_folder=offload_folder
)

# Initialize pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Define categories and questions
questions = {
    "General Information": [
        "What are the basic principles of quantum mechanics?",
        "Can you tell me about the history of the internet?",
        "What is the significance of the Rosetta Stone?"
    ],
    "Technical Help": [
        "How do I create a responsive navigation bar in HTML and CSS?",
        "Explain the difference between machine learning and deep learning.",
        "What are the best practices for securing a home Wi-Fi network?"
    ],
    "Educational Assistance": [
        "Can you help explain the concept of supply and demand in economics?",
        "What is the Pythagorean theorem and how do I apply it?",
        "How do I write a thesis statement for an essay on climate change?"
    ],
    "Advice and Recommendations": [
        "What are some effective time management strategies for college students?",
        "Can you recommend some healthy meal prep ideas for a busy week?",
        "What are the best exercises for improving cardiovascular health?"
    ],
    "Language Learning": [
        "How do you pronounce 'schön' in German and what does it mean?",
        "What are some common phrases to know when traveling to France?",
        "Can you explain the different past tenses in Spanish?"
    ]
}

# Loop through each category and question, and record response times
for category, qs in questions.items():
    print(f"\nCategory: {category}\n" + "="*20)
    for question in qs:
        print(f"\nQuestion: {question}")
        start_time = time.time()
        
        # Generate response
        question = "What are the basic principles of quantum mechanics?"
        response = pipe(question, max_length=200, do_sample=True, num_return_sequences=1, truncation=True)
        
        end_time = time.time()
        response_text = response[0]['generated_text']
        response_time = end_time - start_time
        
        print(f"Response: {response_text}")
        print(f"Response Time: {response_time:.2f} seconds")

