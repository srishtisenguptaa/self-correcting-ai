from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import run_agent

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Self-Correcting AI API is running"}

@app.post("/process")
def process_text(input_data: TextInput):
    result = run_agent(input_data.text)
    return result
