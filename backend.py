from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BartTokenizer, BartForConditionalGeneration

# Load model and tokenizer
model_path = "path_to_save_model"
tokenizer_path = "path_to_save_tokenizer"
tokenizer = BartTokenizer.from_pretrained(tokenizer_path)
model = BartForConditionalGeneration.from_pretrained(model_path)

# Initialize FastAPI app
app = FastAPI()

# Define the request body schema
class Scenario(BaseModel):
    description: str

# Define the endpoint to generate PlantUML code
@app.post("/generate/")
def generate_plantuml(scenario: Scenario):
    try:
        # Tokenize the input description
        inputs = tokenizer(scenario.description, return_tensors="pt")
        # Generate PlantUML code using the model
        outputs = model.generate(**inputs)
        # Decode the generated output
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"plantuml": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, use the command: uvicorn filename:app --reload
